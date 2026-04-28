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


def assert_error_envelope(payload: dict, code: str) -> None:
    assert payload["status"] == "error"
    assert payload["data"] is None
    assert payload["error"]["code"] == code
    assert payload["meta"] is None


def create_task(client: TestClient, title: str, minutes: int = 30) -> dict:
    return assert_success_envelope(
        client.post(
            "/api/v1/tasks",
            json={"title": title, "estimated_minutes": minutes, "cognitive_load": 5},
        ).json()
    )


def get_history(client: TestClient, target_date: date) -> list[dict]:
    return assert_success_envelope(
        client.get(f"/api/v1/execution/history?date={target_date.isoformat()}").json()
    )


def test_feedback_done_creates_history_and_returns_updated_task(client: TestClient) -> None:
    target_date = date(2026, 4, 28)
    task = create_task(client, "Ship history", minutes=45)

    payload = assert_success_envelope(
        client.post(
            "/api/v1/execution/feedback",
            json={"task_id": task["id"], "status": "done", "date": target_date.isoformat()},
        ).json()
    )

    assert payload["id"] == task["id"]
    assert payload["status"] == "done"

    history = get_history(client, target_date)
    assert len(history) == 1
    assert history[0]["task_id"] == task["id"]
    assert history[0]["task_title_snapshot"] == "Ship history"
    assert history[0]["estimated_minutes_snapshot"] == 45
    assert history[0]["status"] == "done"
    assert history[0]["actual_minutes"] is None
    assert history[0]["note"] is None


def test_feedback_persists_actual_minutes_note_and_explicit_date(client: TestClient) -> None:
    target_date = date(2026, 4, 28)
    task = create_task(client, "Measure work", minutes=60)

    assert_success_envelope(
        client.post(
            "/api/v1/execution/feedback",
            json={
                "task_id": task["id"],
                "status": "done",
                "date": target_date.isoformat(),
                "actual_minutes": 75,
                "note": "Needed a little more focus time.",
            },
        ).json()
    )

    history = get_history(client, target_date)
    assert history[0]["actual_minutes"] == 75
    assert history[0]["note"] == "Needed a little more focus time."


def test_skipped_feedback_creates_history_and_leaves_task_todo(client: TestClient) -> None:
    target_date = date(2026, 4, 28)
    task = create_task(client, "Skip safely")

    payload = assert_success_envelope(
        client.post(
            "/api/v1/execution/feedback",
            json={"task_id": task["id"], "status": "skipped", "date": target_date.isoformat()},
        ).json()
    )

    assert payload["status"] == "todo"
    history = get_history(client, target_date)
    assert history[0]["status"] == "skipped"


def test_legacy_in_progress_feedback_records_incomplete_history(client: TestClient) -> None:
    target_date = date(2026, 4, 28)
    task = create_task(client, "Still working")

    payload = assert_success_envelope(
        client.post(
            "/api/v1/execution/feedback",
            json={"task_id": task["id"], "status": "in_progress", "date": target_date.isoformat()},
        ).json()
    )

    assert payload["status"] == "in_progress"
    history = get_history(client, target_date)
    assert history[0]["status"] == "incomplete"


def test_missing_task_feedback_returns_not_found_without_history(client: TestClient) -> None:
    target_date = date(2026, 4, 28)

    response = client.post(
        "/api/v1/execution/feedback",
        json={"task_id": 999, "status": "done", "date": target_date.isoformat()},
    )

    assert response.status_code == 404
    assert_error_envelope(response.json(), "not_found")
    assert get_history(client, target_date) == []


def test_history_filters_by_date_and_preserves_estimate_snapshot(client: TestClient) -> None:
    first_date = date(2026, 4, 28)
    second_date = date(2026, 4, 29)
    task = create_task(client, "Snapshot me", minutes=40)

    assert_success_envelope(
        client.post(
            "/api/v1/execution/feedback",
            json={"task_id": task["id"], "status": "done", "date": first_date.isoformat()},
        ).json()
    )
    assert_success_envelope(
        client.put(
            f"/api/v1/tasks/{task['id']}",
            json={"title": "Edited later", "estimated_minutes": 90},
        ).json()
    )
    assert_success_envelope(
        client.post(
            "/api/v1/execution/feedback",
            json={"task_id": task["id"], "status": "canceled", "date": second_date.isoformat()},
        ).json()
    )

    first_history = get_history(client, first_date)
    assert len(first_history) == 1
    assert first_history[0]["task_title_snapshot"] == "Snapshot me"
    assert first_history[0]["estimated_minutes_snapshot"] == 40
    assert first_history[0]["status"] == "done"

    second_history = get_history(client, second_date)
    assert len(second_history) == 1
    assert second_history[0]["task_title_snapshot"] == "Edited later"
    assert second_history[0]["estimated_minutes_snapshot"] == 90
    assert second_history[0]["status"] == "canceled"

