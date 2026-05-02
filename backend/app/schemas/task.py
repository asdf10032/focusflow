# -*- coding: utf-8 -*-
"""Task 的请求/响应模型。"""
from __future__ import annotations
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=300)
    notes: str | None = Field(default=None, max_length=2000)
    estimated_minutes: int = Field(ge=1, le=8*60)
    cognitive_load: int = Field(ge=1, le=10)
    due_at: datetime | None = None
    earliest_start_at: datetime | None = None
    fixed_start_at: datetime | None = None
    is_splittable: bool = False
    max_split_count: int = Field(default=1, ge=1, le=3)
    status: str = Field(default="todo")
    project_id: int | None = None


class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=300)
    notes: str | None = Field(default=None, max_length=2000)
    estimated_minutes: int | None = Field(default=None, ge=1, le=8*60)
    cognitive_load: int | None = Field(default=None, ge=1, le=10)
    due_at: datetime | None = None
    earliest_start_at: datetime | None = None
    fixed_start_at: datetime | None = None
    is_splittable: bool | None = None
    max_split_count: int | None = Field(default=None, ge=1, le=3)
    status: str | None = None
    project_id: int | None = None


class TaskOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    notes: str | None
    estimated_minutes: int
    cognitive_load: int
    due_at: datetime | None
    earliest_start_at: datetime | None
    fixed_start_at: datetime | None
    is_splittable: bool
    max_split_count: int
    status: str
    project_id: int | None
