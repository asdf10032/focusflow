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


def generate_and_select(client: TestClient, target_date: date, plan_type: str = "balanced") -> dict:
    payload = assert_success_envelope(
        client.post("/api/v1/schedules/generate", json={"date": target_date.isoformat()}).json()
    )
    assert_success_envelope(
        client.post(
            "/api/v1/schedules/select",
            json={"date": target_date.isoformat(), "plan_type": plan_type},
        ).json()
    )
    return next(plan for plan in payload["plans"] if plan["plan_type"] == plan_type)


def submit_feedback(
    client: TestClient,
    task_id: int,
    status: str,
    target_date: date,
    actual_minutes: int | None = None,
    note: str | None = None,
) -> dict:
    payload = {"task_id": task_id, "status": status, "date": target_date.isoformat()}
    if actual_minutes is not None:
        payload["actual_minutes"] = actual_minutes
    if note is not None:
        payload["note"] = note
    return assert_success_envelope(client.post("/api/v1/execution/feedback", json=payload).json())


def get_progress(client: TestClient, target_date: date) -> dict:
    return assert_success_envelope(
        client.get(f"/api/v1/execution/progress?date={target_date.isoformat()}").json()
    )


def get_review(client: TestClient, target_date: date) -> dict:
    return assert_success_envelope(
        client.get(f"/api/v1/execution/review?date={target_date.isoformat()}").json()
    )


def test_progress_returns_empty_metrics_without_selected_plan(client: TestClient) -> None:
    target_date = date(2026, 4, 28)

    progress = get_progress(client, target_date)

    assert progress == {
        "date": target_date.isoformat(),
        "selected_plan": None,
        "planned_count": 0,
        "completed_count": 0,
        "skipped_incomplete_count": 0,
        "completion_rate": 0.0,
    }


def test_progress_counts_selected_work_and_latest_feedback(client: TestClient) -> None:
    target_date = date(2026, 4, 28)
    done_task = create_task(client, "Done work", 40)
    skipped_task = create_task(client, "Skipped work", 30)
    open_task = create_task(client, "Open work", 20)
    generate_and_select(client, target_date)

    submit_feedback(client, done_task["id"], "done", target_date, actual_minutes=35)
    submit_feedback(client, skipped_task["id"], "skipped", target_date)

    progress = get_progress(client, target_date)

    assert progress["selected_plan"]["plan_type"] == "balanced"
    assert progress["planned_count"] == 3
    assert progress["completed_count"] == 1
    assert progress["skipped_incomplete_count"] == 2
    assert progress["completion_rate"] == pytest.approx(1 / 3)
    assert open_task["id"] not in [done_task["id"], skipped_task["id"]]


def test_progress_refreshes_after_feedback_submission(client: TestClient) -> None:
    target_date = date(2026, 4, 28)
    task = create_task(client, "Refresh metrics", 45)
    generate_and_select(client, target_date)

    before = get_progress(client, target_date)
    submit_feedback(client, task["id"], "done", target_date)
    after = get_progress(client, target_date)

    assert before["completed_count"] == 0
    assert after["completed_count"] == 1
    assert after["completion_rate"] == 1.0


def test_daily_review_returns_duration_totals_and_variance(client: TestClient) -> None:
    target_date = date(2026, 4, 28)
    first = create_task(client, "Estimate tightly", 40)
    second = create_task(client, "Estimate loosely", 30)
    generate_and_select(client, target_date)

    submit_feedback(client, first["id"], "done", target_date, actual_minutes=50, note="Ran long")
    submit_feedback(client, second["id"], "incomplete", target_date, actual_minutes=10)

    review = get_review(client, target_date)

    assert review["summary"]["planned_count"] == 2
    assert review["summary"]["completed_count"] == 1
    assert review["summary"]["skipped_incomplete_count"] == 1
    assert review["summary"]["planned_minutes"] == 70
    assert review["summary"]["actual_minutes"] == 60
    assert review["summary"]["estimate_variance_minutes"] == -10
    assert [item["task_title_snapshot"] for item in review["items"]] == [
        "Estimate tightly",
        "Estimate loosely",
    ]
    assert review["items"][0]["estimate_variance_minutes"] == 10
    assert review["items"][0]["note"] == "Ran long"
    assert review["items"][1]["status"] == "incomplete"


def test_review_filters_by_date_and_preserves_snapshots(client: TestClient) -> None:
    first_date = date(2026, 4, 28)
    second_date = date(2026, 4, 29)
    task = create_task(client, "Original title", 25)
    generate_and_select(client, first_date)
    generate_and_select(client, second_date)

    submit_feedback(client, task["id"], "done", first_date, actual_minutes=30)
    assert_success_envelope(
        client.put(
            f"/api/v1/tasks/{task['id']}",
            json={"title": "Edited title", "estimated_minutes": 90},
        ).json()
    )
    submit_feedback(client, task["id"], "done", second_date, actual_minutes=80)

    first_review = get_review(client, first_date)
    second_review = get_review(client, second_date)

    assert len(first_review["items"]) == 1
    assert first_review["items"][0]["task_title_snapshot"] == "Original title"
    assert first_review["items"][0]["estimated_minutes_snapshot"] == 25
    assert first_review["items"][0]["estimate_variance_minutes"] == 5
    assert second_review["items"][0]["task_title_snapshot"] == "Edited title"
    assert second_review["items"][0]["estimated_minutes_snapshot"] == 90
