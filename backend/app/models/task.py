# -*- coding: utf-8 -*-
"""任务模型（tasks）。"""
from __future__ import annotations
from sqlalchemy import String, Integer, Boolean, DateTime, ForeignKey, CheckConstraint, Index, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db.base import Base


class Task(Base):
    """任务表：包含估时、认知负荷、截止等关键字段。"""
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(300), nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    estimated_minutes: Mapped[int] = mapped_column(Integer, nullable=False)
    cognitive_load: Mapped[int] = mapped_column(Integer, nullable=False)
    due_at: Mapped[DateTime | None] = mapped_column(DateTime(timezone=False), nullable=True)
    earliest_start_at: Mapped[DateTime | None] = mapped_column(DateTime(timezone=False), nullable=True)
    fixed_start_at: Mapped[DateTime | None] = mapped_column(DateTime(timezone=False), nullable=True)
    is_splittable: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    max_split_count: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="todo", nullable=False)

    project_id: Mapped[int | None] = mapped_column(ForeignKey("projects.id", ondelete="SET NULL"), nullable=True)

    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=False), server_default=func.now(), nullable=False)
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=False), server_default=func.now(), onupdate=func.now(), nullable=False)

    __table_args__ = (
        CheckConstraint("status IN ('todo','in_progress','done','canceled')", name="ck_tasks_status"),
        Index("ix_tasks_project_id", "project_id"),
        Index("ix_tasks_due_at", "due_at"),
        Index("ix_tasks_status", "status"),
    )

    # 关系
    project: Mapped["Project | None"] = relationship(back_populates="tasks")
    dependencies: Mapped[list["TaskDependency"]] = relationship(back_populates="task", cascade="all,delete-orphan", foreign_keys="TaskDependency.task_id")
    dependents: Mapped[list["TaskDependency"]] = relationship(back_populates="depends_on", cascade="all,delete-orphan", foreign_keys="TaskDependency.depends_on_task_id")
