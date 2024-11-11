#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2024/9/16 上午11:53
@Author : www.mingerzeng@gmail.com
@File : category_entity.py
"""
from pydantic import BaseModel, field_validator
from internal.exception import FailException

class CategoryEntity(BaseModel):
    """分類實體"""
    category: str # 分類唯一標識
    name: str # 分類名稱
    icon: str # 分類圖標名稱

    @field_validator("icon")
    def check_icon_extension(cls, value: str):
        """校驗icon的擴展名是不是.svg，如果不是則拋出錯誤"""
        if not value.endswith(".svg"):
            raise FailException("該分類的icon圖標並不是.svg格式")
        return value