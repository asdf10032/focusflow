# -*- coding: utf-8 -*-
"""数据库会话与基础设施。"""
from __future__ import annotations
import os
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/app.db")
# SQLite 需要 check_same_thread=False 才能在 FastAPI 中使用同一连接
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
    future=True,
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def get_db() -> Generator[Session, None, None]:
    """FastAPI 依赖：提供 DB 会话，自动关闭。"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
