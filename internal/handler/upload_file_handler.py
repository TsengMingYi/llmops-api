#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2024/10/21 上午10:24
@Author : www.mingerzeng@gmail.com
@File : upload_file_handler.py
"""
from injector import inject
from dataclasses import dataclass
from internal.schema.upload_file_schema import UploadFileReq, UploadFileResp, UploadImageReq
from pkg.response import validate_error_json, success_json
from internal.service import CosService

@inject
@dataclass
class UploadFileHandler:
    """上傳文件處理器"""
    cos_service: CosService

    def upload_file(self):
        """上傳文件/文檔"""
        # 1. 構建請求並校驗
        req = UploadFileReq()
        if not req.validate():
            return validate_error_json(req.errors)

        # 2. 調用服務上傳文件並獲取紀錄
        upload_file = self.cos_service.upload_file(req.file.data)

        # 3. 構建響應並返回
        resp = UploadFileResp()
        return success_json(resp.dump(upload_file))

    def upload_image(self):
        """上传图片"""
        # 1.构建请求并校验
        req = UploadImageReq()
        if not req.validate():
            return validate_error_json(req.errors)

        # 2.调用服务并上传文件
        upload_file = self.cos_service.upload_file(req.file.data, True)

        # 3.获取图片的实际URL地址
        image_url = self.cos_service.get_file_url(upload_file.key)

        return success_json({"image_url": image_url})
