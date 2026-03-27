# -*- coding: utf-8 -*-
"""能量模板槽（energy_template_slots）。"""
from __future__ import annotations
from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db.base import Base


class EnergyTemplateSlot(Base):
    __tablename__ = "energy_template_slots"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    template_id: Mapped[int] = mapped_column(ForeignKey("energy_templates.id", ondelete="CASCADE"), nullable=False)
    slot_index: Mapped[int] = mapped_column(Integer, nullable=False)  # 0..47
    energy: Mapped[int] = mapped_column(Integer, nullable=False)  # 0..100

    template: Mapped["EnergyTemplate"] = relationship(back_populates="slots")
