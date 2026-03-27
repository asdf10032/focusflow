# -*- coding: utf-8 -*-
"""Energy/Blocked 路由。"""
from __future__ import annotations
from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import select
from ....db.session import get_db
from ....models.energy_template import EnergyTemplate
from ....models.energy_template_slot import EnergyTemplateSlot
from ....models.blocked_time import BlockedTime
from ....schemas.energy import (
    EnergyTemplateOut,
    EnergyTemplateUpdate,
    BlockedTimeCreate,
    BlockedTimeOut,
)

router = APIRouter()


@router.get("/energy/templates", response_model=List[EnergyTemplateOut], summary="读取能量模板")
def list_energy_templates(db: Session = Depends(get_db)):
    rows = db.execute(select(EnergyTemplate).order_by(EnergyTemplate.id.desc())).scalars().all()
    # 触发加载 slots（如未配置 lazy）
    for t in rows:
        _ = [EnergyTemplateSlot(slot_index=s.slot_index, energy=s.energy) for s in t.slots]
    return rows


@router.put("/energy/templates/{template_id}", response_model=EnergyTemplateOut, summary="更新模板槽位")
def update_energy_template(template_id: int, payload: EnergyTemplateUpdate, db: Session = Depends(get_db)):
    tpl = db.get(EnergyTemplate, template_id)
    if not tpl:
        from ....core.errors import AppError
        raise AppError(code="not_found", message="模板不存在", status_code=404)
    # 全量替换 48 槽
    tpl.slots.clear()
    for s in payload.slots:
        tpl.slots.append(EnergyTemplateSlot(slot_index=s.slot_index, energy=s.energy))
    db.commit()
    db.refresh(tpl)
    return tpl


@router.get("/blocked-times", response_model=List[BlockedTimeOut], summary="读取当天 blocked time")
def list_blocked_times(date: Optional[str] = Query(default=None), db: Session = Depends(get_db)):
    stmt = select(BlockedTime)
    # 可按需扩展：按日期过滤
    rows = db.execute(stmt).scalars().all()
    return rows


@router.post("/blocked-times", response_model=BlockedTimeOut, summary="创建 blocked time")
def create_blocked_time(payload: BlockedTimeCreate, db: Session = Depends(get_db)):
    obj = BlockedTime(**payload.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/blocked-times/{bt_id}", summary="删除 blocked time")
def delete_blocked_time(bt_id: int, db: Session = Depends(get_db)):
    obj = db.get(BlockedTime, bt_id)
    if not obj:
        from ....core.errors import AppError
        raise AppError(code="not_found", message="记录不存在", status_code=404)
    db.delete(obj)
    db.commit()
    return {"status": "success", "data": True, "error": None, "meta": None}
