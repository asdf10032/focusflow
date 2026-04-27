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
from ....models.schedule_item import ScheduleItem
from ....models.schedule_plan import SchedulePlan
from ....models.task import Task
from ....schemas.schedule import (
    GenerateRequest,
    GenerateResponse,
    ReoptimizeRequest,
    SelectRequest,
    ValidateMoveRequest,
)
from ....services.scheduler.engine import generate_plans

router = APIRouter()


def _replace_persisted_plans(db: Session, d: dt_date, response: GenerateResponse) -> None:
    existing = db.query(SchedulePlan).filter(SchedulePlan.date == d).all()
    for plan in existing:
        db.delete(plan)
    db.flush()

    for plan_out in response.plans:
        plan = SchedulePlan(
            date=d,
            plan_type=plan_out.plan_type,
            score=plan_out.score,
            risk_level=plan_out.risk_level,
            selected=False,
        )
        db.add(plan)
        db.flush()

        for item_out in plan_out.items:
            plan.items.append(
                ScheduleItem(
                    task_id=item_out.task_id,
                    start_datetime=item_out.start_datetime,
                    end_datetime=item_out.end_datetime,
                    segment_index=item_out.segment_index or 0,
                    warning=item_out.warning,
                )
            )
    db.commit()


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


@router.post("/schedules/generate", summary="Generate three daily schedule plans")
def schedules_generate(payload: GenerateRequest, db: Session = Depends(get_db)) -> Dict[str, Any]:
    d: dt_date = payload.date or dt_date.today()
    try:
        plans, unplaced, warnings = generate_plans(db, d)
    except ValueError as exc:
        raise AppError(code="invalid_schedule_input", message=str(exc), status_code=400) from exc
    response = GenerateResponse(plans=plans, unplaced=unplaced, warnings=warnings)
    _replace_persisted_plans(db, d, response)
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
    response = GenerateResponse(plans=plans, unplaced=unplaced, warnings=warnings)
    _replace_persisted_plans(db, payload.date, response)
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
