from __future__ import annotations

from datetime import date
from typing import Iterator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from backend.app.db.base import Base
from backend.app.db.session import get_db
from backend.app.main import app


@pytest.fixture()
def client() -> Iterator[TestClient]:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        future=True,
    )
    TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
    Base.metadata.create_all(bind=engine)

    def override_get_db() -> Iterator[Session]:
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()
        Base.metadata.drop_all(bind=engine)


def assert_success_envelope(payload: dict) -> object:
    assert payload["status"] == "success"
    assert "data" in payload
    assert payload["error"] is None
    assert "meta" in payload
    return payload["data"]


def create_task(client: TestClient, title: str, minutes: int) -> dict:
    return assert_success_envelope(
        client.post(
            "/api/v1/tasks",
            json={"title": title, "estimated_minutes": minutes, "cognitive_load": 5},
        ).json()
    )


def submit_feedback(
    client: TestClient,
    task_id: int,
    status: str,
    target_date: date,
    actual_minutes: int | None = None,
) -> dict:
    payload = {"task_id": task_id, "status": status, "date": target_date.isoformat()}
    if actual_minutes is not None:
        payload["actual_minutes"] = actual_minutes
    return assert_success_envelope(client.post("/api/v1/execution/feedback", json=payload).json())


def get_weekly_review(client: TestClient, target_date: date) -> dict:
    return assert_success_envelope(
        client.get(f"/api/v1/execution/weekly-review?date={target_date.isoformat()}").json()
    )


def test_weekly_review_returns_boundaries_summary_and_day_breakdown(client: TestClient) -> None:
    week_date = date(2026, 4, 29)
    monday = date(2026, 4, 27)
    sunday = date(2026, 5, 3)
    done_task = create_task(client, "Finish proposal", 40)
    skipped_task = create_task(client, "Call supplier", 30)
    incomplete_task = create_task(client, "Draft launch plan", 20)
    canceled_task = create_task(client, "Cancel stale task", 25)

    submit_feedback(client, done_task["id"], "done", monday, actual_minutes=50)
    submit_feedback(client, skipped_task["id"], "skipped", date(2026, 4, 29))
    submit_feedback(client, incomplete_task["id"], "incomplete", date(2026, 4, 30), actual_minutes=10)
    submit_feedback(client, canceled_task["id"], "canceled", date(2026, 5, 1))

    review = get_weekly_review(client, week_date)

    assert review["week_start"] == monday.isoformat()
    assert review["week_end"] == sunday.isoformat()
    assert review["summary"] == {
        "logged_count": 4,
        "completed_count": 1,
        "skipped_incomplete_count": 3,
        "completion_rate": 0.25,
        "planned_minutes": 115,
        "actual_minutes": 60,
        "estimate_variance_minutes": -55,
    }
    assert [day["date"] for day in review["days"]] == [
        "2026-04-27",
        "2026-04-28",
        "2026-04-29",
        "2026-04-30",
        "2026-05-01",
        "2026-05-02",
        "2026-05-03",
    ]
    assert review["days"][0]["summary"]["logged_count"] == 1
    assert review["days"][0]["items"][0]["task_title_snapshot"] == "Finish proposal"
    assert review["days"][0]["items"][0]["estimate_variance_minutes"] == 10
    assert review["days"][1]["summary"]["logged_count"] == 0
    assert review["days"][1]["summary"]["estimate_variance_minutes"] is None
    assert review["days"][1]["items"] == []
    assert review["comparison"] == {
        "available": False,
        "previous_week_start": "2026-04-20",
        "previous_week_end": "2026-04-26",
        "previous_summary": None,
        "deltas": None,
        "message_code": "previous_week_unavailable",
    }


def test_weekly_review_uses_execution_log_snapshots_after_task_edits(client: TestClient) -> None:
    task = create_task(client, "Original weekly item", 25)
    submit_feedback(client, task["id"], "done", date(2026, 4, 28), actual_minutes=30)

    assert_success_envelope(
        client.put(
            f"/api/v1/tasks/{task['id']}",
            json={"title": "Edited weekly item", "estimated_minutes": 90},
        ).json()
    )

    review = get_weekly_review(client, date(2026, 4, 30))

    item = review["days"][1]["items"][0]
    assert item["task_title_snapshot"] == "Original weekly item"
    assert item["estimated_minutes_snapshot"] == 25
    assert item["estimate_variance_minutes"] == 5
    assert review["summary"]["planned_minutes"] == 25
    assert review["summary"]["estimate_variance_minutes"] == 5


def test_weekly_review_returns_previous_week_comparison_deltas(client: TestClient) -> None:
    previous_done = create_task(client, "Previous done", 50)
    previous_incomplete = create_task(client, "Previous incomplete", 40)
    current_done = create_task(client, "Current done", 80)
    current_skipped = create_task(client, "Current skipped", 20)

    submit_feedback(client, previous_done["id"], "done", date(2026, 4, 20), actual_minutes=60)
    submit_feedback(client, previous_incomplete["id"], "incomplete", date(2026, 4, 21), actual_minutes=20)
    submit_feedback(client, current_done["id"], "done", date(2026, 4, 27), actual_minutes=100)
    submit_feedback(client, current_skipped["id"], "skipped", date(2026, 4, 28))

    review = get_weekly_review(client, date(2026, 4, 30))

    assert review["summary"]["completion_rate"] == 0.5
    assert review["summary"]["actual_minutes"] == 100
    assert review["summary"]["estimate_variance_minutes"] == 0
    assert review["comparison"]["available"] is True
    assert review["comparison"]["previous_week_start"] == "2026-04-20"
    assert review["comparison"]["previous_week_end"] == "2026-04-26"
    assert review["comparison"]["previous_summary"]["completion_rate"] == 0.5
    assert review["comparison"]["previous_summary"]["actual_minutes"] == 80
    assert review["comparison"]["previous_summary"]["estimate_variance_minutes"] == -10
    assert review["comparison"]["deltas"] == {
        "completion_rate": 0.0,
        "actual_minutes": 20,
        "estimate_variance_minutes": 10,
    }
    assert review["comparison"]["message_code"] is None


def test_weekly_review_returns_empty_week_metadata(client: TestClient) -> None:
    review = get_weekly_review(client, date(2026, 4, 30))

    assert review["week_start"] == "2026-04-27"
    assert review["week_end"] == "2026-05-03"
    assert review["summary"] == {
        "logged_count": 0,
        "completed_count": 0,
        "skipped_incomplete_count": 0,
        "completion_rate": 0.0,
        "planned_minutes": 0,
        "actual_minutes": 0,
        "estimate_variance_minutes": None,
    }
    assert len(review["days"]) == 7
    assert all(day["summary"]["logged_count"] == 0 for day in review["days"])
    assert all(day["items"] == [] for day in review["days"])
    assert review["comparison"]["available"] is False
    assert review["comparison"]["previous_summary"] is None
    assert review["comparison"]["deltas"] is None
