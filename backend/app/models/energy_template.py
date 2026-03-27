# -*- coding: utf-8 -*-
"""能量模板（energy_templates）。"""
from __future__ import annotations
from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db.base import Base


class EnergyTemplate(Base):
    __tablename__ = "energy_templates"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)  # early_bird/normal/night_owl/custom
    day_type: Mapped[str] = mapped_column(String(20), nullable=False)  # weekday/weekend
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=False), server_default=func.now(), nullable=False)

    slots: Mapped[list["EnergyTemplateSlot"]] = relationship(back_populates="template", cascade="all,delete-orphan")
