from __future__ import annotations

from datetime import date
import json
from typing import Iterator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from backend.app.db.base import Base
from backend.app.db.session import get_db
from backend.app.main import app
from backend.app.models.blocked_time import BlockedTime
from backend.app.models.execution_log import ExecutionLog
from backend.app.models.schedule_plan import SchedulePlan
from backend.app.models.task import Task


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


def test_demo_seed_builds_repeatable_end_to_end_flow(client: TestClient) -> None:
    from backend.app.services.seeds.demo_data import seed_demo_data

    target_date = date(2026, 4, 27)
    db = get_test_db_session()
    try:
        first = seed_demo_data(db, target_date=target_date)
        second = seed_demo_data(db, target_date=target_date)

        assert first["date"] == target_date.isoformat()
        assert second["date"] == target_date.isoformat()
        assert db.query(Task).count() == 5
        assert db.query(BlockedTime).filter(BlockedTime.date == target_date).count() == 1
        assert db.query(SchedulePlan).filter(SchedulePlan.date == target_date).count() == 3
        assert first["review_date"] == target_date.isoformat()
        assert second["execution_log_count"] == first["execution_log_count"] == 2
        assert db.query(ExecutionLog).filter(ExecutionLog.date == target_date).count() == 2
        logs = db.query(ExecutionLog).filter(ExecutionLog.date == target_date).all()
        assert all(log.task_project_id_snapshot == first["project_id"] for log in logs)
        assert all(log.cognitive_load_snapshot is not None for log in logs)
        assert (
            db.query(SchedulePlan)
            .filter(SchedulePlan.date == target_date, SchedulePlan.selected.is_(True))
            .one()
            .plan_type
            == "balanced"
        )
    finally:
        db.close()

    today = assert_success_envelope(
        client.get(f"/api/v1/execution/today?date={target_date.isoformat()}").json()
    )
    assert today["selected_plan"]["plan_type"] == "balanced"
    assert len(today["items"]) >= 1

    progress = assert_success_envelope(
        client.get(f"/api/v1/execution/progress?date={target_date.isoformat()}").json()
    )
    assert progress["selected_plan"]["plan_type"] == "balanced"
    assert progress["planned_count"] >= 2
    assert progress["completed_count"] == 1

    review = assert_success_envelope(
        client.get(f"/api/v1/execution/review?date={target_date.isoformat()}").json()
    )
    assert len(review["items"]) == 2
    assert review["summary"]["actual_minutes"] > 0
    assert review["summary"]["estimate_variance_minutes"] is not None
    assert any(item["note"] for item in review["items"])

    history = assert_success_envelope(
        client.get(f"/api/v1/execution/history?date={target_date.isoformat()}").json()
    )
    assert len(history) == 2
    assert {item["status"] for item in history} == {"done", "incomplete"}

    searched_tasks = assert_success_envelope(client.get("/api/v1/tasks?q=advisor").json())
    assert [task["title"] for task in searched_tasks] == ["Review thesis outline"]
    assert searched_tasks[0]["notes"]

    task_export = assert_success_envelope(client.get("/api/v1/exports/tasks").json())
    exported_tasks = json.loads(task_export["content"])
    assert task_export["record_count"] == 5
    assert any(task["notes"] and "Searchable demo note" in task["notes"] for task in exported_tasks)

    history_export = assert_success_envelope(
        client.get(f"/api/v1/exports/execution-history?date={target_date.isoformat()}").json()
    )
    assert history_export["record_count"] == 2

    review_export = assert_success_envelope(
        client.get(f"/api/v1/exports/daily-review?date={target_date.isoformat()}").json()
    )
    assert review_export["record_count"] == 2

    feedbacked_task_ids = {item["task_id"] for item in history}
    partial_replan = assert_success_envelope(
        client.post("/api/v1/schedules/partial-replan", json={"date": target_date.isoformat()}).json()
    )
    balanced_replan = next(plan for plan in partial_replan["plans"] if plan["plan_type"] == "balanced")
    replanned_task_ids = {item["task_id"] for item in balanced_replan["items"]}
    assert replanned_task_ids
    assert replanned_task_ids.isdisjoint(feedbacked_task_ids)

    selected_replan = assert_success_envelope(
        client.post(
            "/api/v1/schedules/select",
            json={"date": target_date.isoformat(), "plan_type": "balanced"},
        ).json()
    )
    assert selected_replan["selected"] is True

    today_after_replan = assert_success_envelope(
        client.get(f"/api/v1/execution/today?date={target_date.isoformat()}").json()
    )
    assert today_after_replan["selected_plan"]["plan_type"] == "balanced"
    assert len(today_after_replan["items"]) >= 1

    history_suggestion = assert_success_envelope(
        client.post(
            "/api/v1/ai/suggest-duration",
            json={
                "title": "Prepare slide talking points",
                "project_id": first["project_id"],
                "cognitive_load": 4,
                "estimated_minutes": 30,
            },
        ).json()
    )
    assert history_suggestion["source"] == "history"
    assert history_suggestion["confidence"] == "high"
    assert history_suggestion["sample_count"] >= 1
    assert history_suggestion["suggested_minutes"] == 35

    fallback_suggestion = assert_success_envelope(
        client.post(
            "/api/v1/ai/suggest-duration",
            json={"title": "Plan a new workshop", "cognitive_load": 9},
        ).json()
    )
    assert fallback_suggestion["source"] == "fallback"
    assert fallback_suggestion["sample_count"] == 0
    assert fallback_suggestion["suggested_minutes"] == 90

    schedule = assert_success_envelope(
        client.post("/api/v1/schedules/generate", json={"date": target_date.isoformat()}).json()
    )
    assert "unplaced_reasons" in schedule
    assert all(plan["summary"] and plan["risk_explanation"] for plan in schedule["plans"])

    task_id = today_after_replan["items"][0]["task"]["id"]
    feedback = assert_success_envelope(
        client.post(
            "/api/v1/execution/feedback",
            json={"task_id": task_id, "status": "done", "date": target_date.isoformat()},
        ).json()
    )
    assert feedback["status"] == "done"

    draft = assert_success_envelope(
        client.post("/api/v1/ai/parse-task", json={"text": "Polish demo script 45min medium"}).json()
    )
    assert draft["title"] == "Polish demo script"
    assert draft["estimated_minutes"] == 45
    assert draft["cognitive_load"] == 5
