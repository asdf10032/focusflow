# -*- coding: utf-8 -*-
from __future__ import annotations

import argparse
import os
from datetime import date as dt_date, datetime, time
from typing import Any

from sqlalchemy.orm import Session

from ...db.session import DATABASE_URL, SessionLocal
from ...models.blocked_time import BlockedTime
from ...models.project import Project
from ...models.schedule_plan import SchedulePlan
from ...models.task import Task
from ...schemas.schedule import GenerateResponse
from ..scheduler.engine import generate_plans
from ..scheduler.persistence import replace_persisted_plans
from .energy_templates import seed_default_templates

DEMO_PROJECT_NAME = "FocusFlow Demo"
DEMO_BLOCKED_NOTE = "Demo lunch and reset"


def _at(d: dt_date, hour: int, minute: int = 0) -> datetime:
    return datetime.combine(d, time(hour=hour, minute=minute))


def _first_project(db: Session) -> Project | None:
    return db.query(Project).filter(Project.name == DEMO_PROJECT_NAME).order_by(Project.id.asc()).first()


def _upsert_demo_project(db: Session) -> Project:
    project = _first_project(db)
    if project is None:
        project = Project(name=DEMO_PROJECT_NAME, priority=8)
        db.add(project)
        db.flush()
    else:
        project.priority = 8
    return project


def _upsert_task(db: Session, project: Project, values: dict[str, Any]) -> Task:
    task = (
        db.query(Task)
        .filter(Task.project_id == project.id, Task.title == values["title"])
        .order_by(Task.id.asc())
        .first()
    )
    if task is None:
        task = Task(project_id=project.id, **values)
        db.add(task)
        db.flush()
        return task

    for key, value in values.items():
        setattr(task, key, value)
    task.project_id = project.id
    return task


def _upsert_blocked_time(db: Session, target_date: dt_date) -> BlockedTime:
    blocked = (
        db.query(BlockedTime)
        .filter(BlockedTime.date == target_date, BlockedTime.note == DEMO_BLOCKED_NOTE)
        .order_by(BlockedTime.id.asc())
        .first()
    )
    if blocked is None:
        blocked = BlockedTime(date=target_date, start_minute_of_day=720, end_minute_of_day=780, category="custom")
        db.add(blocked)
    blocked.start_minute_of_day = 720
    blocked.end_minute_of_day = 780
    blocked.category = "custom"
    blocked.note = DEMO_BLOCKED_NOTE
    return blocked


def _select_balanced_plan(db: Session, target_date: dt_date) -> None:
    plans = db.query(SchedulePlan).filter(SchedulePlan.date == target_date).all()
    for plan in plans:
        plan.selected = plan.plan_type == "balanced"
    db.commit()


def seed_demo_data(db: Session, target_date: dt_date | None = None) -> dict[str, Any]:
    d = target_date or dt_date.today()
    seed_default_templates(db)

    project = _upsert_demo_project(db)
    task_values = [
        {
            "title": "Review thesis outline",
            "estimated_minutes": 60,
            "cognitive_load": 7,
            "due_at": _at(d, 17),
            "earliest_start_at": None,
            "fixed_start_at": None,
            "is_splittable": False,
            "max_split_count": 1,
            "status": "todo",
        },
        {
            "title": "Practice demo walkthrough",
            "estimated_minutes": 45,
            "cognitive_load": 5,
            "due_at": _at(d, 19),
            "earliest_start_at": None,
            "fixed_start_at": None,
            "is_splittable": False,
            "max_split_count": 1,
            "status": "todo",
        },
        {
            "title": "Polish FocusFlow README",
            "estimated_minutes": 90,
            "cognitive_load": 6,
            "due_at": _at(d, 20),
            "earliest_start_at": None,
            "fixed_start_at": None,
            "is_splittable": True,
            "max_split_count": 3,
            "status": "in_progress",
        },
        {
            "title": "Prepare slide talking points",
            "estimated_minutes": 30,
            "cognitive_load": 4,
            "due_at": _at(d, 16),
            "earliest_start_at": None,
            "fixed_start_at": None,
            "is_splittable": False,
            "max_split_count": 1,
            "status": "todo",
        },
        {
            "title": "Archive yesterday notes",
            "estimated_minutes": 30,
            "cognitive_load": 2,
            "due_at": None,
            "earliest_start_at": None,
            "fixed_start_at": None,
            "is_splittable": False,
            "max_split_count": 1,
            "status": "todo",
        },
    ]
    tasks = [_upsert_task(db, project, values) for values in task_values]
    _upsert_blocked_time(db, d)
    db.commit()

    plans, unplaced, warnings = generate_plans(db, d)
    response = GenerateResponse(plans=plans, unplaced=unplaced, warnings=warnings)
    replace_persisted_plans(db, d, response)
    _select_balanced_plan(db, d)

    return {
        "date": d.isoformat(),
        "project_id": project.id,
        "task_ids": [task.id for task in tasks],
        "plan_types": [plan.plan_type for plan in plans],
        "selected_plan_type": "balanced",
        "unplaced": unplaced,
        "warnings": warnings,
    }


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Seed repeatable FocusFlow demo data.")
    parser.add_argument("--date", help="Demo date in YYYY-MM-DD format. Defaults to today.")
    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    target_date = dt_date.fromisoformat(args.date) if args.date else None
    if DATABASE_URL.startswith("sqlite"):
        os.makedirs("data", exist_ok=True)

    session = SessionLocal()
    try:
        result = seed_demo_data(session, target_date=target_date)
        print(f"[seed] demo data ready for {result['date']} with {len(result['task_ids'])} tasks.")
    finally:
        session.close()
