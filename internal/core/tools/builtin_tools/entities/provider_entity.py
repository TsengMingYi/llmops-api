#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2024/9/16 上午2:36
@Author : www.mingerzeng@gmail.com
@File : provider_entity.py
"""
import yaml
import os.path
from typing import Any
from .tool_entity import ToolEntity
from pydantic import BaseModel,Field
from internal.lib.helper import dynamic_import

class ProviderEntity(BaseModel):
    """服務提供商實體，映射的資料是providers.yaml裡的每條紀錄"""
    name: str # 名字
    label: str # 標籤，展示給前端顯示的
    description: str # 描述
    icon: str # 圖標地址
    background: str # 圖標的顏色
    category: str # 分類資訊
    created_at: int = 0 # 提供商/工具的創建時間


class Provider(BaseModel):
    """服務提供商，在該類下，可以獲取到該服務提供商的所有工具，描述，圖標等多個資訊"""
    name: str # 服務提供商的名字
    position: int # 服務提供商的順序
    provider_entity: ProviderEntity # 服務提供商實體
    tool_entity_map: dict[str, ToolEntity] = Field(default_factory=dict) # 工具實體映射表
    tool_func_map: dict[str, Any] = Field(default_factory=dict) # 工具函數映射表

    def __init__(self, **kwargs):
        """構造函數，完成對應服務提供商的初始化"""
        super().__init__(**kwargs)
        self._provider_init()


    def get_tool(self, tool_name: str) -> Any:
        """根據工具的名字，來獲取到該服務提供商下的指定工具"""
        return self.tool_func_map.get(tool_name)

    def get_tool_entity(self, tool_name: str) -> ToolEntity:
        """根據工具的名字，來獲取到該服務提供商下的指定工具的實體/資訊"""
        return self.tool_entity_map.get(tool_name)

    def get_tool_entities(self) -> list[ToolEntity]:
        """獲取該服務提供商下的所有工具實體/資訊列表"""
        return list(self.tool_entity_map.values())

    def _provider_init(self):
        """服務提供商初始化函數"""
        # 1. 獲取當前類的路徑，計算得到對應服務提供商的地址/路徑
        current_path = os.path.abspath(__file__)
        entities_path = os.path.dirname(current_path)
        provider_path = os.path.join(os.path.dirname(entities_path), "providers", self.name)

        # 2. 組裝獲取positions.yaml資料
        positions_yaml_path = os.path.join(provider_path, "positions.yaml")
        with open(positions_yaml_path, encoding="utf-8") as f:
            positions_yaml_data = yaml.safe_load(f)

        # 3. 循環讀取位置資訊獲取服務提供商的工具名字
        for tool_name in positions_yaml_data:
            # 4. 獲取工具的yaml資料
            tool_yaml_path = os.path.join(provider_path, f"{tool_name}.yaml")
            with open(tool_yaml_path, encoding="utf-8") as f:
                tool_yaml_data = yaml.safe_load(f)

            # 5. 將工具資訊實體復植填充到tool_entity_map中
            self.tool_entity_map[tool_name] = ToolEntity(**tool_yaml_data)

            # 6. 動態導入對應的工具並填充到tool_func_map中
            self.tool_func_map[tool_name] = dynamic_import(
                f"internal.core.tools.builtin_tools.providers.{self.name}",
                tool_name,
            )