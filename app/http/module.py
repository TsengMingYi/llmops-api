#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2024/8/13 下午1:42
@Author : www.mingerzeng@gmail.com
@File : module.py
"""
from pkg.sqlalchemy import SQLAlchemy
from injector import Module, Binder, Injector
from flask_migrate import Migrate
from internal.extension.migrate_extension import migrate
from internal.extension.redis_extension import redis_client
from internal.extension.database_extension import db
from redis import Redis


class ExtensionModule(Module):
    """擴展模塊的依賴注入"""

    def configure(self, binder: Binder) -> None:
        binder.bind(SQLAlchemy,to=db)
        binder.bind(Migrate,to=migrate)
        binder.bind(Redis, to=redis_client)


injector = Injector([ExtensionModule])