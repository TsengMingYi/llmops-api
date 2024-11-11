#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2024/9/16 上午8:53
@Author : www.mingerzeng@gmail.com
@File : current_time.py
"""
from typing import Any
from datetime import datetime
from langchain_core.tools import BaseTool

class CurrentTimeTool(BaseTool):
    """一個用於獲取當前時間的工具"""
    name = "current_time"
    description = "一個用於獲取當前時間的工具"

    def _run(self, *args: Any, **kwargs: Any) -> Any:
        """獲取當前系統的時間並進行格式化後返回"""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S %Z")

def current_time(**kwargs) -> BaseTool:
    """返回獲取當前時間的LangChain工具"""
    return CurrentTimeTool()
