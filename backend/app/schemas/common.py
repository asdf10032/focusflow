# -*- coding: utf-8 -*-
"""通用 Schema 与分页模型。"""
from __future__ import annotations
from typing import Any, Generic, List, Optional, TypeVar
from pydantic import BaseModel, Field

T = TypeVar("T")


class Envelope(BaseModel):
    """统一响应模型（文档用途）。"""
    status: str
    data: Any | None = None
    error: dict | None = None
    meta: dict | None = None


class PageMeta(BaseModel):
    total: int = Field(ge=0)
    limit: int = Field(ge=1, le=100)
    offset: int = Field(ge=0)


class Page(BaseModel, Generic[T]):
    items: List[T]
    meta: PageMeta
