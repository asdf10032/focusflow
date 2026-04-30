# -*- coding: utf-8 -*-
"""应用入口：注册路由、CORS、异常处理。"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import get_settings
from .core.errors import AppError, app_error_handler
from .core.response import http_exception_handler
from .api.v1.endpoints.health import router as health_router
from .api.v1.endpoints.projects import router as projects_router
from .api.v1.endpoints.tasks import router as tasks_router
from .api.v1.endpoints.energy import router as energy_router
from .api.v1.endpoints.schedules import router as schedules_router
from .api.v1.endpoints.execution import router as execution_router
from .api.v1.endpoints.ai import router as ai_router
from .api.v1.endpoints.exports import router as exports_router

settings = get_settings()

app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 异常处理
app.add_exception_handler(AppError, app_error_handler)
app.add_exception_handler(Exception, http_exception_handler)

# 路由
app.include_router(health_router, prefix="/api/v1")
app.include_router(projects_router, prefix="/api/v1")
app.include_router(tasks_router, prefix="/api/v1")
app.include_router(energy_router, prefix="/api/v1")
app.include_router(schedules_router, prefix="/api/v1")
app.include_router(execution_router, prefix="/api/v1")
app.include_router(ai_router, prefix="/api/v1")
app.include_router(exports_router, prefix="/api/v1")


# 便于 "uvicorn backend.app.main:app --reload" 启动
__all__ = ["app"]
