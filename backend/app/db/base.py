# -*- coding: utf-8 -*-
"""SQLAlchemy Base 与模型聚合入口。Alembic 将从此处导入元数据。"""
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# Alembic 环境会 import 本模块，从而递归导入所有 models 以注册元数据
# 注意：保持导入在文件底部，避免循环依赖
try:
    from .. import models  # noqa: F401  # 导入以注册模型
except Exception:
    # 在某些工具静态分析/早期导入阶段，models 可能不存在，忽略即可
    pass
