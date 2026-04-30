# -*- coding: utf-8 -*-
from __future__ import annotations

from pydantic import BaseModel


class ExportPayload(BaseModel):
    filename: str
    content_type: str
    content: str
    record_count: int | None = None

