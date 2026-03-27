# -*- coding: utf-8 -*-
"""SQLAlchemy Base 与模型聚合入口。Alembic 将从此处导入元数据。"""
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# 注意：Alembic 环境中会 import 本模块，从而递归导入所有 models
# 后续在此导入 models.* 以注册到元数据（Phase 1 中待补充具体模型文件）。
