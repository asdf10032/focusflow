# -*- coding: utf-8 -*-
from __future__ import annotations

import csv
import io
import json
from datetime import date as dt_date
from typing import Any

from sqlalchemy.orm import Session

from ..core.errors import AppError
from ..models.execution_log import ExecutionLog
from ..models.project import Project
from ..models.task import Task
from ..schemas.export import ExportPayload
from ..schemas.task import TaskOut


JSON_CONTENT_TYPE = "application/json"
CSV_CONTENT_TYPE = "text/csv"


def _date_label(date: dt_date | None, start_date: dt_date | None, end_date: dt_date | None) -> str:
    if date is not None:
        return date.isoformat()
    if start_date is not None and end_date is not None:
        return f"{start_date.isoformat()}-to-{end_date.isoformat()}"
    raise AppError(
        code="invalid_request",
        message="Provide either date or both start_date and end_date",
        status_code=400,
    )


def _resolve_range(
    date: dt_date | None,
    start_date: dt_date | None,
    end_date: dt_date | None,
) -> tuple[dt_date, dt_date, str]:
    label = _date_label(date, start_date, end_date)
    if date is not None:
        if start_date is not None or end_date is not None:
            raise AppError(
                code="invalid_request",
                message="Use either date or start_date/end_date, not both",
                status_code=400,
            )
        return date, date, label
    if start_date is None or end_date is None:
        raise AppError(
            code="invalid_request",
            message="Provide either date or both start_date and end_date",
            status_code=400,
        )
    if start_date > end_date:
        raise AppError(
            code="invalid_date_range",
            message="start_date must be before or equal to end_date",
            status_code=400,
        )
    return start_date, end_date, label


def _json_payload(filename: str, data: Any, record_count: int) -> dict[str, Any]:
    payload = ExportPayload(
        filename=filename,
        content_type=JSON_CONTENT_TYPE,
        content=json.dumps(data, ensure_ascii=False, sort_keys=True, indent=2),
        record_count=record_count,
    )
    return payload.model_dump(mode="json")


def _csv_payload(filename: str, rows: list[dict[str, Any]], fieldnames: list[str]) -> dict[str, Any]:
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=fieldnames, lineterminator="\n")
    writer.writeheader()
    for row in rows:
        writer.writerow(row)
    payload = ExportPayload(
        filename=filename,
        content_type=CSV_CONTENT_TYPE,
        content=output.getvalue(),
        record_count=len(rows),
    )
    return payload.model_dump(mode="json")


def export_tasks(db: Session) -> dict[str, Any]:
    projects = db.query(Project).all()
    projects_by_id = {project.id: project for project in projects}
    tasks = db.query(Task).order_by(Task.id.asc()).all()
    data = []
    for task in tasks:
        item = TaskOut.model_validate(task).model_dump(mode="json")
        project = projects_by_id.get(task.project_id)
        item["project_name"] = project.name if project is not None else None
        item["project_priority"] = project.priority if project is not None else None
        data.append(item)
    return _json_payload("focusflow-tasks.json", data, len(data))


def _logs_in_range(db: Session, start_date: dt_date, end_date: dt_date) -> list[ExecutionLog]:
    return (
        db.query(ExecutionLog)
        .filter(ExecutionLog.date >= start_date, ExecutionLog.date <= end_date)
        .order_by(ExecutionLog.date.asc(), ExecutionLog.created_at.asc(), ExecutionLog.id.asc())
        .all()
    )


def _execution_log_data(log: ExecutionLog) -> dict[str, Any]:
    return {
        "id": log.id,
        "task_id": log.task_id,
        "task_title_snapshot": log.task_title_snapshot,
        "estimated_minutes_snapshot": log.estimated_minutes_snapshot,
        "task_project_id_snapshot": log.task_project_id_snapshot,
        "cognitive_load_snapshot": log.cognitive_load_snapshot,
        "date": log.date.isoformat(),
        "status": log.status,
        "actual_minutes": log.actual_minutes,
        "note": log.note,
        "created_at": log.created_at.isoformat(),
    }


def export_execution_history(
    db: Session,
    *,
    date: dt_date | None = None,
    start_date: dt_date | None = None,
    end_date: dt_date | None = None,
) -> dict[str, Any]:
    resolved_start, resolved_end, label = _resolve_range(date, start_date, end_date)
    logs = _logs_in_range(db, resolved_start, resolved_end)
    data = [_execution_log_data(log) for log in logs]
    return _json_payload(f"focusflow-execution-history-{label}.json", data, len(data))


def _review_row(log: ExecutionLog) -> dict[str, Any]:
    variance = ""
    if log.actual_minutes is not None:
        variance = log.actual_minutes - log.estimated_minutes_snapshot
    return {
        "date": log.date.isoformat(),
        "task_id": log.task_id,
        "task_title": log.task_title_snapshot,
        "status": log.status,
        "estimated_minutes": log.estimated_minutes_snapshot,
        "actual_minutes": log.actual_minutes if log.actual_minutes is not None else "",
        "estimate_variance_minutes": variance,
        "note": log.note or "",
    }


def export_daily_review(
    db: Session,
    *,
    date: dt_date | None = None,
    start_date: dt_date | None = None,
    end_date: dt_date | None = None,
) -> dict[str, Any]:
    resolved_start, resolved_end, label = _resolve_range(date, start_date, end_date)
    logs = _logs_in_range(db, resolved_start, resolved_end)
    rows = [_review_row(log) for log in logs]
    return _csv_payload(
        f"focusflow-daily-review-{label}.csv",
        rows,
        [
            "date",
            "task_id",
            "task_title",
            "status",
            "estimated_minutes",
            "actual_minutes",
            "estimate_variance_minutes",
            "note",
        ],
    )

