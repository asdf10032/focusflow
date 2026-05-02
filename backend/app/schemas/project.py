# -*- coding: utf-8 -*-
"""Project 的请求/响应模型。"""
from __future__ import annotations
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class ProjectCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    priority: int = Field(default=0, ge=0, le=10)


class ProjectOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    priority: int
    created_at: datetime
    updated_at: datetime
