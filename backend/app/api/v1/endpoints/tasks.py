# -*- coding: utf-8 -*-
"""Tasks 路由。"""
from __future__ import annotations
from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import select
from ....db.session import get_db
from ....models.task import Task
from ....schemas.task import TaskCreate, TaskUpdate, TaskOut

router = APIRouter()


@router.get("/tasks", response_model=List[TaskOut], summary="获取任务列表")
def list_tasks(
    status: Optional[str] = Query(default=None),
    project_id: Optional[int] = Query(default=None),
    db: Session = Depends(get_db),
):
    """按需过滤任务列表。第一版不分页。"""
    stmt = select(Task)
    if status:
        stmt = stmt.where(Task.status == status)
    if project_id:
        stmt = stmt.where(Task.project_id == project_id)
    rows = db.execute(stmt.order_by(Task.id.desc())).scalars().all()
    return rows


@router.post("/tasks", response_model=TaskOut, summary="创建任务")
def create_task(payload: TaskCreate, db: Session = Depends(get_db)):
    """创建任务。"""
    obj = Task(**payload.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.put("/tasks/{task_id}", response_model=TaskOut, summary="更新任务")
def update_task(task_id: int, payload: TaskUpdate, db: Session = Depends(get_db)):
    """更新任务。"""
    obj = db.get(Task, task_id)
    if not obj:
        from ....core.errors import AppError
        raise AppError(code="not_found", message="任务不存在", status_code=404)
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/tasks/{task_id}", summary="删除任务")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """删除任务。"""
    obj = db.get(Task, task_id)
    if not obj:
        from ....core.errors import AppError
        raise AppError(code="not_found", message="任务不存在", status_code=404)
    db.delete(obj)
    db.commit()
    return {"status": "success", "data": True, "error": None, "meta": None}
