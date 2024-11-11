#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2024/8/12 上午9:33
@Author : www.mingerzeng@gmail.com
@File : app_schema.py
"""

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length

class CompletionReq(FlaskForm):
    """基礎聊天接口請求驗證"""
    # 必填 ，長度最大為2000
    query = StringField('query',validators=[
        DataRequired(message="用戶的提問是必填"),
        Length(max=2000,message="用戶的提問最大長度是2000")
    ])