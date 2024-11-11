#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2024/9/16 上午9:42
@Author : www.mingerzeng@gmail.com
@File : wikipedia_search.py
"""
from langchain_community.tools.wikipedia.tool import WikipediaQueryInput, WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_core.tools import BaseTool
from internal.lib.helper import add_attribute


@add_attribute("args_schema", WikipediaQueryInput)
def wikipedia_search(**kwargs) -> BaseTool:
    """返回維基百科搜索工具"""
    return WikipediaQueryRun(
        api_wrapper=WikipediaAPIWrapper(),
    )

