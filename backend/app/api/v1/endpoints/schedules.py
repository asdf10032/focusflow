# -*- coding: utf-8 -*-
from __future__ import annotations

from datetime import date as dt_date, datetime
from typing import Any, Dict

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ....core.errors import AppError
from ....core.response import success
from ....db.session import get_db
from ....models.blocked_time import BlockedTime
from ....models.execution_log import ExecutionLog
from ....models.schedule_item import ScheduleItem
from ....models.schedule_plan import SchedulePlan
from ....models.task import Task
from ....schemas.schedule import (
    GenerateRequest,
    GenerateResponse,
    PartialReplanRequest,
    ReoptimizeRequest,
    SelectRequest,
    UnplacedReasonOut,
    ValidateMoveRequest,
)
from ....services.scheduler.engine import generate_plans
from ....services.scheduler.persistence import replace_persisted_plans

router = APIRouter()


def _overlaps(start: datetime, end: datetime, other_start: datetime, other_end: datetime) -> bool:
    return start < other_end and other_start < end


def _minute_of_day(value: datetime) -> int:
    return value.hour * 60 + value.minute


def _item_data(item: ScheduleItem) -> dict[str, Any]:
    return {
        "task_id": item.task_id,
        "start_datetime": item.start_datetime.isoformat(),
        "end_datetime": item.end_datetime.isoformat(),
        "segment_index": item.segment_index,
        "warning": item.warning,
    }


def _unplaced_reasons_for_response(plans: list[Any], unplaced: list[int]) -> list[UnplacedReasonOut]:
    if not unplaced:
        return []
    no_items = all(len(plan.items) == 0 for plan in plans)
    reason = "blocked_time" if no_items else "no_capacity"
    message = (
        "Task could not be scheduled because the day has no open time."
        if no_items
        else "Task could not be scheduled because there was not enough open time."
    )
    return [
        UnplacedReasonOut(task_id=task_id, reason=reason, message=message)
        for task_id in sorted(unplaced)
    ]


def _selected_plan_for_date(db: Session, d: dt_date) -> SchedulePlan | None:
    return (
        db.query(SchedulePlan)
        .filter(SchedulePlan.date == d, SchedulePlan.selected.is_(True))
        .one_or_none()
    )


def _selected_task_ids(plan: SchedulePlan) -> list[int]:
    ordered_ids: list[int] = []
    seen: set[int] = set()
    for item in sorted(plan.items, key=lambda row: (row.start_datetime, row.id)):
        if item.task_id in seen:
            continue
        seen.add(item.task_id)
        ordered_ids.append(item.task_id)
    return ordered_ids


def _remaining_replan_tasks(db: Session, plan: SchedulePlan, d: dt_date) -> list[Task]:
    selected_ids = _selected_task_ids(plan)
    if not selected_ids:
        return []

    feedbacked_ids = {
        row.task_id
        for row in db.query(ExecutionLog.task_id).filter(
            ExecutionLog.date == d,
            ExecutionLog.task_id.in_(selected_ids),
        )
    }
    tasks = db.query(Task).filter(Task.id.in_(selected_ids)).all()
    tasks_by_id = {task.id: task for task in tasks}

    remaining: list[Task] = []
    for task_id in selected_ids:
        task = tasks_by_id.get(task_id)
        if task is None:
            continue
        if task.id in feedbacked_ids:
            continue
        if task.status not in {"todo", "in_progress"}:
            continue
        remaining.append(task)
    return remaining


@router.post("/schedules/generate", summary="Generate three daily schedule plans")
def schedules_generate(payload: GenerateRequest, db: Session = Depends(get_db)) -> Dict[str, Any]:
    d: dt_date = payload.date or dt_date.today()
    try:
        plans, unplaced, warnings = generate_plans(db, d)
    except ValueError as exc:
        raise AppError(code="invalid_schedule_input", message=str(exc), status_code=400) from exc
    response = GenerateResponse(
        plans=plans,
        unplaced=unplaced,
        unplaced_reasons=_unplaced_reasons_for_response(plans, unplaced),
        warnings=warnings,
    )
    replace_persisted_plans(db, d, response)
    return success(response.model_dump(mode="json"))


@router.post("/schedules/validate-move", summary="Validate a proposed schedule item move")
def schedules_validate_move(payload: ValidateMoveRequest, db: Session = Depends(get_db)) -> Dict[str, Any]:
    conflicts: list[dict[str, Any]] = []
    task = db.get(Task, payload.task_id)
    plan = (
        db.query(SchedulePlan)
        .filter(SchedulePlan.date == payload.date, SchedulePlan.plan_type == payload.plan_type)
        .one_or_none()
    )

    if task is None:
        conflicts.append({"type": "missing_task", "message": "Task not found", "task_id": payload.task_id})
    if plan is None:
        conflicts.append({"type": "missing_plan", "message": "Schedule plan not found"})

    if payload.end_datetime <= payload.start_datetime:
        conflicts.append({"type": "invalid_range", "message": "End time must be after start time"})

    if plan is not None:
        for item in plan.items:
            same_segment = item.task_id == payload.task_id and item.segment_index == (payload.segment_index or 0)
            if same_segment:
                continue
            if _overlaps(payload.start_datetime, payload.end_datetime, item.start_datetime, item.end_datetime):
                conflicts.append(
                    {
                        "type": "overlap",
                        "message": "Proposed time overlaps another scheduled task",
                        "task_id": item.task_id,
                        "start_datetime": item.start_datetime.isoformat(),
                        "end_datetime": item.end_datetime.isoformat(),
                    }
                )

    blocked_rows = db.query(BlockedTime).filter(BlockedTime.date == payload.date).all()
    proposed_start = _minute_of_day(payload.start_datetime)
    proposed_end = _minute_of_day(payload.end_datetime)
    for blocked in blocked_rows:
        if proposed_start < blocked.end_minute_of_day and blocked.start_minute_of_day < proposed_end:
            conflicts.append(
                {
                    "type": "blocked_time",
                    "message": "Proposed time overlaps blocked time",
                    "start_minute_of_day": blocked.start_minute_of_day,
                    "end_minute_of_day": blocked.end_minute_of_day,
                }
            )

    return success(
        {
            "valid": len(conflicts) == 0,
            "conflicts": conflicts,
            "proposed_item": {
                "task_id": payload.task_id,
                "start_datetime": payload.start_datetime.isoformat(),
                "end_datetime": payload.end_datetime.isoformat(),
                "segment_index": payload.segment_index,
                "warning": None,
            },
        }
    )


@router.post("/schedules/reoptimize", summary="Regenerate plans after schedule changes")
def schedules_reoptimize(payload: ReoptimizeRequest, db: Session = Depends(get_db)) -> Dict[str, Any]:
    try:
        plans, unplaced, warnings = generate_plans(db, payload.date)
    except ValueError as exc:
        raise AppError(code="invalid_schedule_input", message=str(exc), status_code=400) from exc
    response = GenerateResponse(
        plans=plans,
        unplaced=unplaced,
        unplaced_reasons=_unplaced_reasons_for_response(plans, unplaced),
        warnings=warnings,
    )
    replace_persisted_plans(db, payload.date, response)
    return success(response.model_dump(mode="json"))


@router.post("/schedules/partial-replan", summary="Regenerate plans for remaining selected work")
def schedules_partial_replan(payload: PartialReplanRequest, db: Session = Depends(get_db)) -> Dict[str, Any]:
    selected_plan = _selected_plan_for_date(db, payload.date)
    if selected_plan is None:
        raise AppError(
            code="missing_selected_plan",
            message="Select a schedule plan before replanning remaining work.",
            status_code=400,
        )

    remaining_tasks = _remaining_replan_tasks(db, selected_plan, payload.date)
    if not remaining_tasks:
        raise AppError(
            code="no_remaining_work",
            message="There is no remaining selected work to replan for this date.",
            status_code=400,
        )

    try:
        plans, unplaced, warnings = generate_plans(db, payload.date, candidate_tasks=remaining_tasks)
    except ValueError as exc:
        raise AppError(code="invalid_schedule_input", message=str(exc), status_code=400) from exc

    if unplaced and all(len(plan.items) == 0 for plan in plans):
        raise AppError(
            code="no_schedulable_time",
            message="There is no schedulable time left for the remaining work.",
            status_code=400,
        )

    response = GenerateResponse(
        plans=plans,
        unplaced=unplaced,
        unplaced_reasons=_unplaced_reasons_for_response(plans, unplaced),
        warnings=warnings,
    )
    replace_persisted_plans(db, payload.date, response)
    return success(response.model_dump(mode="json"))


@router.post("/schedules/select", summary="Select a schedule plan")
def schedules_select(payload: SelectRequest, db: Session = Depends(get_db)) -> Dict[str, Any]:
    plans = db.query(SchedulePlan).filter(SchedulePlan.date == payload.date).all()
    selected_plan = next((plan for plan in plans if plan.plan_type == payload.plan_type), None)
    if selected_plan is None:
        raise AppError(code="not_found", message="Schedule plan not found", status_code=404)

    for plan in plans:
        plan.selected = plan.id == selected_plan.id
    db.commit()

    return success(
        {
            "date": payload.date,
            "plan_type": selected_plan.plan_type,
            "selected": True,
        }
    )
