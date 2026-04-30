from __future__ import annotations

import csv
import io
import json
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
    assert "meta" in payload


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


def create_project(client: TestClient, name: str = "Export Project", priority: int = 7) -> dict:
    return assert_success_envelope(
        client.post("/api/v1/projects", json={"name": name, "priority": priority}).json()
    )


def create_task(client: TestClient, title: str, minutes: int, project_id: int | None = None) -> dict:
    payload = {
        "title": title,
        "estimated_minutes": minutes,
        "cognitive_load": 5,
        "project_id": project_id,
    }
    return assert_success_envelope(client.post("/api/v1/tasks", json=payload).json())


def submit_feedback(
    client: TestClient,
    task_id: int,
    target_date: date,
    *,
    status: str = "done",
    actual_minutes: int | None = 35,
    note: str | None = None,
) -> dict:
    payload = {
        "task_id": task_id,
        "status": status,
        "date": target_date.isoformat(),
        "actual_minutes": actual_minutes,
        "note": note,
    }
    return assert_success_envelope(client.post("/api/v1/execution/feedback", json=payload).json())


def test_task_export_returns_json_with_project_context(client: TestClient) -> None:
    project = create_project(client)
    task = create_task(client, "Export planning notes", 45, project["id"])

    export = assert_success_envelope(client.get("/api/v1/exports/tasks").json())
    content = json.loads(export["content"])

    assert export["filename"] == "focusflow-tasks.json"
    assert export["content_type"] == "application/json"
    assert export["record_count"] == 1
    assert content[0]["id"] == task["id"]
    assert content[0]["project_id"] == project["id"]
    assert content[0]["project_name"] == "Export Project"
    assert content[0]["project_priority"] == 7


def test_execution_history_export_filters_single_date(client: TestClient) -> None:
    first = create_task(client, "First day", 30)
    second = create_task(client, "Second day", 60)
    submit_feedback(client, first["id"], date(2026, 5, 1), actual_minutes=40)
    submit_feedback(client, second["id"], date(2026, 5, 2), actual_minutes=70)

    export = assert_success_envelope(
        client.get("/api/v1/exports/execution-history?date=2026-05-01").json()
    )
    content = json.loads(export["content"])

    assert export["filename"] == "focusflow-execution-history-2026-05-01.json"
    assert export["record_count"] == 1
    assert content[0]["task_title_snapshot"] == "First day"
    assert content[0]["actual_minutes"] == 40
    assert content[0]["date"] == "2026-05-01"


def test_execution_history_export_filters_inclusive_date_range(client: TestClient) -> None:
    before = create_task(client, "Before", 20)
    inside = create_task(client, "Inside", 25)
    after = create_task(client, "After", 35)
    submit_feedback(client, before["id"], date(2026, 4, 30))
    submit_feedback(client, inside["id"], date(2026, 5, 1))
    submit_feedback(client, after["id"], date(2026, 5, 3))

    export = assert_success_envelope(
        client.get(
            "/api/v1/exports/execution-history?start_date=2026-05-01&end_date=2026-05-02"
        ).json()
    )
    content = json.loads(export["content"])

    assert export["filename"] == "focusflow-execution-history-2026-05-01-to-2026-05-02.json"
    assert [item["task_title_snapshot"] for item in content] == ["Inside"]


def test_daily_review_export_returns_stable_csv_with_variance(client: TestClient) -> None:
    task = create_task(client, "Review export", 50)
    submit_feedback(client, task["id"], date(2026, 5, 1), actual_minutes=65, note="Ran long")

    export = assert_success_envelope(client.get("/api/v1/exports/daily-review?date=2026-05-01").json())
    rows = list(csv.DictReader(io.StringIO(export["content"])))

    assert export["filename"] == "focusflow-daily-review-2026-05-01.csv"
    assert export["content_type"] == "text/csv"
    assert export["record_count"] == 1
    assert rows[0] == {
        "date": "2026-05-01",
        "task_id": str(task["id"]),
        "task_title": "Review export",
        "status": "done",
        "estimated_minutes": "50",
        "actual_minutes": "65",
        "estimate_variance_minutes": "15",
        "note": "Ran long",
    }


def test_invalid_export_date_range_returns_error_envelope(client: TestClient) -> None:
    task = create_task(client, "No mutation", 20)
    submit_feedback(client, task["id"], date(2026, 5, 1))

    response = client.get(
        "/api/v1/exports/execution-history?start_date=2026-05-03&end_date=2026-05-01"
    )

    assert response.status_code == 400
    assert_error_envelope(response.json(), "invalid_date_range")
    history = assert_success_envelope(client.get("/api/v1/execution/history?date=2026-05-01").json())
    assert len(history) == 1
