# -*- coding: utf-8 -*-
"""调度相关的响应/请求模型。"""
from __future__ import annotations
from datetime import date as dt_date, datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class ScheduleItemOut(BaseModel):
    """单个任务的排期片段。"""
    task_id: int
    start_datetime: datetime
    end_datetime: datetime
    segment_index: Optional[int] = None
    warning: Optional[str] = None


class SchedulePlanOut(BaseModel):
    """排期方案（内存生成版）。"""
    date: dt_date
    plan_type: str  # conservative/balanced/aggressive
    score: Optional[float] = None
    risk_level: Optional[str] = None
    items: List[ScheduleItemOut] = Field(default_factory=list)


class GenerateRequest(BaseModel):
    """生成请求：默认使用今天。"""
    date: Optional[dt_date] = None


class GenerateResponse(BaseModel):
    plans: List[SchedulePlanOut]
    unplaced: List[int] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)


class SelectRequest(BaseModel):
    date: dt_date
    plan_type: str


class ValidateMoveRequest(BaseModel):
    date: dt_date
    plan_type: str
    task_id: int
    start_datetime: datetime
    end_datetime: datetime
    segment_index: Optional[int] = None


class ReoptimizeRequest(BaseModel):
    date: dt_date
