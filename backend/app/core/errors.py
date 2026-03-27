# -*- coding: utf-8 -*-
"""
应用自定义异常与错误到响应的映射。
"""
from typing import Optional, Dict, Any
from fastapi import Request
from fastapi.responses import JSONResponse


class AppError(Exception):
    """业务层可抛出的受检异常。

    中文约定：
    - code：稳定错误码（前端可据此分类处理）
    - message：面向用户的可读信息
    - status_code：HTTP 状态码（默认 400）
    - details：可选的调试信息（不包含敏感数据）
    """

    def __init__(self, code: str, message: str, status_code: int = 400, details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details or None


async def app_error_handler(_: Request, exc: AppError) -> JSONResponse:
    """将 AppError 转换为统一错误响应。"""
    from .response import error_response  # 延迟导入避免循环

    return error_response(
        code=exc.code,
        message=exc.message,
        details=exc.details,
        status_code=exc.status_code,
    )
