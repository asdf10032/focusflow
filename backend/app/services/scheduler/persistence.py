# -*- coding: utf-8 -*-
from __future__ import annotations

from datetime import date as dt_date

from sqlalchemy.orm import Session

from ...models.schedule_item import ScheduleItem
from ...models.schedule_plan import SchedulePlan
from ...schemas.schedule import GenerateResponse


def replace_persisted_plans(db: Session, d: dt_date, response: GenerateResponse) -> None:
    existing = db.query(SchedulePlan).filter(SchedulePlan.date == d).all()
    for plan in existing:
        db.delete(plan)
    db.flush()

    for plan_out in response.plans:
        plan = SchedulePlan(
            date=d,
            plan_type=plan_out.plan_type,
            score=plan_out.score,
            risk_level=plan_out.risk_level,
            selected=False,
        )
        db.add(plan)
        db.flush()

        for item_out in plan_out.items:
            plan.items.append(
                ScheduleItem(
                    task_id=item_out.task_id,
                    start_datetime=item_out.start_datetime,
                    end_datetime=item_out.end_datetime,
                    segment_index=item_out.segment_index or 0,
                    warning=item_out.warning,
                )
            )
    db.commit()
