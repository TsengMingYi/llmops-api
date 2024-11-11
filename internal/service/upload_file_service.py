#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2024/10/22 上午10:47
@Author : www.mingerzeng@gmail.com
@File : upload_file_service.py
"""

from injector import inject
from dataclasses import dataclass
from .base_service import BaseService
from pkg.sqlalchemy import SQLAlchemy
from internal.model import UploadFile

@inject
@dataclass
class UploadFileService(BaseService):
    """上傳文件紀錄服務"""
    db: SQLAlchemy

    def create_upload_file(self, **kwargs) -> UploadFile:
        """創建文件上傳紀錄"""
        return self.create(UploadFile, **kwargs)