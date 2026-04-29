# -*- coding: utf-8 -*-
from __future__ import annotations

from datetime import date, datetime

from sqlalchemy import CheckConstraint, Date, DateTime, Index, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from ..db.base import Base


class ExecutionLog(Base):
    __tablename__ = "execution_logs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    task_id: Mapped[int] = mapped_column(Integer, nullable=False)
    task_title_snapshot: Mapped[str] = mapped_column(String(300), nullable=False)
    estimated_minutes_snapshot: Mapped[int] = mapped_column(Integer, nullable=False)
    task_project_id_snapshot: Mapped[int | None] = mapped_column(Integer, nullable=True)
    cognitive_load_snapshot: Mapped[int | None] = mapped_column(Integer, nullable=True)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False)
    actual_minutes: Mapped[int | None] = mapped_column(Integer, nullable=True)
    note: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=False), server_default=func.now(), nullable=False)

    __table_args__ = (
        CheckConstraint(
            "status IN ('done','skipped','incomplete','canceled')",
            name="ck_execution_logs_status",
        ),
        Index("ix_execution_logs_date", "date"),
        Index("ix_execution_logs_task_id", "task_id"),
    )

