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

    task_id = today["items"][0]["task"]["id"]
    feedback = assert_success_envelope(
        client.post("/api/v1/execution/feedback", json={"task_id": task_id, "status": "done"}).json()
    )
    assert feedback["status"] == "done"

    draft = assert_success_envelope(
        client.post("/api/v1/ai/parse-task", json={"text": "Polish demo script 45min medium"}).json()
    )
    assert draft["title"] == "Polish demo script"
    assert draft["estimated_minutes"] == 45
    assert draft["cognitive_load"] == 5
