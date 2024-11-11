#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2024/9/16 上午3:02
@Author : www.mingerzeng@gmail.com
@File : helper.py
"""
from typing import Any
import importlib


def dynamic_import(module_name: str, symbol_name: str) -> Any:
    """動態導入特定模塊下的特定功能"""
    module = importlib.import_module(module_name)
    return getattr(module, symbol_name)

def add_attribute(attr_name: str, attr_value: Any):
    """裝飾器函數，為特定的函數添加相應的屬性，第一個參數為屬性名字，第二個參數為屬性值"""

    def decorator(func):
        setattr(func, attr_name, attr_value)
        return func

    return decorator