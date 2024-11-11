#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2024/8/12 上午10:11
@Author : www.mingerzeng@gmail.com
@File : http_code.py
"""
from enum import Enum

class HttpCode(str, Enum):
    """Http基礎業務狀態碼"""
    SUCCESS = 'success' # 成功狀態
    FAIL = "fail" # 失敗狀態
    NOT_FOUND = "not_found" # 未找到
    UNAUTHORIZED = "unauthorized" # 未授權
    FORBIDDEN = "forbidden" # 無權限
    VALIDATE_ERROR = "validate_error" # 資料驗證錯誤
