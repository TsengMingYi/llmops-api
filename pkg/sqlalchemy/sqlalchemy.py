#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2024/8/13 下午3:43
@Author : www.mingerzeng@gmail.com
@File : sqlalchemy.py
"""

from contextlib import contextmanager
from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy

class SQLAlchemy(_SQLAlchemy):
    """重寫Flask-SQLAlchemy中的核心類，實現自動提交"""

    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e
