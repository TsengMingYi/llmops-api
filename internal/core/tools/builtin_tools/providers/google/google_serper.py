#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2024/9/16 上午2:15
@Author : www.mingerzeng@gmail.com
@File : google_serper.py
"""
from langchain_core.tools import BaseTool
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_community.tools import GoogleSerperRun
from langchain_core.pydantic_v1 import BaseModel, Field
from internal.lib.helper import add_attribute

class GoogleSerperArgsSchema(BaseModel):
    """google serper API search 參數描述"""
    query: str = Field(description="需要檢索查詢的語句.")

@add_attribute("args_schema", GoogleSerperArgsSchema)
def google_serper(**kwargs) -> BaseTool:
    """google Serper搜索"""
    return GoogleSerperRun(
        name="google_serper",
        description="這是一個低成本的google search API，當你需要搜索時事的時候，可以使用該工具，該工具的輸入是一個查詢語句",
        args_schema=GoogleSerperArgsSchema,
        api_wrapper=GoogleSerperAPIWrapper(),
    )