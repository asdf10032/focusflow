# -*- coding: utf-8 -*-
"""不可排时间段（blocked_times）。"""
from __future__ import annotations
from sqlalchemy import String, Integer, Date, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column
from ..db.base import Base


class BlockedTime(Base):
    __tablename__ = "blocked_times"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    date: Mapped[Date] = mapped_column(Date, nullable=False)
    start_minute_of_day: Mapped[int] = mapped_column(Integer, nullable=False)  # 0..1439
    end_minute_of_day: Mapped[int] = mapped_column(Integer, nullable=False)  # start<end
    category: Mapped[str] = mapped_column(String(20), nullable=False)  # sleep/class/custom
    note: Mapped[str | None] = mapped_column(String(200), nullable=True)

    __table_args__ = (
        CheckConstraint("start_minute_of_day >= 0 AND start_minute_of_day < 1440", name="ck_bt_start"),
        CheckConstraint("end_minute_of_day > 0 AND end_minute_of_day <= 1440", name="ck_bt_end"),
        CheckConstraint("start_minute_of_day < end_minute_of_day", name="ck_bt_range"),
    )
