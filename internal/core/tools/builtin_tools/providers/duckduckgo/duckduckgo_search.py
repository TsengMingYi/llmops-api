#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2024/9/16 上午9:06
@Author : www.mingerzeng@gmail.com
@File : duckduckgo_search.py
"""
from langchain_core.tools import BaseTool
from langchain_core.pydantic_v1 import BaseModel,Field
from langchain_community.tools import DuckDuckGoSearchRun
from internal.lib.helper import add_attribute

class DDGInput(BaseModel):
    query: str = Field(description="需要搜索的查詢語句")

@add_attribute("args_schema", DDGInput)
def duckduckgo_search(**kwargs) -> BaseTool:
    """返回DuckDuckGo搜索工具"""
    return DuckDuckGoSearchRun(
        description="一個注重隱私的搜索工具，當你需要搜索時事時可以使用該工具，工具的輸入是一個查詢語句",
        args_schema=DDGInput,
    )