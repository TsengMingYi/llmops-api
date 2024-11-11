#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2024/8/12 上午10:16
@Author : www.mingerzeng@gmail.com
@File : response.py
"""
from dataclasses import field , dataclass
from .http_code import HttpCode
from typing import Any, Union, Generator
from flask import jsonify, stream_with_context, Response as FlaskResponse


@dataclass
class Response:
    """基礎HTTP接口響應格式"""
    code : HttpCode.SUCCESS
    message : str = ""
    data : Any = field(default_factory=dict)

def json(data : Response = None):
    """基礎的響應接口"""
    response = jsonify(data)
    # 添加跨域響應Header
    # response.headers['Access-Control-Allow-Origin'] = 'http://localhost:5173'
    # response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    # response.headers['Access-Control-Allow-Methods'] = 'GET, POST,OPTIONS'
    # response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response, 200

def success_json(data : Response = None):
    """成功資料響應"""
    return json(Response(code=HttpCode.SUCCESS,message="",data=data))

def fail_json(data : Response = None):
    """失敗資料響應"""
    return json(Response(code=HttpCode.FAIL, message="", data=data))

def validate_error_json(errors : dict = None):
    """資料驗證錯誤響應"""
    first_key = next(iter(errors))
    if first_key is not None:
        msg = errors.get(first_key)[0]
    else:
        msg = ""
    return json(Response(code=HttpCode.VALIDATE_ERROR, message=msg, data=errors))

def message(code : HttpCode = None, msg : str = ""):
    """基礎的信息響應,固定返回消息提示，資料固定為空字典"""
    return json(Response(code=code,message=msg,data={}))

def success_message(msg : str = ""):
    """成功的消息響應"""
    return message(code=HttpCode.SUCCESS,msg=msg)

def fail_message(msg : str = ""):
    """失敗的消息響應"""
    return message(code=HttpCode.FAIL,msg=msg)

def not_found_message(msg : str = ""):
    """未找到消息響應"""
    return message(code=HttpCode.NOT_FOUND,msg=msg)

def unauthorized_message(msg : str = ""):
    """未授權消息響應"""
    return message(code=HttpCode.UNAUTHORIZED,msg=msg)

def forbidden_message(msg : str = ""):
    """無權限消息響應"""
    return message(code=HttpCode.FORBIDDEN,msg=msg)

def compact_generate_response(response: Union[Response, Generator]) -> FlaskResponse:
    """統一合併處理塊輸出以及流式事件輸出"""
    # 1. 檢測下是否為塊輸出(Response)
    if isinstance(response, Response):
        return json(response)
    else:
        # 2. response格式為生成器，代表本次響應需要執行流式事件輸出
        def generate() -> Generator:
            """構建generate函數，流式從response中獲取資料"""
            yield from response

        # 3. 返回攜帶上下文的流式事件輸出
        return FlaskResponse(
            stream_with_context(generate()),
            status=200,
            mimetype="text/event-stream",
        )