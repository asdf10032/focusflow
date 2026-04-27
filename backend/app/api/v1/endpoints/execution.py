# -*- coding: utf-8 -*-
from __future__ import annotations

from datetime import date as dt_date
from typing import Any, Dict

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from ....core.errors import AppError
from ....core.response import success
from ....db.session import get_db
from ....models.schedule_plan import SchedulePlan
from ....models.task import Task
from ....schemas.task import TaskOut

router = APIRouter()


class FeedbackRequest(BaseModel):
    task_id: int
    status: str = Field(pattern="^(todo|in_progress|done|canceled)$")


def _task_data(task: Task) -> dict[str, Any]:
    return TaskOut.model_validate(task).model_dump(mode="json")


def _selected_plan_data(plan: SchedulePlan) -> dict[str, Any]:
    return {
        "id": plan.id,
        "date": plan.date.isoformat(),
        "plan_type": plan.plan_type,
        "score": plan.score,
        "risk_level": plan.risk_level,
        "selected": plan.selected,
    }


@router.get("/execution/today", summary="Get selected work for a day")
def execution_today(date: dt_date = Query(...), db: Session = Depends(get_db)) -> Dict[str, Any]:
    plan = (
        db.query(SchedulePlan)
        .filter(SchedulePlan.date == date, SchedulePlan.selected.is_(True))
        .one_or_none()
    )
    if plan is None:
        return success({"date": date.isoformat(), "selected_plan": None, "items": []})

    task_ids = [item.task_id for item in plan.items]
    tasks = db.query(Task).filter(Task.id.in_(task_ids)).all() if task_ids else []
    tasks_by_id = {task.id: task for task in tasks}

    items = []
    for item in sorted(plan.items, key=lambda row: (row.start_datetime, row.id)):
        task = tasks_by_id.get(item.task_id)
        if task is None:
            continue
        items.append(
            {
                "task_id": item.task_id,
                "start_datetime": item.start_datetime.isoformat(),
                "end_datetime": item.end_datetime.isoformat(),
                "segment_index": item.segment_index,
                "warning": item.warning,
                "task": _task_data(task),
            }
        )

    return success({"date": date.isoformat(), "selected_plan": _selected_plan_data(plan), "items": items})


@router.post("/execution/feedback", summary="Submit execution feedback")
def execution_feedback(payload: FeedbackRequest, db: Session = Depends(get_db)) -> Dict[str, Any]:
    task = db.get(Task, payload.task_id)
    if task is None:
        raise AppError(code="not_found", message="Task not found", status_code=404)

    task.status = payload.status
    db.commit()
    db.refresh(task)
    return success(_task_data(task))
