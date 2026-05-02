# -*- coding: utf-8 -*-
"""排期方案（schedule_plans）。"""
from __future__ import annotations
from datetime import date
from sqlalchemy import String, Boolean, Date, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db.base import Base


class SchedulePlan(Base):
    __tablename__ = "schedule_plans"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    plan_type: Mapped[str] = mapped_column(String(20), nullable=False)  # conservative/balanced/aggressive
    score: Mapped[float] = mapped_column(Float, nullable=True)
    risk_level: Mapped[str] = mapped_column(String(20), nullable=True)  # low/medium/high
    selected: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    items: Mapped[list["ScheduleItem"]] = relationship(back_populates="plan", cascade="all,delete-orphan")
