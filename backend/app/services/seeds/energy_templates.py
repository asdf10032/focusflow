# -*- coding: utf-8 -*-
"""种子脚本：写入默认能量模板（early_bird/normal/night_owl）。

特性：
- 幂等：若模板已存在，则覆盖其 slots 以确保一致性。
- 范围：weekday / weekend 各 48 槽，取值 0..100。

使用：
- 作为模块调用：seed_default_templates(db)
- 命令行一次性执行：
  python -m backend.app.services.seeds.energy_templates
"""
from __future__ import annotations
from typing import List, Dict
import os

from sqlalchemy.orm import Session

from ...db.session import SessionLocal, DATABASE_URL
from ...models.energy_template import EnergyTemplate
from ...models.energy_template_slot import EnergyTemplateSlot


def _curve_early_bird(day_type: str) -> List[int]:
    """早起型：上午高峰 8-11，午后回落，晚上低。"""
    base = [20]*48
    # 8:00-11:30 → slots 16..23 提升
    for i in range(16, 24):
        base[i] = 70
    # 下午 14:00-16:30 → slots 28..33 中等
    for i in range(28, 34):
        base[i] = 55
    # 晚上降至 30-40
    for i in range(36, 46):
        base[i] = 35
    if day_type == "weekend":
        base = [min(100, int(x*0.9)) for x in base]
    return base


def _curve_normal(day_type: str) -> List[int]:
    """常规型：中午略高，晚上适中。"""
    base = [40]*48
    for i in range(22, 30):  # 11:00-14:30
        base[i] = 60
    for i in range(34, 42):  # 17:00-20:30
        base[i] = 55
    if day_type == "weekend":
        base = [min(100, int(x*0.95)) for x in base]
    return base


def _curve_night_owl(day_type: str) -> List[int]:
    """夜猫型：20-23 点高峰，早晨低。"""
    base = [30]*48
    for i in range(0, 10):  # 凌晨低
        base[i] = 20
    for i in range(40, 47):  # 20:00-23:30
        base[i] = 70
    for i in range(16, 22):  # 上午中等
        base[i] = 50
    if day_type == "weekend":
        base = [min(100, int(x*1.05)) for x in base]
    return base


_DEFAULTS: Dict[str, callable] = {
    "early_bird": _curve_early_bird,
    "normal": _curve_normal,
    "night_owl": _curve_night_owl,
}


def _ensure_template(db: Session, name: str, day_type: str, slots: List[int]) -> None:
    tpl = (
        db.query(EnergyTemplate)
        .filter(EnergyTemplate.name == name, EnergyTemplate.day_type == day_type)
        .one_or_none()
    )
    if tpl is None:
        tpl = EnergyTemplate(name=name, day_type=day_type)
        db.add(tpl)
        db.flush()
    # 覆盖 48 槽
    tpl.slots.clear()
    for idx, energy in enumerate(slots):
        tpl.slots.append(EnergyTemplateSlot(slot_index=idx, energy=int(energy)))


def seed_default_templates(db: Session) -> None:
    """写入默认模板（weekday/weekend × 3 类）。"""
    for name, fn in _DEFAULTS.items():
        for day_type in ("weekday", "weekend"):
            _ensure_template(db, name, day_type, fn(day_type))
    db.commit()


if __name__ == "__main__":
    # 允许直接运行：python -m backend.app.services.seeds.energy_templates
    # 提示：如使用 SQLite，确保 ./data 目录存在
    if DATABASE_URL.startswith("sqlite"):
        os.makedirs("data", exist_ok=True)
    session = SessionLocal()
    try:
        seed_default_templates(session)
        print("[seed] energy templates seeded.")
    finally:
        session.close()
