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
from backend.app.models.schedule_plan import SchedulePlan
from backend.app.models.task_dependency import TaskDependency
from backend.app.services.seeds.energy_templates import seed_default_templates


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


def test_health_returns_success_envelope(client: TestClient) -> None:
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert assert_success_envelope(response.json()) == {"ok": True}


def test_project_and_task_crud_use_success_envelopes(client: TestClient) -> None:
    project_response = client.post("/api/v1/projects", json={"name": "Thesis", "priority": 8})
    project = assert_success_envelope(project_response.json())
    assert project["name"] == "Thesis"
    assert project["priority"] == 8

    projects = assert_success_envelope(client.get("/api/v1/projects").json())
    assert [item["name"] for item in projects] == ["Thesis"]

    task_response = client.post(
        "/api/v1/tasks",
        json={
            "title": "Write proposal",
            "estimated_minutes": 60,
            "cognitive_load": 7,
            "project_id": project["id"],
        },
    )
    task = assert_success_envelope(task_response.json())
    assert task["title"] == "Write proposal"
    assert task["status"] == "todo"

    updated = assert_success_envelope(
        client.put(f"/api/v1/tasks/{task['id']}", json={"status": "in_progress"}).json()
    )
    assert updated["status"] == "in_progress"

    tasks = assert_success_envelope(client.get("/api/v1/tasks?status=in_progress").json())
    assert [item["id"] for item in tasks] == [task["id"]]

    assert assert_success_envelope(client.delete(f"/api/v1/tasks/{task['id']}").json()) is True


def test_energy_templates_and_blocked_times_use_success_envelopes(client: TestClient) -> None:
    with next(get_db_override := app.dependency_overrides[get_db]()) as db:
        seed_default_templates(db)

    templates = assert_success_envelope(client.get("/api/v1/energy/templates").json())
    assert len(templates) == 6
    assert {template["name"] for template in templates} == {"early_bird", "normal", "night_owl"}
    assert all(len(template["slots"]) == 48 for template in templates)

    blocked = assert_success_envelope(
        client.post(
            "/api/v1/blocked-times",
            json={
                "date": date.today().isoformat(),
                "start_minute_of_day": 540,
                "end_minute_of_day": 600,
                "category": "class",
            },
        ).json()
    )
    assert blocked["category"] == "class"

    blocked_list = assert_success_envelope(client.get("/api/v1/blocked-times").json())
    assert [item["id"] for item in blocked_list] == [blocked["id"]]


def test_schedule_generate_returns_three_plan_types(client: TestClient) -> None:
    client.post(
        "/api/v1/tasks",
        json={"title": "Read paper", "estimated_minutes": 30, "cognitive_load": 4},
    )

    payload = assert_success_envelope(
        client.post("/api/v1/schedules/generate", json={"date": date.today().isoformat()}).json()
    )

    assert [plan["plan_type"] for plan in payload["plans"]] == [
        "conservative",
        "balanced",
        "aggressive",
    ]


def test_schedule_generate_persists_three_plans_and_respects_blocked_slots(client: TestClient) -> None:
    target_date = date(2026, 4, 26)
    client.post(
        "/api/v1/blocked-times",
        json={
            "date": target_date.isoformat(),
            "start_minute_of_day": 0,
            "end_minute_of_day": 30,
            "category": "sleep",
        },
    )
    client.post(
        "/api/v1/tasks",
        json={"title": "Morning review", "estimated_minutes": 30, "cognitive_load": 3},
    )

    payload = assert_success_envelope(
        client.post("/api/v1/schedules/generate", json={"date": target_date.isoformat()}).json()
    )

    first_items = [plan["items"][0] for plan in payload["plans"]]
    assert all(not item["start_datetime"].endswith("T00:00:00") for item in first_items)

    db = get_test_db_session()
    try:
        persisted = db.query(SchedulePlan).filter(SchedulePlan.date == target_date).all()
        assert len(persisted) == 3
        assert {plan.plan_type for plan in persisted} == {"conservative", "balanced", "aggressive"}
        assert all(len(plan.items) == 1 for plan in persisted)
    finally:
        db.close()


def test_schedule_select_marks_only_one_plan_selected(client: TestClient) -> None:
    target_date = date(2026, 4, 26)
    client.post(
        "/api/v1/tasks",
        json={"title": "Focused work", "estimated_minutes": 30, "cognitive_load": 5},
    )
    client.post("/api/v1/schedules/generate", json={"date": target_date.isoformat()})

    selected = assert_success_envelope(
        client.post(
            "/api/v1/schedules/select",
            json={"date": target_date.isoformat(), "plan_type": "balanced"},
        ).json()
    )
    assert selected == {"date": target_date.isoformat(), "plan_type": "balanced", "selected": True}

    db = get_test_db_session()
    try:
        persisted = db.query(SchedulePlan).filter(SchedulePlan.date == target_date).all()
        assert [plan.plan_type for plan in persisted if plan.selected] == ["balanced"]
    finally:
        db.close()


def test_schedule_generate_returns_validation_error_for_dependency_cycle(client: TestClient) -> None:
    target_date = date(2026, 4, 26)
    first = assert_success_envelope(
        client.post(
            "/api/v1/tasks",
            json={"title": "First", "estimated_minutes": 30, "cognitive_load": 5},
        ).json()
    )
    second = assert_success_envelope(
        client.post(
            "/api/v1/tasks",
            json={"title": "Second", "estimated_minutes": 30, "cognitive_load": 5},
        ).json()
    )

    db = get_test_db_session()
    try:
        db.add_all(
            [
                TaskDependency(task_id=first["id"], depends_on_task_id=second["id"]),
                TaskDependency(task_id=second["id"], depends_on_task_id=first["id"]),
            ]
        )
        db.commit()
    finally:
        db.close()

    response = client.post("/api/v1/schedules/generate", json={"date": target_date.isoformat()})
    payload = response.json()

    assert response.status_code == 400
    assert payload["status"] == "error"
    assert payload["error"]["code"] == "invalid_schedule_input"
