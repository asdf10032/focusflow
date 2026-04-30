# -*- coding: utf-8 -*-
from __future__ import annotations

from datetime import date as dt_date
from typing import Any, Dict

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ....core.response import success
from ....db.session import get_db
from ....services.export_data import export_daily_review, export_execution_history, export_tasks

router = APIRouter()


@router.get("/exports/tasks", summary="Export tasks as JSON")
def export_tasks_endpoint(db: Session = Depends(get_db)) -> Dict[str, Any]:
    return success(export_tasks(db))


@router.get("/exports/execution-history", summary="Export execution history as JSON")
def export_execution_history_endpoint(
    date: dt_date | None = Query(default=None),
    start_date: dt_date | None = Query(default=None),
    end_date: dt_date | None = Query(default=None),
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    return success(
        export_execution_history(
            db,
            date=date,
            start_date=start_date,
            end_date=end_date,
        )
    )


@router.get("/exports/daily-review", summary="Export daily review as CSV")
def export_daily_review_endpoint(
    date: dt_date | None = Query(default=None),
    start_date: dt_date | None = Query(default=None),
    end_date: dt_date | None = Query(default=None),
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    return success(
        export_daily_review(
            db,
            date=date,
            start_date=start_date,
            end_date=end_date,
        )
    )

