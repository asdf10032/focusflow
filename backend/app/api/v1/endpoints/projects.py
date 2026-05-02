# -*- coding: utf-8 -*-
from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ....core.response import success
from ....db.session import get_db
from ....models.project import Project
from ....schemas.project import ProjectCreate, ProjectOut

router = APIRouter()


def _project_data(project: Project) -> dict:
    return ProjectOut.model_validate(project).model_dump(mode="json")


@router.get("/projects", summary="List projects")
def list_projects(db: Session = Depends(get_db)):
    items = db.query(Project).order_by(Project.id.desc()).all()
    return success([_project_data(item) for item in items])


@router.post("/projects", summary="Create project")
def create_project(payload: ProjectCreate, db: Session = Depends(get_db)):
    obj = Project(name=payload.name, priority=payload.priority)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return success(_project_data(obj))
