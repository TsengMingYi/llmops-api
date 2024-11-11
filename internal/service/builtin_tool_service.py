#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2024/9/16 上午10:11
@Author : www.mingerzeng@gmail.com
@File : builtin_tool_service.py
"""
import mimetypes
import os.path
from typing import Any

from injector import inject
from internal.exception import NotFoundException
from dataclasses import dataclass
from flask import current_app
from langchain_core.pydantic_v1 import BaseModel
from internal.core.tools.builtin_tools.providers import BuiltinProviderManager
from internal.core.tools.builtin_tools.categories import BuiltinCategoryManager

@inject
@dataclass
class BuiltinToolService:
    """內置工具服務"""
    builtin_provider_manager: BuiltinProviderManager
    builtin_category_manager: BuiltinCategoryManager

    def get_builtin_tools(self) -> list:
        """獲取LLMOps專案中的所有內置提供商+工具對應的資訊"""
        # 1. 獲取所有的提供商
        providers = self.builtin_provider_manager.get_providers()

        # 2. 遍歷所有的提供商並提取工具資訊
        builtin_tools = []
        for provider in providers:
            provider_entity = provider.provider_entity
            builtin_tool = {
                **provider_entity.model_dump(exclude=["icon"]),
                "tools": [],
            }

            # 3. 循環遍歷提取提供者的所有工具實體
            for tool_entity in provider.get_tool_entities():
                # 4. 從提供者中獲取工具函數
                tool = provider.get_tool(tool_entity.name)

                # 5. 構建工具實體資訊
                tool_dict = {
                    **tool_entity.model_dump(),
                    "inputs": self.get_tool_inputs(tool),
                }

                builtin_tool["tools"].append(tool_dict)

            builtin_tools.append(builtin_tool)

        return builtin_tools

    def get_provider_tool(self, provider_name: str, tool_name: str) -> dict:
        """根據傳遞的提供者名字+工具名字獲取指定工具資訊"""
        # 1. 獲取內置的提供商
        provider = self.builtin_provider_manager.get_provider(provider_name)
        if provider is None:
            raise NotFoundException(f"該提供商{provider_name}不存在")

        # 2. 獲取該提供商下對應的工具
        tool_entity = provider.get_tool_entity(tool_name)
        if tool_entity is None:
            raise NotFoundException(f"該工具{tool_name}不存在")

        # 3. 組裝提供商和工具實體資訊
        provider_entity = provider.provider_entity
        tool = provider.get_tool(tool_name)

        builtin_tool = {
            "provider": {**provider_entity.model_dump(exclude=["icon", "created_at"])},
            **tool_entity.model_dump(),
            "created_at": provider_entity.created_at,
            "inputs": self.get_tool_inputs(tool)
        }

        return builtin_tool

    def get_provider_icon(self, provider_name: str) -> tuple[bytes, str]:
        """根據傳遞的提供者名字獲取icon流資訊"""
        # 1. 獲取對應的工具提供者
        provider = self.builtin_provider_manager.get_provider(provider_name)
        if not provider:
            raise NotFoundException(f"該工具提供者{provider_name}不存在")

        # 2. 獲取專案的根路徑資訊
        root_path = os.path.dirname(os.path.dirname(current_app.root_path))

        # 3. 拼接得到提供者所在的文件夾
        provider_path = os.path.join(
            root_path,
            "internal", "core" , "tools" , "builtin_tools" , "providers" , provider_name ,
        )

        # 4. 拼接得到icon對應的路徑
        icon_path = os.path.join(provider_path, "_asset", provider.provider_entity.icon)

        # 5. 檢測icon是否存在
        if not os.path.exists(icon_path):
            raise NotFoundException(f"該工具提供者_asset下未提供圖標")

        # 6. 讀取icon的類型
        mimetype, _ = mimetypes.guess_type(icon_path)
        mimetype = mimetype or "application/octet-stream"

        # 7. 讀取icon的字節資料
        with open(icon_path, "rb") as f:
            byte_data = f.read()
            return byte_data, mimetype

    def get_categories(self) -> list[str, Any]:
        """獲取所有的內置分類資訊，涵蓋了category，name，icon"""
        category_map = self.builtin_category_manager.get_category_map()
        return [{
            "name": category["entity"].name,
            "category": category["entity"].category,
            "icon": category["icon"],
        } for category in category_map.values()]

    @classmethod
    def get_tool_inputs(cls, tool) -> list:
        """根據傳入的工具獲取inputs資訊"""
        inputs = []
        if hasattr(tool, "args_schema") and issubclass(tool.args_schema, BaseModel):
            for field_name, model_field in tool.args_schema.__fields__.items():
                inputs.append({
                    "name": field_name,
                    "description": model_field.field_info.description or "",
                    "required": model_field.required,
                    "type": model_field.outer_type_.__name__,
                })
            return inputs

