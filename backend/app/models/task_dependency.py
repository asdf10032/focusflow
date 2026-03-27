# -*- coding: utf-8 -*-
"""任务依赖（task_dependencies）。"""
from __future__ import annotations
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db.base import Base


class TaskDependency(Base):
    __tablename__ = "task_dependencies"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False)
    depends_on_task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False)

    __table_args__ = (
        UniqueConstraint("task_id", "depends_on_task_id", name="uq_task_dep_pair"),
    )

    task: Mapped["Task"] = relationship(foreign_keys=[task_id], back_populates="dependencies")
    depends_on: Mapped["Task"] = relationship(foreign_keys=[depends_on_task_id], back_populates="dependents")
