# -*- coding: utf-8 -*-
from __future__ import annotations

import re
from typing import Any, Dict

from fastapi import APIRouter
from pydantic import BaseModel, Field

from ....core.response import success

router = APIRouter()

_DURATION_PATTERN = re.compile(
    r"(?P<value>\d+(?:\.\d+)?)\s*(?P<unit>小时|小時|h|hr|hrs|hour|hours|分钟|分鐘|min|mins|m)",
    re.IGNORECASE,
)
_LOAD_PATTERN = re.compile(r"\b(?P<load>low|medium|high)\b", re.IGNORECASE)


class ParseTaskRequest(BaseModel):
    text: str = Field(min_length=1, max_length=1000)


def _parse_duration(text: str) -> tuple[int, str]:
    match = _DURATION_PATTERN.search(text)
    if match is None:
        return 60, text

    value = float(match.group("value"))
    unit = match.group("unit").lower()
    minutes = int(value * 60) if unit in {"小时", "小時", "h", "hr", "hrs", "hour", "hours"} else int(value)
    cleaned = (text[: match.start()] + text[match.end() :]).strip()
    return max(1, min(minutes, 8 * 60)), cleaned


def _parse_load(text: str) -> tuple[int, str]:
    match = _LOAD_PATTERN.search(text)
    if match is None:
        return 5, text

    raw = match.group("load").lower()
    load = {"low": 3, "medium": 5, "high": 8}[raw]
    cleaned = (text[: match.start()] + text[match.end() :]).strip()
    return load, cleaned


@router.post("/ai/parse-task", summary="Parse a task draft locally")
def parse_task(payload: ParseTaskRequest) -> Dict[str, Any]:
    text = " ".join(payload.text.strip().split())
    estimated_minutes, without_duration = _parse_duration(text)
    cognitive_load, title = _parse_load(without_duration)

    return success(
        {
            "title": title.strip(" -,:;") or text,
            "estimated_minutes": estimated_minutes,
            "cognitive_load": cognitive_load,
            "due_at": None,
            "is_splittable": False,
            "max_split_count": 1,
            "status": "todo",
        }
    )
