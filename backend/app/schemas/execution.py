# -*- coding: utf-8 -*-
from __future__ import annotations

from datetime import date as dt_date, datetime

from pydantic import BaseModel, ConfigDict, Field

FeedbackInputStatus = str


class FeedbackRequest(BaseModel):
    task_id: int
    status: FeedbackInputStatus = Field(pattern="^(todo|in_progress|done|skipped|incomplete|canceled)$")
    date: dt_date | None = None
    actual_minutes: int | None = Field(default=None, ge=1, le=24 * 60)
    note: str | None = Field(default=None, max_length=1000)


class ExecutionLogOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    task_id: int
    task_title_snapshot: str
    estimated_minutes_snapshot: int
    date: dt_date
    status: str
    actual_minutes: int | None
    note: str | None
    created_at: datetime


class SelectedPlanOut(BaseModel):
    id: int
    date: dt_date
    plan_type: str
    score: float | None
    risk_level: str | None
    selected: bool


class ExecutionProgressOut(BaseModel):
    date: dt_date
    selected_plan: SelectedPlanOut | None
    planned_count: int
    completed_count: int
    skipped_incomplete_count: int
    completion_rate: float


class ExecutionReviewSummaryOut(ExecutionProgressOut):
    planned_minutes: int
    actual_minutes: int
    estimate_variance_minutes: int | None


class ExecutionReviewItemOut(BaseModel):
    id: int
    task_id: int
    task_title_snapshot: str
    estimated_minutes_snapshot: int
    date: dt_date
    status: str
    actual_minutes: int | None
    note: str | None
    created_at: datetime
    estimate_variance_minutes: int | None


class ExecutionReviewOut(BaseModel):
    date: dt_date
    selected_plan: SelectedPlanOut | None
    summary: ExecutionReviewSummaryOut
    items: list[ExecutionReviewItemOut]

