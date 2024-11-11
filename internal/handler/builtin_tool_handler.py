#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2024/9/16 上午10:03
@Author : www.mingerzeng@gmail.com
@File : builtin_tool_handler.py
"""
import io

from injector import inject
from dataclasses import dataclass
from flask import send_file
from internal.service import BuiltinToolService
from pkg.response import success_json

@inject
@dataclass
class BuiltinToolHandler:
    """內置工具處理器"""
    builtin_tool_service: BuiltinToolService

    def get_builtin_tools(self):
        """獲取LLMOps所有內置工具資訊+提供商資訊"""
        builtin_tools = self.builtin_tool_service.get_builtin_tools()
        return success_json(builtin_tools)

    def get_provider_tool(self, provider_name: str, tool_name: str):
        """根據傳遞的提供商名字+工具名字獲取指定工具的資訊"""
        builtin_tool = self.builtin_tool_service.get_provider_tool(provider_name, tool_name)
        return success_json(builtin_tool)

    def get_provider_icon(self,provider_name: str):
        """根據傳遞的提供商獲取icon圖標流資訊"""
        icon , mimetype = self.builtin_tool_service.get_provider_icon(provider_name)
        return send_file(io.BytesIO(icon), mimetype)

    def get_categories(self):
        """獲取所有內置提供商的分類資訊"""
        categories = self.builtin_tool_service.get_categories()
        return success_json(categories)

