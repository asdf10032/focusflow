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


def test_generated_schedules_include_deterministic_plan_explanations(client: TestClient) -> None:
    target_date = date(2026, 4, 29)
    create_task(client, "Explain this plan", 30)

    payload = assert_success_envelope(
        client.post("/api/v1/schedules/generate", json={"date": target_date.isoformat()}).json()
    )

    assert payload["unplaced_reasons"] == []
    for plan in payload["plans"]:
        assert plan["summary"]
        assert plan["risk_explanation"]
        assert plan["plan_type"] in plan["summary"]
        assert plan["risk_level"] in plan["risk_explanation"]


def test_blocked_day_returns_unplaced_reasons_and_high_risk_explanation(client: TestClient) -> None:
    target_date = date(2026, 4, 29)
    task = create_task(client, "Cannot fit", 30)
    db = get_test_db_session()
    try:
        db.add(
            BlockedTime(
                date=target_date,
                start_minute_of_day=0,
                end_minute_of_day=1440,
                category="blocked",
            )
        )
        db.commit()
    finally:
        db.close()

    payload = assert_success_envelope(
        client.post("/api/v1/schedules/generate", json={"date": target_date.isoformat()}).json()
    )

    assert payload["unplaced"] == [task["id"]]
    assert payload["unplaced_reasons"] == [
        {
            "task_id": task["id"],
            "reason": "blocked_time",
            "message": "Task could not be scheduled because the day has no open time.",
        }
    ]
    assert all(plan["risk_level"] == "high" for plan in payload["plans"])
    assert all("high" in plan["risk_explanation"] for plan in payload["plans"])
