#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2024/8/11 2:10 上午
@Author : www.mingerzeng@gmail.com
@File : http.py
"""
import logging

from flask import Flask
from flask_cors import CORS
from internal.exception import CustomException
from internal.router import Router
from config import Config
from pkg.response import json, Response,HttpCode
from pkg.sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from internal.model import App
from internal.extension import logging_extension,redis_extension, celery_extension

class Http(Flask):
    """Http服務引擎"""

    def __init__(self, *args, conf: Config,db : SQLAlchemy, migrate : Migrate,router: Router, **kwargs):

        # 1. 調用父類別構造函數初始化
        super().__init__(*args, **kwargs)

        # 2. 初始化應用配置
        self.config.from_object(conf)

        # 3. 註冊綁定異常錯誤處理
        self.register_error_handler(Exception,self._register_error_handler)

        # 4. 初始化flask擴展
        db.init_app(self)
        migrate.init_app(self,db,directory="internal/migration")
        redis_extension.init_app(self)
        celery_extension.init_app(self)
        logging_extension.init_app(self)

        # 5. 解決前後端跨域問題
        CORS(self, resources={
            r"/*": {
                "origins": "*",
                "supports_credentials": True,
                # "methods": ["GET","POST"],
                # "allow_headers": ["Content-Type"]
            }
        })

        # 5. 註冊應用路由
        router.register_router(self)

    def _register_error_handler(self , error : Exception):
        # 1. 日誌紀錄異常資訊
        logging.error("An error occurred: %s", error, exc_info=True)

        # 2. 異常資料是不是我們的自定義異常，如果是可以提取message和code等資訊
        if isinstance(error,CustomException):
            return json(Response(
                code=error.code,
                message=error.message,
                data=error.data if error.data is not None else {},
            ))
        # 3. 如果不是我們的自定義異常，則有可能是程式，資料庫拋出的異常，也可以提取資訊，設置為FAIl狀態碼
        if self.debug:
            raise error
        else:

            return json(Response(
                code=HttpCode.FAIL,
                message=str(error),
                data={},
            ))
