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
from backend.app.models.blocked_time import BlockedTime
from backend.app.models.execution_log import ExecutionLog
from backend.app.models.schedule_plan import SchedulePlan


@pytest.fixture()
def env() -> Iterator[tuple[TestClient, sessionmaker[Session]]]:
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
            yield test_client, TestingSessionLocal
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


def partial_replan(client: TestClient, target_date: date):
    return client.post("/api/v1/schedules/partial-replan", json={"date": target_date.isoformat()})


def unique_task_ids(plan: dict) -> list[int]:
    seen: set[int] = set()
    ordered: list[int] = []
    for item in plan["items"]:
        if item["task_id"] in seen:
            continue
        seen.add(item["task_id"])
        ordered.append(item["task_id"])
    return ordered


def test_partial_replan_requires_selected_plan(env: tuple[TestClient, sessionmaker[Session]]) -> None:
    client, _ = env
    target_date = date(2026, 5, 1)
    create_task(client, "Needs a selected plan")

    response = partial_replan(client, target_date)

    assert response.status_code == 400
    assert_error_envelope(response.json(), "missing_selected_plan")


def test_partial_replan_excludes_same_day_feedbacked_tasks(
    env: tuple[TestClient, sessionmaker[Session]],
) -> None:
    client, _ = env
    target_date = date(2026, 5, 1)
    done = create_task(client, "Already done")
    skipped = create_task(client, "Skipped today")
    canceled = create_task(client, "Canceled today")
    incomplete = create_task(client, "Still in progress")
    remaining = create_task(client, "Remaining work")
    generate_and_select(client, target_date)

    for task, status in [
        (done, "done"),
        (skipped, "skipped"),
        (canceled, "canceled"),
        (incomplete, "in_progress"),
    ]:
        assert_success_envelope(
            client.post(
                "/api/v1/execution/feedback",
                json={"task_id": task["id"], "status": status, "date": target_date.isoformat()},
            ).json()
        )

    payload = assert_success_envelope(partial_replan(client, target_date).json())

    assert [plan["plan_type"] for plan in payload["plans"]] == [
        "conservative",
        "balanced",
        "aggressive",
    ]
    for plan in payload["plans"]:
        assert unique_task_ids(plan) == [remaining["id"]]


def test_partial_replan_excludes_done_and_canceled_task_status_without_same_day_log(
    env: tuple[TestClient, sessionmaker[Session]],
) -> None:
    client, _ = env
    target_date = date(2026, 5, 1)
    done = create_task(client, "Status done")
    canceled = create_task(client, "Status canceled")
    remaining = create_task(client, "Status todo")
    generate_and_select(client, target_date)

    assert_success_envelope(client.put(f"/api/v1/tasks/{done['id']}", json={"status": "done"}).json())
    assert_success_envelope(
        client.put(f"/api/v1/tasks/{canceled['id']}", json={"status": "canceled"}).json()
    )

    payload = assert_success_envelope(partial_replan(client, target_date).json())

    for plan in payload["plans"]:
        assert unique_task_ids(plan) == [remaining["id"]]


def test_partial_replan_replaces_plans_clears_selection_and_preserves_logs(
    env: tuple[TestClient, sessionmaker[Session]],
) -> None:
    client, SessionLocal = env
    target_date = date(2026, 5, 1)
    completed = create_task(client, "Completed first")
    remaining = create_task(client, "Plan the remainder")
    generate_and_select(client, target_date)
    assert_success_envelope(
        client.post(
            "/api/v1/execution/feedback",
            json={"task_id": completed["id"], "status": "done", "date": target_date.isoformat()},
        ).json()
    )

    payload = assert_success_envelope(partial_replan(client, target_date).json())

    assert payload["unplaced"] == []
    assert payload["warnings"] == []
    assert unique_task_ids(next(plan for plan in payload["plans"] if plan["plan_type"] == "balanced")) == [
        remaining["id"]
    ]
    with SessionLocal() as db:
        persisted = db.query(SchedulePlan).filter(SchedulePlan.date == target_date).all()
        logs = db.query(ExecutionLog).filter(ExecutionLog.date == target_date).all()
        assert len(persisted) == 3
        assert not any(plan.selected for plan in persisted)
        assert len(logs) == 1
        assert logs[0].task_id == completed["id"]


def test_partial_replan_returns_no_remaining_work_without_mutating_plans(
    env: tuple[TestClient, sessionmaker[Session]],
) -> None:
    client, SessionLocal = env
    target_date = date(2026, 5, 1)
    task = create_task(client, "Nothing left")
    generate_and_select(client, target_date)
    assert_success_envelope(
        client.post(
            "/api/v1/execution/feedback",
            json={"task_id": task["id"], "status": "done", "date": target_date.isoformat()},
        ).json()
    )

    response = partial_replan(client, target_date)

    assert response.status_code == 400
    assert_error_envelope(response.json(), "no_remaining_work")
    with SessionLocal() as db:
        persisted = db.query(SchedulePlan).filter(SchedulePlan.date == target_date).all()
        assert len(persisted) == 3
        assert sum(1 for plan in persisted if plan.selected) == 1


def test_partial_replan_returns_no_schedulable_time_without_mutating_plans(
    env: tuple[TestClient, sessionmaker[Session]],
) -> None:
    client, SessionLocal = env
    target_date = date(2026, 5, 1)
    completed = create_task(client, "Done before block")
    create_task(client, "Cannot fit now")
    generate_and_select(client, target_date)
    assert_success_envelope(
        client.post(
            "/api/v1/execution/feedback",
            json={"task_id": completed["id"], "status": "done", "date": target_date.isoformat()},
        ).json()
    )
    with SessionLocal() as db:
        db.add(
            BlockedTime(
                date=target_date,
                start_minute_of_day=0,
                end_minute_of_day=24 * 60,
                category="custom",
                note="No remaining capacity",
            )
        )
        db.commit()

    response = partial_replan(client, target_date)

    assert response.status_code == 400
    assert_error_envelope(response.json(), "no_schedulable_time")
    with SessionLocal() as db:
        persisted = db.query(SchedulePlan).filter(SchedulePlan.date == target_date).all()
        assert len(persisted) == 3
        assert sum(1 for plan in persisted if plan.selected) == 1
