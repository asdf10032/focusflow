# -*- coding: utf-8 -*-
"""健康检查端点。"""
from fastapi import APIRouter
from ....core.response import success

router = APIRouter()


@router.get("/health", summary="健康检查")
def health_check():
    """返回服务健康状态。"""
    return success({"ok": True})
