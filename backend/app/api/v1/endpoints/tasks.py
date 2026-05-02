# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from ....core.errors import AppError
from ....core.response import success
from ....db.session import get_db
from ....models.task import Task
from ....schemas.task import TaskCreate, TaskOut, TaskUpdate

router = APIRouter()


def _task_data(task: Task) -> dict:
    return TaskOut.model_validate(task).model_dump(mode="json")


@router.get("/tasks", summary="List tasks")
def list_tasks(
    status: Optional[str] = Query(default=None),
    project_id: Optional[int] = Query(default=None),
    q: Optional[str] = Query(default=None),
    db: Session = Depends(get_db),
):
    stmt = select(Task)
    if status:
        stmt = stmt.where(Task.status == status)
    if project_id:
        stmt = stmt.where(Task.project_id == project_id)
    query = q.strip() if q else ""
    if query:
        pattern = f"%{query}%"
        stmt = stmt.where(or_(Task.title.ilike(pattern), Task.notes.ilike(pattern)))
    rows = db.execute(stmt.order_by(Task.id.desc())).scalars().all()
    return success([_task_data(row) for row in rows])


@router.post("/tasks", summary="Create task")
def create_task(payload: TaskCreate, db: Session = Depends(get_db)):
    obj = Task(**payload.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return success(_task_data(obj))


@router.put("/tasks/{task_id}", summary="Update task")
def update_task(task_id: int, payload: TaskUpdate, db: Session = Depends(get_db)):
    obj = db.get(Task, task_id)
    if not obj:
        raise AppError(code="not_found", message="Task not found", status_code=404)
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return success(_task_data(obj))


@router.delete("/tasks/{task_id}", summary="Delete task")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    obj = db.get(Task, task_id)
    if not obj:
        raise AppError(code="not_found", message="Task not found", status_code=404)
    db.delete(obj)
    db.commit()
    return success(True)
