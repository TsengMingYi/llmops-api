#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2024/8/13 下午2:16
@Author : www.mingerzeng@gmail.com
@File : app_service.py
"""

import uuid
from pkg.sqlalchemy import SQLAlchemy
from dataclasses import dataclass
from injector import inject
from internal.model import App


@inject
@dataclass
class AppService:
    """應用服務邏輯"""
    db : SQLAlchemy

    def create_app(self) -> App:
        with self.db.auto_commit():
            # 1. 創建模型的實體類
            app = App(name="測試機器人",account_id=uuid.uuid4(),icon="",description="這是一個簡單的聊天機器人")
            # 2. 將實體類添加到session會話中
            self.db.session.add(app)
        return app

    def get_app(self, id : uuid.UUID) -> App:
        app = self.db.session.query(App).get(id)
        return app

    def update_app(self, id : uuid.UUID) -> App:
        with self.db.auto_commit():
            app = self.get_app(id)
            app.name = "自製聊天機器人"
        return app

    def delete_app(self, id : uuid.UUID) -> App:
        with self.db.auto_commit():
            app = self.get_app(id)
            self.db.session.delete(app)
        return app