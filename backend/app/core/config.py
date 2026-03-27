# -*- coding: utf-8 -*-
"""
应用配置模块：从环境变量读取基础配置。
说明：为避免额外依赖，此处不使用 pydantic-settings，保持零依赖读取。
"""
import os
from functools import lru_cache
from typing import List


class Settings:
    """运行时配置（简化版）。"""
    ENV: str
    APP_NAME: str
    APP_VERSION: str
    PORT: int
    CORS_ORIGINS: List[str]

    def __init__(self) -> None:
        # 环境：dev / prod
        self.ENV = os.getenv("ENV", "dev")
        self.APP_NAME = os.getenv("APP_NAME", "FocusFlow API")
        self.APP_VERSION = os.getenv("APP_VERSION", "0.1.0")
        # 端口仅用于文档说明，实际由启动命令决定
        self.PORT = int(os.getenv("PORT", "8000"))
        # 逗号分隔的 origins 列表
        origins = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173")
        self.CORS_ORIGINS = [o.strip() for o in origins.split(",") if o.strip()]


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """获取单例配置实例。"""
    return Settings()
