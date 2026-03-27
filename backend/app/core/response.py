# -*- coding: utf-8 -*-
"""
统一响应与错误处理：
- 标准响应 envelope：{status, data, error, meta}
- FastAPI 依赖的异常转换
"""
from typing import Any, Dict, Optional
from fastapi import Request
from fastapi.responses import JSONResponse


def success(data: Any = None, meta: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """成功响应构造器。
    参数：
    - data: 业务数据
    - meta: 附加元信息（分页等）
    返回：统一结构的 dict
    """
    return {
        "status": "success",
        "data": data,
        "error": None,
        "meta": meta or None,
    }


def error_response(code: str, message: str, details: Optional[Dict[str, Any]] = None, status_code: int = 400) -> JSONResponse:
    """错误响应构造器（直接返回 JSONResponse）。"""
    payload = {
        "status": "error",
        "data": None,
        "error": {"code": code, "message": message, "details": details or None},
        "meta": None,
    }
    return JSONResponse(status_code=status_code, content=payload)


async def http_exception_handler(_: Request, exc: Exception) -> JSONResponse:
    """兜底异常处理：防止内部异常泄漏。"""
    return error_response(code="internal_error", message=str(exc) if __debug__ else "internal server error", status_code=500)
