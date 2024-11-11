#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2024/10/29 下午3:10
@Author : www.mingerzeng@gmail.com
@File : demo_task.py
"""
import logging
import time
from uuid import UUID
from flask import current_app

from celery import shared_task

@shared_task
def demo_task(id: UUID) -> str:
    """測試異步任務"""
    logging.info("睡眠5秒")
    time.sleep(5)
    logging.info(f"id的值:{id}")
    logging.info(f"配置資訊:{current_app.config}")
    return "募小可"