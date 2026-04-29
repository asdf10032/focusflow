# -*- coding: utf-8 -*-
from __future__ import annotations

from datetime import date as dt_date, datetime, timedelta
from math import ceil
from typing import Iterable, List, Tuple

from sqlalchemy.orm import Session

from ...models.blocked_time import BlockedTime
from ...models.energy_template import EnergyTemplate
from ...models.task import Task
from ...models.task_dependency import TaskDependency
from ...schemas.schedule import ScheduleItemOut, SchedulePlanOut

SLOT_MINUTES = 30
SLOTS_PER_DAY = 24 * 60 // SLOT_MINUTES
PLAN_TYPES = ("conservative", "balanced", "aggressive")


def _day_type(d: dt_date) -> str:
    return "weekend" if d.weekday() >= 5 else "weekday"


def _load_energy_vector(db: Session, d: dt_date) -> List[int]:
    template = (
        db.query(EnergyTemplate)
        .filter(EnergyTemplate.name == "normal", EnergyTemplate.day_type == _day_type(d))
        .one_or_none()
    )
    if not template or not template.slots:
        return [50] * SLOTS_PER_DAY

    ordered = sorted(template.slots, key=lambda slot: slot.slot_index)
    values = [int(slot.energy) for slot in ordered]
    if len(values) < SLOTS_PER_DAY:
        values.extend([50] * (SLOTS_PER_DAY - len(values)))
    return values[:SLOTS_PER_DAY]


def _load_blocked_mask(db: Session, d: dt_date) -> List[bool]:
    mask = [False] * SLOTS_PER_DAY
    rows = db.query(BlockedTime).filter(BlockedTime.date == d).all()
    for blocked in rows:
        start_slot = max(0, blocked.start_minute_of_day // SLOT_MINUTES)
        end_slot = min(SLOTS_PER_DAY, ceil(blocked.end_minute_of_day / SLOT_MINUTES))
        for slot in range(start_slot, end_slot):
            mask[slot] = True
    return mask


def _available_slots(db: Session, d: dt_date) -> List[bool]:
    energy = _load_energy_vector(db, d)
    blocked = _load_blocked_mask(db, d)
    return [(energy[slot] > 0) and (not blocked[slot]) for slot in range(SLOTS_PER_DAY)]


def _query_candidate_tasks(db: Session) -> List[Task]:
    return (
        db.query(Task)
        .filter(Task.status.in_(["todo", "in_progress"]))
        .order_by(Task.id.asc())
        .all()
    )


def _due_key(task: Task) -> tuple[bool, datetime]:
    return (task.due_at is None, task.due_at or datetime.max)


def _priority_sorted(tasks: Iterable[Task], mode: str) -> List[Task]:
    if mode == "conservative":
        return sorted(tasks, key=lambda task: (task.cognitive_load, *_due_key(task), task.estimated_minutes, task.id))
    if mode == "aggressive":
        return sorted(tasks, key=lambda task: (*_due_key(task), -task.estimated_minutes, not task.is_splittable, task.id))
    return sorted(tasks, key=lambda task: (*_due_key(task), task.cognitive_load, task.id))


def _dependency_ordered_tasks(db: Session, tasks: List[Task], mode: str) -> List[Task]:
    if not tasks:
        return []

    by_id = {task.id: task for task in tasks}
    task_ids = set(by_id)
    dependencies = (
        db.query(TaskDependency)
        .filter(TaskDependency.task_id.in_(task_ids), TaskDependency.depends_on_task_id.in_(task_ids))
        .all()
    )

    dependents_by_prereq: dict[int, list[int]] = {task_id: [] for task_id in task_ids}
    indegree: dict[int, int] = {task_id: 0 for task_id in task_ids}
    for dep in dependencies:
        dependents_by_prereq[dep.depends_on_task_id].append(dep.task_id)
        indegree[dep.task_id] += 1

    priority_rank = {task.id: index for index, task in enumerate(_priority_sorted(tasks, mode))}
    ready = sorted((task_id for task_id, count in indegree.items() if count == 0), key=lambda task_id: priority_rank[task_id])
    ordered_ids: list[int] = []

    while ready:
        task_id = ready.pop(0)
        ordered_ids.append(task_id)
        for dependent_id in sorted(dependents_by_prereq[task_id], key=lambda item: priority_rank[item]):
            indegree[dependent_id] -= 1
            if indegree[dependent_id] == 0:
                ready.append(dependent_id)
        ready.sort(key=lambda item: priority_rank[item])

    if len(ordered_ids) != len(tasks):
        raise ValueError("cycle dependency detected")

    return [by_id[task_id] for task_id in ordered_ids]


def _slot_time(d: dt_date, slot_idx: int) -> Tuple[datetime, datetime]:
    start = datetime.combine(d, datetime.min.time()) + timedelta(minutes=slot_idx * SLOT_MINUTES)
    return start, start + timedelta(minutes=SLOT_MINUTES)


def _place_task_contiguous(available: List[bool], need_slots: int) -> int | None:
    run = 0
    start = 0
    for index, is_available in enumerate(available):
        if is_available:
            if run == 0:
                start = index
            run += 1
            if run >= need_slots:
                return start
        else:
            run = 0
    return None


def _place_task_split(available: List[bool], parts: int) -> List[int] | None:
    slots: list[int] = []
    for index, is_available in enumerate(available):
        if is_available:
            slots.append(index)
            if len(slots) >= parts:
                return slots
    return None


def _assign_for_mode(
    db: Session,
    tasks: List[Task],
    d: dt_date,
    initial_available: List[bool],
    mode: str,
) -> Tuple[List[ScheduleItemOut], List[int]]:
    items: list[ScheduleItemOut] = []
    unplaced: list[int] = []
    available = list(initial_available)

    for task in _dependency_ordered_tasks(db, tasks, mode):
        needed_slots = max(1, ceil(task.estimated_minutes / SLOT_MINUTES))
        if task.is_splittable:
            slots = _place_task_split(available, needed_slots)
        else:
            start_slot = _place_task_contiguous(available, needed_slots)
            slots = None if start_slot is None else list(range(start_slot, start_slot + needed_slots))

        if not slots:
            unplaced.append(task.id)
            continue

        for segment_index, slot in enumerate(slots):
            start, end = _slot_time(d, slot)
            items.append(
                ScheduleItemOut(
                    task_id=task.id,
                    start_datetime=start,
                    end_datetime=end,
                    segment_index=segment_index if len(slots) > 1 else None,
                    warning=None,
                )
            )
            available[slot] = False

    return items, unplaced


def _score_plan(items: List[ScheduleItemOut], unplaced: List[int]) -> float:
    placed_task_count = len({item.task_id for item in items})
    if placed_task_count == 0:
        return 0.0
    fragmentation_penalty = max(0, len(items) - placed_task_count) * 0.25
    unplaced_penalty = len(unplaced) * 5
    return max(0.0, round((placed_task_count * 10) - fragmentation_penalty - unplaced_penalty, 2))


def _risk_level(unplaced: List[int]) -> str:
    return "high" if unplaced else "low"


def _plan_summary(mode: str, items: List[ScheduleItemOut], unplaced: List[int]) -> str:
    task_count = len({item.task_id for item in items})
    item_count = len(items)
    if task_count == 0:
        return f"{mode} plan places no tasks and leaves {len(unplaced)} task(s) unscheduled."
    if item_count == task_count:
        return f"{mode} plan places {task_count} task(s) in focused blocks."
    return f"{mode} plan places {task_count} task(s) across {item_count} scheduled segment(s)."


def _risk_explanation(risk_level: str, unplaced: List[int]) -> str:
    if risk_level == "high":
        return f"Risk is high because {len(unplaced)} task(s) could not be scheduled."
    return "Risk is low because all candidate tasks fit into available time."


def generate_plans(db: Session, d: dt_date) -> Tuple[List[SchedulePlanOut], List[int], List[str]]:
    available = _available_slots(db, d)
    tasks = _query_candidate_tasks(db)

    plans: list[SchedulePlanOut] = []
    all_unplaced: set[int] = set()

    for mode in PLAN_TYPES:
        items, unplaced = _assign_for_mode(db, tasks, d, available, mode)
        risk_level = _risk_level(unplaced)
        all_unplaced.update(unplaced)
        plans.append(
            SchedulePlanOut(
                date=d,
                plan_type=mode,
                score=_score_plan(items, unplaced),
                risk_level=risk_level,
                summary=_plan_summary(mode, items, unplaced),
                risk_explanation=_risk_explanation(risk_level, unplaced),
                items=items,
            )
        )

    unplaced_ids = sorted(all_unplaced)
    warnings = [f"Task {task_id} could not be scheduled on {d.isoformat()}." for task_id in unplaced_ids]
    return plans, unplaced_ids, warnings
