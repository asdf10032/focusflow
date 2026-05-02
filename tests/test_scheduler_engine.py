from __future__ import annotations

from datetime import date
from typing import Iterator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from backend.app.db.base import Base
from backend.app.models.blocked_time import BlockedTime
from backend.app.models.task import Task
from backend.app.models.task_dependency import TaskDependency
from backend.app.services.scheduler.engine import generate_plans


@pytest.fixture()
def db() -> Iterator[Session]:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        future=True,
    )
    TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


def add_task(db: Session, title: str, minutes: int = 30, load: int = 5) -> Task:
    task = Task(title=title, estimated_minutes=minutes, cognitive_load=load, status="todo")
    db.add(task)
    db.flush()
    return task


def test_dependency_order_places_prerequisite_before_dependent(db: Session) -> None:
    dependent = add_task(db, "Write proposal", load=2)
    prerequisite = add_task(db, "Read source material", load=9)
    db.add(TaskDependency(task_id=dependent.id, depends_on_task_id=prerequisite.id))
    db.commit()

    plans, unplaced, warnings = generate_plans(db, date(2026, 4, 26))

    assert unplaced == []
    assert warnings == []
    for plan in plans:
        ordered_task_ids = [item.task_id for item in plan.items]
        assert ordered_task_ids.index(prerequisite.id) < ordered_task_ids.index(dependent.id)


def test_cycle_dependency_raises_scheduler_error(db: Session) -> None:
    first = add_task(db, "First")
    second = add_task(db, "Second")
    db.add_all(
        [
            TaskDependency(task_id=first.id, depends_on_task_id=second.id),
            TaskDependency(task_id=second.id, depends_on_task_id=first.id),
        ]
    )
    db.commit()

    with pytest.raises(ValueError, match="cycle"):
        generate_plans(db, date(2026, 4, 26))


def test_full_day_blocked_reports_unplaced_and_high_risk(db: Session) -> None:
    target_date = date(2026, 4, 26)
    task = add_task(db, "Impossible task")
    db.add(
        BlockedTime(
            date=target_date,
            start_minute_of_day=0,
            end_minute_of_day=1440,
            category="sleep",
        )
    )
    db.commit()

    plans, unplaced, warnings = generate_plans(db, target_date)

    assert unplaced == [task.id]
    assert warnings == [f"Task {task.id} could not be scheduled on {target_date.isoformat()}."]
    assert all(plan.risk_level == "high" for plan in plans)
    assert all(plan.score == 0 for plan in plans)
