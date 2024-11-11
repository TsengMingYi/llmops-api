#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2024/9/16 上午2:46
@Author : www.mingerzeng@gmail.com
@File : tool_entity.py
"""
from enum import Enum
from typing import Optional, Any
from pydantic import BaseModel, Field

class ToolParamType(str, Enum):
    """工具參數類型枚舉類"""
    STRING = "string"
    NUMBER = "number"
    BOOLEAN = "boolean"
    SELECT = "select"

class ToolParam(BaseModel):
    """工具參數類型"""
    name: str # 參數的實際名字
    label: str # 參數的展示標籤
    type: ToolParamType # 參數的類型
    required: bool = False # 是否必填
    default: Optional[Any] = None # 默認值
    min: Optional[float] = None # 最小值
    max: Optional[float] = None # 最大值
    options: list[dict[str, Any]] = Field(default_factory=list) # 下拉菜單選項列表

class ToolEntity(BaseModel):
    """工具實體類，存儲的資訊映射的是工具名.yaml裡的資料"""
    name: str # 工具名字
    label: str # 工具標籤
    description: str # 工具描述
    params: list[ToolParam] = Field(default_factory=list) # 工具的參數資訊