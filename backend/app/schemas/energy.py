# -*- coding: utf-8 -*-
"""Energy/Blocked 的请求/响应模型。"""
from __future__ import annotations
from typing import List
from datetime import date
from pydantic import BaseModel, ConfigDict, Field


class EnergyTemplateSlotIn(BaseModel):
    slot_index: int = Field(ge=0, le=47)
    energy: int = Field(ge=0, le=100)


class EnergyTemplateOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    day_type: str
    slots: List[EnergyTemplateSlotIn]


class EnergyTemplateUpdate(BaseModel):
    slots: List[EnergyTemplateSlotIn]


class BlockedTimeCreate(BaseModel):
    date: date
    start_minute_of_day: int = Field(ge=0, le=1439)
    end_minute_of_day: int = Field(ge=1, le=1440)
    category: str
    note: str | None = None


class BlockedTimeOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    date: date
    start_minute_of_day: int
    end_minute_of_day: int
    category: str
    note: str | None
