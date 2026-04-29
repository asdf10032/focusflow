# -*- coding: utf-8 -*-
from __future__ import annotations

from pydantic import BaseModel, Field


class ParseTaskRequest(BaseModel):
    text: str = Field(min_length=1, max_length=1000)


class DurationSuggestionRequest(BaseModel):
    title: str = Field(min_length=1, max_length=300)
    project_id: int | None = None
    cognitive_load: int | None = Field(default=None, ge=1, le=10)
    estimated_minutes: int | None = Field(default=None, ge=1, le=8 * 60)


class DurationSuggestionOut(BaseModel):
    suggested_minutes: int
    confidence: str
    sample_count: int
    source: str
    reason_code: str
    reason: str
