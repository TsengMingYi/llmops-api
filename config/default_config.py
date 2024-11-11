#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2024/8/13 下午1:13
@Author : www.mingerzeng@gmail.com
@File : default_config.py
"""

# 應用默認配置項
DEFAULT_CONFIG = {
    # wtf配置
    "WTF_CSRF_ENABLED" : "False",

    # SQLAlchemy資料庫配置
"SQLALCHEMY_DATABASE_URI" :"",
"SQLALCHEMY_POOL_SIZE":30,
"SQLALCHEMY_POOL_RECYCLE":3600,
"SQLALCHEMY_ECHO":"True",

    # Redis資料庫配置
    "REDIS_HOST": "localhost",
    "REDIS_PORT": "6379",
    "REDIS_USERNAME": "",
    "REDIS_PASSWORD": "",
    "REDIS_DB": "0",
    "REDIS_USE_SSL": "False",

    # Celery默認配置
    "CELERY_BROKER_DB": 1,
    "CELERY_RESULT_BACKEND_DB": 1,
    "CELERY_TASK_IGNORE_RESULT": "False",
    "CELERY_RESULT_EXPIRES": 3600,
    "CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP": "True",
}
