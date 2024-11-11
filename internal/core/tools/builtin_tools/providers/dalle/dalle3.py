#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2024/9/16 上午9:23
@Author : www.mingerzeng@gmail.com
@File : dalle3.py
"""
from langchain_community.tools.openai_dalle_image_generation import OpenAIDALLEImageGenerationTool
from langchain_core.tools import BaseTool
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_community.utilities.dalle_image_generator import DallEAPIWrapper
from internal.lib.helper import add_attribute

class Dalle3ArgsSchema(BaseModel):
    query: str = Field(description="輸入應該是生成圖像的文本提示(prompt)")

@add_attribute("args_schema", Dalle3ArgsSchema)
def dalle3(**kwargs) -> BaseTool:
    """返回dalle3繪圖的LangChain工具"""
    return OpenAIDALLEImageGenerationTool(
        api_wrapper=DallEAPIWrapper(model="dall-e-3",**kwargs),
        args_schema=Dalle3ArgsSchema,
    )
