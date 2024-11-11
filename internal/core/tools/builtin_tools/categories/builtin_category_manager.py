#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2024/9/16 上午11:42
@Author : www.mingerzeng@gmail.com
@File : builtin_category_manager.py
"""
import os.path
from typing import Any

import yaml
from injector import inject, singleton
from pydantic import BaseModel,Field
from internal.exception import NotFoundException
from internal.core.tools.builtin_tools.entities import CategoryEntity

@inject
@singleton
class BuiltinCategoryManager(BaseModel):
    """內置的工具分類管理器"""
    category_map: dict[str, Any] = Field(default_factory=dict)

    def __init__(self, **kwargs):
        """分類管理器初始化"""
        super().__init__(**kwargs)
        self._init_categories()

    def get_category_map(self) -> dict[str, Any]:
        """獲取分類映射資訊"""
        return self.category_map

    def _init_categories(self):
        """初始化分類資料"""
        # 1. 檢測資料是否已經處理
        if self.category_map:
            return

        # 2. 獲取yaml資料路徑並加載
        current_path = os.path.abspath(__file__)
        category_path = os.path.dirname(current_path)
        category_yaml_path = os.path.join(category_path, "categories.yaml")
        with open(category_yaml_path, encoding="utf-8") as f:
            categories = yaml.safe_load(f)

        # 3. 循環遍歷所有分類，並且將分類加載成實體資訊
        for category in categories:
            # 4. 創建分類實體資訊
            category_entity = CategoryEntity(**category)

            # 5. 獲取icon的位置並檢測icon是否存在
            icon_path = os.path.join(category_path, "icons", category_entity.icon)
            if not os.path.exists(icon_path):
                raise NotFoundException(f"該分類{category_entity.category}的icon未提供")

            # 6. 讀取對應的icon資訊
            with open(icon_path, encoding="utf-8") as f:
                icon = f.read()

            # 7. 將資料映射到字典中
            self.category_map[category_entity.category] = {
                "entity": category_entity,
                "icon": icon,
            }

