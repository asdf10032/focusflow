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

