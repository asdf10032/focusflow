# -*- coding: utf-8 -*-
"""排期项（schedule_items）。"""
from __future__ import annotations
from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db.base import Base


class ScheduleItem(Base):
    __tablename__ = "schedule_items"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    plan_id: Mapped[int] = mapped_column(ForeignKey("schedule_plans.id", ondelete="CASCADE"), nullable=False)
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False)
    start_datetime: Mapped[DateTime] = mapped_column(DateTime(timezone=False), nullable=False)
    end_datetime: Mapped[DateTime] = mapped_column(DateTime(timezone=False), nullable=False)
    segment_index: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    warning: Mapped[str | None] = mapped_column(String(200), nullable=True)

    plan: Mapped["SchedulePlan"] = relationship(back_populates="items")
