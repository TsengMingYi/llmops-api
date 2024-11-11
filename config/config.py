#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2024/8/12 上午9:41
@Author : www.mingerzeng@gmail.com
@File : config.py
"""
import os
from typing import Any
from .default_config import DEFAULT_CONFIG


def _get_env(key: str) -> Any:
    """從環境變量中獲取配置項，如果找不到則返回默認值"""
    # return os.environ.get(key,DEFAULT_CONFIG.get(key))
    return os.getenv(key,DEFAULT_CONFIG.get(key))

def _get_bool_env(key : str) -> bool:
    """從環境變量中獲取布爾值型的配置項，如果找不到則返回默認值"""
    value : str = _get_env(key)
    return value.lower() == "true" if value is not None else False

class Config:
    def __init__(self):
        # 關閉wtf的csrf保護
        self.WTF_CSRF_ENABLED = _get_bool_env("WTF_CSRF_ENABLED")

        # 配置資料庫配置
        self.SQLALCHEMY_DATABASE_URI = _get_env("SQLALCHEMY_DATABASE_URI")
        self.SQLALCHEMY_ENGINE_OPTIONS = {
            "pool_size": int(_get_env("SQLALCHEMY_POOL_SIZE")),
            "pool_recycle": int(_get_env("SQLALCHEMY_POOL_RECYCLE"))
        }
        self.SQLALCHEMY_ECHO = _get_bool_env("SQLALCHEMY_ECHO")

        # 配置Redis配置
        self.REDIS_HOST = _get_env("REDIS_HOST")
        self.REDIS_PORT = _get_env("REDIS_PORT")
        self.REDIS_USERNAME = _get_env("REDIS_USERNAME")
        self.REDIS_PASSWORD = _get_env("REDIS_PASSWORD")
        self.REDIS_DB = _get_env("REDIS_DB")
        self.REDIS_USE_SSL = _get_bool_env("REDIS_USE_SSL")

        # Celery配置
        self.CELERY = {
            "broker_url": f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{int(_get_env('CELERY_BROKER_DB'))}",
            "result_backend": f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{int(_get_env('CELERY_RESULT_BACKEND_DB'))}",
            "task_ignore_result": _get_bool_env("CELERY_TASK_IGNORE_RESULT"),
            "result_expires": int(_get_env("CELERY_RESULT_EXPIRES")),
            "broker_connection_retry_on_startup": _get_bool_env("CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP"),
        }
        