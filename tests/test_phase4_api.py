from __future__ import annotations

from datetime import date, datetime, timedelta
from typing import Iterator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from backend.app.db.base import Base
from backend.app.db.session import get_db
from backend.app.main import app
from backend.app.models.schedule_plan import SchedulePlan


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


def create_task(client: TestClient, title: str, minutes: int = 30) -> dict:
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


def test_validate_move_accepts_non_conflicting_move(client: TestClient) -> None:
    target_date = date(2026, 4, 26)
    task = create_task(client, "Draft outline")
    generate_and_select(client, target_date)

    start = datetime(2026, 4, 26, 15, 0)
    payload = assert_success_envelope(
        client.post(
            "/api/v1/schedules/validate-move",
            json={
                "date": target_date.isoformat(),
                "plan_type": "balanced",
                "task_id": task["id"],
                "start_datetime": start.isoformat(),
                "end_datetime": (start + timedelta(minutes=30)).isoformat(),
            },
        ).json()
    )

    assert payload["valid"] is True
    assert payload["conflicts"] == []
    assert payload["proposed_item"]["task_id"] == task["id"]


def test_validate_move_reports_overlap_conflict(client: TestClient) -> None:
    target_date = date(2026, 4, 26)
    create_task(client, "First task")
    second = create_task(client, "Second task")
    plan = generate_and_select(client, target_date)
    occupied = plan["items"][0]

    payload = assert_success_envelope(
        client.post(
            "/api/v1/schedules/validate-move",
            json={
                "date": target_date.isoformat(),
                "plan_type": "balanced",
                "task_id": second["id"],
                "start_datetime": occupied["start_datetime"],
                "end_datetime": occupied["end_datetime"],
            },
        ).json()
    )

    assert payload["valid"] is False
    assert [conflict["type"] for conflict in payload["conflicts"]] == ["overlap"]


def test_validate_move_reports_missing_plan(client: TestClient) -> None:
    target_date = date(2026, 4, 26)
    task = create_task(client, "Unscheduled")
    start = datetime(2026, 4, 26, 9, 0)

    payload = assert_success_envelope(
        client.post(
            "/api/v1/schedules/validate-move",
            json={
                "date": target_date.isoformat(),
                "plan_type": "balanced",
                "task_id": task["id"],
                "start_datetime": start.isoformat(),
                "end_datetime": (start + timedelta(minutes=30)).isoformat(),
            },
        ).json()
    )

    assert payload["valid"] is False
    assert payload["conflicts"][0]["type"] == "missing_plan"


def test_reoptimize_regenerates_plans_and_clears_selected_state(client: TestClient) -> None:
    target_date = date(2026, 4, 26)
    create_task(client, "Focused work")
    generate_and_select(client, target_date)

    payload = assert_success_envelope(
        client.post("/api/v1/schedules/reoptimize", json={"date": target_date.isoformat()}).json()
    )

    assert [plan["plan_type"] for plan in payload["plans"]] == [
        "conservative",
        "balanced",
        "aggressive",
    ]
    db = get_test_db_session()
    try:
        persisted = db.query(SchedulePlan).filter(SchedulePlan.date == target_date).all()
        assert len(persisted) == 3
        assert not any(plan.selected for plan in persisted)
    finally:
        db.close()


def test_today_execution_returns_selected_work(client: TestClient) -> None:
    target_date = date(2026, 4, 26)
    task = create_task(client, "Execute this")
    generate_and_select(client, target_date)

    payload = assert_success_envelope(
        client.get(f"/api/v1/execution/today?date={target_date.isoformat()}").json()
    )

    assert payload["date"] == target_date.isoformat()
    assert payload["selected_plan"]["plan_type"] == "balanced"
    assert payload["items"][0]["task"]["id"] == task["id"]
    assert payload["items"][0]["task"]["title"] == "Execute this"


def test_today_execution_returns_empty_payload_without_selected_plan(client: TestClient) -> None:
    target_date = date(2026, 4, 26)

    payload = assert_success_envelope(
        client.get(f"/api/v1/execution/today?date={target_date.isoformat()}").json()
    )

    assert payload == {"date": target_date.isoformat(), "selected_plan": None, "items": []}


def test_execution_feedback_updates_task_status(client: TestClient) -> None:
    task = create_task(client, "Finished task")

    payload = assert_success_envelope(
        client.post(
            "/api/v1/execution/feedback",
            json={"task_id": task["id"], "status": "done"},
        ).json()
    )

    assert payload["id"] == task["id"]
    assert payload["status"] == "done"


def test_parse_task_returns_structured_draft_from_duration_hint(client: TestClient) -> None:
    payload = assert_success_envelope(
        client.post("/api/v1/ai/parse-task", json={"text": "Write launch notes 90分钟 high"}).json()
    )

    assert payload["title"] == "Write launch notes"
    assert payload["estimated_minutes"] == 90
    assert payload["cognitive_load"] == 8
    assert payload["due_at"] is None
    assert payload["is_splittable"] is False
    assert payload["max_split_count"] == 1
    assert payload["status"] == "todo"
