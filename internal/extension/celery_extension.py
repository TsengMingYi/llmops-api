#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2024/10/28 下午2:57
@Author : www.mingerzeng@gmail.com
@File : celery_extension.py
"""

from flask import Flask
from celery import Task,Celery

def init_app(app: Flask):
    """Celery配置服務初始化"""


    class FlaskTask(Task):
        """定義FlaskTask，確保Celery在Flask應用的上下文中運行，這樣可以訪問flask配置，資料庫等內容"""
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    # 1. 創建Celery應用並配置
    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()

    # 2. 將celery掛載到app的擴展中
    app.extensions["celery"] = celery_app