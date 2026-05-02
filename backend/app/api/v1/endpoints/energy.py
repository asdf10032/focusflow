# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from ....core.errors import AppError
from ....core.response import success
from ....db.session import get_db
from ....models.blocked_time import BlockedTime
from ....models.energy_template import EnergyTemplate
from ....models.energy_template_slot import EnergyTemplateSlot
from ....schemas.energy import BlockedTimeCreate, BlockedTimeOut, EnergyTemplateUpdate

router = APIRouter()


def _energy_template_data(template: EnergyTemplate) -> dict:
    return {
        "id": template.id,
        "name": template.name,
        "day_type": template.day_type,
        "slots": [
            {"slot_index": slot.slot_index, "energy": slot.energy}
            for slot in sorted(template.slots, key=lambda item: item.slot_index)
        ],
    }


def _blocked_time_data(blocked_time: BlockedTime) -> dict:
    return BlockedTimeOut.model_validate(blocked_time).model_dump(mode="json")


@router.get("/energy/templates", summary="List energy templates")
def list_energy_templates(db: Session = Depends(get_db)):
    rows = db.execute(select(EnergyTemplate).order_by(EnergyTemplate.id.desc())).scalars().all()
    return success([_energy_template_data(row) for row in rows])


@router.put("/energy/templates/{template_id}", summary="Update energy template slots")
def update_energy_template(template_id: int, payload: EnergyTemplateUpdate, db: Session = Depends(get_db)):
    template = db.get(EnergyTemplate, template_id)
    if not template:
        raise AppError(code="not_found", message="Energy template not found", status_code=404)

    template.slots.clear()
    for slot in payload.slots:
        template.slots.append(EnergyTemplateSlot(slot_index=slot.slot_index, energy=slot.energy))
    db.commit()
    db.refresh(template)
    return success(_energy_template_data(template))


@router.get("/blocked-times", summary="List blocked times")
def list_blocked_times(date: Optional[str] = Query(default=None), db: Session = Depends(get_db)):
    stmt = select(BlockedTime)
    if date:
        stmt = stmt.where(BlockedTime.date == date)
    rows = db.execute(stmt.order_by(BlockedTime.id.asc())).scalars().all()
    return success([_blocked_time_data(row) for row in rows])


@router.post("/blocked-times", summary="Create blocked time")
def create_blocked_time(payload: BlockedTimeCreate, db: Session = Depends(get_db)):
    obj = BlockedTime(**payload.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return success(_blocked_time_data(obj))


@router.delete("/blocked-times/{bt_id}", summary="Delete blocked time")
def delete_blocked_time(bt_id: int, db: Session = Depends(get_db)):
    obj = db.get(BlockedTime, bt_id)
    if not obj:
        raise AppError(code="not_found", message="Blocked time not found", status_code=404)
    db.delete(obj)
    db.commit()
    return success(True)
