#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2024/8/11 2:14 上午
@Author : www.mingerzeng@gmail.com
@File : app.py
"""
from flask_cors import CORS
from flask_migrate import Migrate
from injector import Injector
from internal.router import Router
from internal.server.http import Http
import dotenv
from config import Config
from .module import ExtensionModule
from .module import injector
from pkg.sqlalchemy import SQLAlchemy

# 將env加載到環境變量中
dotenv.load_dotenv()

conf = Config()


app = Http(__name__, conf=conf, db=injector.get(SQLAlchemy),migrate=injector.get(Migrate),router=injector.get(Router))
# CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

celery = app.extensions["celery"]

if __name__ == "__main__":
    app.run(debug=True)

