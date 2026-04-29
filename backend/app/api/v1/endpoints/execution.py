# -*- coding: utf-8 -*-
from __future__ import annotations

from datetime import date as dt_date
from typing import Any, Dict

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ....core.errors import AppError
from ....core.response import success
from ....db.session import get_db
from ....models.execution_log import ExecutionLog
from ....models.schedule_plan import SchedulePlan
from ....models.task import Task
from ....schemas.execution import (
    ExecutionLogOut,
    ExecutionProgressOut,
    ExecutionReviewItemOut,
    ExecutionReviewOut,
    ExecutionReviewSummaryOut,
    FeedbackRequest,
)
from ....schemas.task import TaskOut

router = APIRouter()


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


def _selected_plan_for_date(db: Session, date: dt_date) -> SchedulePlan | None:
    return (
        db.query(SchedulePlan)
        .filter(SchedulePlan.date == date, SchedulePlan.selected.is_(True))
        .one_or_none()
    )


def _normalize_feedback_status(status: str) -> str:
    if status in {"todo", "in_progress"}:
        return "incomplete"
    return status


def _task_status_from_feedback(status: str) -> str:
    return {
        "done": "done",
        "skipped": "todo",
        "incomplete": "in_progress",
        "canceled": "canceled",
        "todo": "todo",
        "in_progress": "in_progress",
    }[status]


def _log_data(log: ExecutionLog) -> dict[str, Any]:
    return ExecutionLogOut.model_validate(log).model_dump(mode="json")


def _logs_for_date(db: Session, date: dt_date) -> list[ExecutionLog]:
    return (
        db.query(ExecutionLog)
        .filter(ExecutionLog.date == date)
        .order_by(ExecutionLog.created_at.asc(), ExecutionLog.id.asc())
        .all()
    )


def _planned_task_ids(plan: SchedulePlan | None) -> list[int]:
    if plan is None:
        return []
    ordered_ids: list[int] = []
    seen: set[int] = set()
    for item in sorted(plan.items, key=lambda row: (row.start_datetime, row.id)):
        if item.task_id in seen:
            continue
        seen.add(item.task_id)
        ordered_ids.append(item.task_id)
    return ordered_ids


def _planned_minutes(plan: SchedulePlan | None, logs: list[ExecutionLog]) -> int:
    if logs:
        return sum(log.estimated_minutes_snapshot for log in logs)
    if plan is not None:
        return sum(
            int((item.end_datetime - item.start_datetime).total_seconds() // 60)
            for item in plan.items
        )
    return 0


def _latest_logs_by_task(logs: list[ExecutionLog]) -> dict[int, ExecutionLog]:
    latest: dict[int, ExecutionLog] = {}
    for log in logs:
        latest[log.task_id] = log
    return latest


def _progress_payload(date: dt_date, plan: SchedulePlan | None, logs: list[ExecutionLog]) -> dict[str, Any]:
    planned_ids = _planned_task_ids(plan)
    latest_by_task = _latest_logs_by_task(logs)
    completed_count = sum(
        1
        for task_id in planned_ids
        if latest_by_task.get(task_id) is not None and latest_by_task[task_id].status == "done"
    )
    planned_count = len(planned_ids)
    skipped_incomplete_count = max(planned_count - completed_count, 0)
    completion_rate = completed_count / planned_count if planned_count else 0.0
    payload = ExecutionProgressOut(
        date=date,
        selected_plan=_selected_plan_data(plan) if plan is not None else None,
        planned_count=planned_count,
        completed_count=completed_count,
        skipped_incomplete_count=skipped_incomplete_count,
        completion_rate=completion_rate,
    )
    return payload.model_dump(mode="json")


def _review_item_payload(log: ExecutionLog) -> dict[str, Any]:
    variance = None
    if log.actual_minutes is not None:
        variance = log.actual_minutes - log.estimated_minutes_snapshot
    return ExecutionReviewItemOut(
        id=log.id,
        task_id=log.task_id,
        task_title_snapshot=log.task_title_snapshot,
        estimated_minutes_snapshot=log.estimated_minutes_snapshot,
        date=log.date,
        status=log.status,
        actual_minutes=log.actual_minutes,
        note=log.note,
        created_at=log.created_at,
        estimate_variance_minutes=variance,
    ).model_dump(mode="json")


def _review_payload(date: dt_date, plan: SchedulePlan | None, logs: list[ExecutionLog]) -> dict[str, Any]:
    progress = _progress_payload(date, plan, logs)
    planned_minutes = _planned_minutes(plan, logs)
    actual_minutes = sum(log.actual_minutes for log in logs if log.actual_minutes is not None)
    estimate_variance = actual_minutes - planned_minutes if logs else None
    summary = ExecutionReviewSummaryOut(
        **progress,
        planned_minutes=planned_minutes,
        actual_minutes=actual_minutes,
        estimate_variance_minutes=estimate_variance,
    ).model_dump(mode="json")
    return ExecutionReviewOut(
        date=date,
        selected_plan=progress["selected_plan"],
        summary=summary,
        items=[_review_item_payload(log) for log in logs],
    ).model_dump(mode="json")


@router.get("/execution/today", summary="Get selected work for a day")
def execution_today(date: dt_date = Query(...), db: Session = Depends(get_db)) -> Dict[str, Any]:
    plan = _selected_plan_for_date(db, date)
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

    log = ExecutionLog(
        task_id=task.id,
        task_title_snapshot=task.title,
        estimated_minutes_snapshot=task.estimated_minutes,
        date=payload.date or dt_date.today(),
        status=_normalize_feedback_status(payload.status),
        actual_minutes=payload.actual_minutes,
        note=payload.note,
    )
    db.add(log)
    task.status = _task_status_from_feedback(payload.status)
    db.commit()
    db.refresh(task)
    return success(_task_data(task))


@router.get("/execution/history", summary="Get execution history for a day")
def execution_history(date: dt_date = Query(...), db: Session = Depends(get_db)) -> Dict[str, Any]:
    logs = _logs_for_date(db, date)
    return success([_log_data(log) for log in logs])


@router.get("/execution/progress", summary="Get execution progress for a day")
def execution_progress(date: dt_date = Query(...), db: Session = Depends(get_db)) -> Dict[str, Any]:
    plan = _selected_plan_for_date(db, date)
    logs = _logs_for_date(db, date)
    return success(_progress_payload(date, plan, logs))


@router.get("/execution/review", summary="Get daily execution review")
def execution_review(date: dt_date = Query(...), db: Session = Depends(get_db)) -> Dict[str, Any]:
    plan = _selected_plan_for_date(db, date)
    logs = _logs_for_date(db, date)
    return success(_review_payload(date, plan, logs))
