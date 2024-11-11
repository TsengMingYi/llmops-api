#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2024/9/16 上午2:25
@Author : www.mingerzeng@gmail.com
@File : builtin_provider_manager.py
"""

import yaml
import os.path
from pydantic import BaseModel, Field
from typing import Any
from injector import inject, singleton
from internal.core.tools.builtin_tools.entities import ProviderEntity, Provider

@inject
@singleton
class BuiltinProviderManager(BaseModel):
    """服務提供商工廠類"""
    provider_map: dict[str, Provider] = Field(default_factory=dict)

    def __init__(self, **kwargs):
        """構造函數，初始化對應的provider_tool_map"""
        super().__init__(**kwargs)
        self._get_provider_tool_map()

    def get_provider(self, provider_name: str) -> Provider:
        """根據傳遞的名字來獲取服務提供商"""
        return self.provider_map.get(provider_name)

    def get_providers(self) -> list[Provider]:
        """獲取所有服務提供商列表"""
        return list(self.provider_map.values())

    def get_provider_entities(self) -> list[ProviderEntity]:
        """獲取所有服務提供商實體列表資訊"""
        return [provider.provider_entity for provider in self.provider_map.values()]

    def get_tool(self, provider_name: str, tool_name: str) -> Any:
        """根據服務提供商的名字+工具名字，來獲取特定的工具實體"""
        provider = self.get_provider(provider_name)
        if provider is None:
            return None
        return provider.get_tool(tool_name)

    def _get_provider_tool_map(self):
        """專案初始化的時候獲取服務提供商，工具的映射關係並填充provider_tool_map"""
        # 1. 檢測provider_tool_map是否為空
        if self.provider_map:
            return

        # 2. 獲取當前文件/類所在的文件夾路徑
        current_path = os.path.abspath(__file__)
        providers_path = os.path.dirname(current_path)
        providers_yaml_path = os.path.join(providers_path, "providers.yaml")

        # 3. 讀取providers.yaml的資料
        with open(providers_yaml_path, encoding="utf-8") as f:
            providers_yaml_data = yaml.safe_load(f)

        # 4. 循環遍歷providers.yaml的資料
        for idx, provider_data in enumerate(providers_yaml_data):
            provider_entity = ProviderEntity(**provider_data)
            self.provider_map[provider_entity.name] = Provider(
                name=provider_entity.name,
                position=idx + 1,
                provider_entity=provider_entity
            )