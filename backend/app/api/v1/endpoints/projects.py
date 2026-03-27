# -*- coding: utf-8 -*-
"""Projects 路由。"""
from __future__ import annotations
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ....db.session import get_db
from ....models.project import Project
from ....core.response import success
from ....schemas.project import ProjectCreate, ProjectOut

router = APIRouter()


@router.get("/projects", response_model=List[ProjectOut], summary="获取项目列表")
def list_projects(db: Session = Depends(get_db)):
    """返回所有项目。第一版不分页。"""
    items = db.query(Project).order_by(Project.id.desc()).all()
    return items


@router.post("/projects", response_model=ProjectOut, summary="创建项目")
def create_project(payload: ProjectCreate, db: Session = Depends(get_db)):
    """创建新项目。"""
    obj = Project(name=payload.name, priority=payload.priority)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj
