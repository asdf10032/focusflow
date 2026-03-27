# -*- coding: utf-8 -*-
"""项目模型（projects）。"""
from __future__ import annotations
from sqlalchemy import String, Integer, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db.base import Base


class Project(Base):
    """项目表：用于归组任务并携带优先级。"""
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    priority: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=False), server_default=func.now(), nullable=False)
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=False), server_default=func.now(), onupdate=func.now(), nullable=False)

    # 关系：一对多到任务
    tasks: Mapped[list["Task"]] = relationship(back_populates="project", cascade="all,delete-orphan")
