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
from backend.app.models.execution_log import ExecutionLog


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


def get_test_db_session() -> Session:
    override = app.dependency_overrides[get_db]
    generator = override()
    return next(generator)


def create_project(client: TestClient, name: str = "Learning Project") -> dict:
    return assert_success_envelope(
        client.post("/api/v1/projects", json={"name": name, "priority": 5}).json()
    )


def create_task(
    client: TestClient,
    title: str,
    minutes: int,
    cognitive_load: int = 5,
    project_id: int | None = None,
) -> dict:
    payload = {"title": title, "estimated_minutes": minutes, "cognitive_load": cognitive_load}
    if project_id is not None:
        payload["project_id"] = project_id
    return assert_success_envelope(client.post("/api/v1/tasks", json=payload).json())


def submit_done(
    client: TestClient,
    task_id: int,
    actual_minutes: int,
    target_date: date = date(2026, 4, 30),
) -> dict:
    return assert_success_envelope(
        client.post(
            "/api/v1/execution/feedback",
            json={
                "task_id": task_id,
                "status": "done",
                "date": target_date.isoformat(),
                "actual_minutes": actual_minutes,
            },
        ).json()
    )


def suggest_duration(client: TestClient, payload: dict) -> dict:
    return assert_success_envelope(client.post("/api/v1/ai/suggest-duration", json=payload).json())


def test_similar_history_returns_learned_suggestion_with_confidence(client: TestClient) -> None:
    project = create_project(client)
    first = create_task(client, "Write launch notes", 60, cognitive_load=6, project_id=project["id"])
    second = create_task(client, "Write launch note draft", 45, cognitive_load=6, project_id=project["id"])
    submit_done(client, first["id"], actual_minutes=70)
    submit_done(client, second["id"], actual_minutes=80)

    suggestion = suggest_duration(
        client,
        {
            "title": "write launch notes",
            "project_id": project["id"],
            "cognitive_load": 6,
            "estimated_minutes": 55,
        },
    )

    assert suggestion == {
        "suggested_minutes": 75,
        "confidence": "high",
        "sample_count": 2,
        "source": "history",
        "reason_code": "history_project_load_match",
        "reason": "Based on similar completed tasks in the same project and load band.",
    }


def test_suggestion_uses_snapshots_after_task_is_edited(client: TestClient) -> None:
    project = create_project(client)
    task = create_task(client, "Estimate backend API", 40, cognitive_load=8, project_id=project["id"])
    submit_done(client, task["id"], actual_minutes=95)

    assert_success_envelope(
        client.put(
            f"/api/v1/tasks/{task['id']}",
            json={
                "title": "Completely different title",
                "estimated_minutes": 15,
                "cognitive_load": 2,
                "project_id": None,
            },
        ).json()
    )

    suggestion = suggest_duration(
        client,
        {"title": "estimate backend api", "project_id": project["id"], "cognitive_load": 8},
    )

    assert suggestion["suggested_minutes"] == 95
    assert suggestion["sample_count"] == 1
    assert suggestion["confidence"] == "high"
    assert suggestion["source"] == "history"


def test_non_done_and_missing_actual_minutes_logs_are_ignored(client: TestClient) -> None:
    done_task = create_task(client, "Read scheduler code", 30, cognitive_load=4)
    incomplete_task = create_task(client, "Read scheduler internals", 30, cognitive_load=4)
    no_actual_task = create_task(client, "Read scheduler docs", 30, cognitive_load=4)
    submit_done(client, done_task["id"], actual_minutes=35)
    assert_success_envelope(
        client.post(
            "/api/v1/execution/feedback",
            json={
                "task_id": incomplete_task["id"],
                "status": "incomplete",
                "date": "2026-04-30",
                "actual_minutes": 120,
            },
        ).json()
    )
    assert_success_envelope(
        client.post(
            "/api/v1/execution/feedback",
            json={"task_id": no_actual_task["id"], "status": "done", "date": "2026-04-30"},
        ).json()
    )

    suggestion = suggest_duration(client, {"title": "read scheduler code", "cognitive_load": 4})

    assert suggestion["suggested_minutes"] == 35
    assert suggestion["sample_count"] == 1
    assert suggestion["source"] == "history"


def test_fallback_uses_current_estimate_or_cognitive_load_band(client: TestClient) -> None:
    from_estimate = suggest_duration(
        client,
        {"title": "Brand new work", "estimated_minutes": 47, "cognitive_load": 9},
    )
    from_low_load = suggest_duration(client, {"title": "Tiny admin task", "cognitive_load": 2})
    from_unknown_load = suggest_duration(client, {"title": "Unclear task"})
    from_high_load = suggest_duration(client, {"title": "Deep design task", "cognitive_load": 9})

    assert from_estimate["suggested_minutes"] == 47
    assert from_estimate["confidence"] == "low"
    assert from_estimate["source"] == "fallback"
    assert from_estimate["reason_code"] == "fallback_current_estimate"
    assert from_low_load["suggested_minutes"] == 30
    assert from_unknown_load["suggested_minutes"] == 60
    assert from_high_load["suggested_minutes"] == 90


def test_suggest_duration_validates_bad_payload(client: TestClient) -> None:
    response = client.post(
        "/api/v1/ai/suggest-duration",
        json={"title": "", "cognitive_load": 11, "estimated_minutes": 481},
    )

    assert response.status_code == 422


def test_feedback_snapshots_project_and_cognitive_load(client: TestClient) -> None:
    project = create_project(client)
    task = create_task(client, "Snapshot context", 50, cognitive_load=7, project_id=project["id"])

    submit_done(client, task["id"], actual_minutes=55)

    db = get_test_db_session()
    try:
        log = db.query(ExecutionLog).one()
        assert log.task_project_id_snapshot == project["id"]
        assert log.cognitive_load_snapshot == 7
    finally:
        db.close()
