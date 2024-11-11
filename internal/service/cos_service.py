#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2024/10/22 上午10:26
@Author : www.mingerzeng@gmail.com
@File : cos_service.py
"""
import hashlib
import os
import uuid
from dataclasses import dataclass
from datetime import datetime
from .upload_file_service import UploadFileService
from injector import inject
from qcloud_cos import CosS3Client, CosConfig
from werkzeug.datastructures import FileStorage
from internal.model import UploadFile
from internal.entity.upload_file_entity import ALLOWED_IMAGE_EXTENSION, ALLOWED_DOCUMENT_EXTENSION
from internal.exception import FailException

@inject
@dataclass
class CosService:
    """cos對象存儲服務"""
    upload_file_service: UploadFileService

    def upload_file(self, file: FileStorage, only_image: bool = False) -> UploadFile:
        """上傳文件到cos對象存儲，上傳後返回文件的資訊"""
        account_id = "80c021d7-2078-e3ec-f90e-83e4389f1d46"

        # 1. 提取文件擴展名並檢測是否可以上傳
        filename = file.filename
        extension = filename.rsplit(".", 1)[-1] if "." in filename else ""
        if extension.lower() not in (ALLOWED_IMAGE_EXTENSION+ALLOWED_DOCUMENT_EXTENSION):
            raise FailException(f"該.{extension}擴展的文件不允許上傳")
        elif only_image and extension not in ALLOWED_IMAGE_EXTENSION:
            raise FailException(f"該.{extension}擴展名的文件不支持上傳，請上傳正確的圖片")

        # 2. 獲取客戶端+存儲桶名字
        client = self._get_client()
        bucket = self._get_bucket()

        # 3. 生成一個隨機的名字
        random_filename = str(uuid.uuid4()) + "." + extension
        now = datetime.now()
        upload_filename = f"{now.year}/{now.month:02d}/{now.day:02d}/{random_filename}"

        # 4. 流式讀取上傳的資料並將其上傳到cos中
        file_content = file.stream.read()

        try:
            # 5. 將資料上傳到cos存儲桶中
            client.put_object(bucket, file_content, upload_filename)
        except Exception as e:
            raise FailException("上傳文件失敗，請稍後重試")

        # 6. 創建upload_file紀錄
        return self.upload_file_service.create_upload_file(
            account_id=account_id,
            name=filename,
            key=upload_filename,
            size=len(file_content),
            extension=extension,
            mime_type=file.mimetype,
            hash=hashlib.sha3_256(file_content).hexdigest(),
        )

    def download_file(self, key: str, target_file_path: str):
        """下载cos云端的文件到本地的指定路径"""
        client = self._get_client()
        bucket = self._get_bucket()

        client.download_file(bucket, key, target_file_path)

    @classmethod
    def get_file_url(cls, key: str) -> str:
        """根据传递的cos云端key获取图片的实际URL地址"""
        cos_domain = os.getenv("COS_DOMAIN")

        if not cos_domain:
            bucket = os.getenv("COS_BUCKET")
            scheme = os.getenv("COS_SCHEME")
            region = os.getenv("COS_REGION")
            cos_domain = f"{scheme}://{bucket}.cos.{region}.myqcloud.com"

        return f"{cos_domain}/{key}"

    @classmethod
    def _get_client(cls) -> CosS3Client:
        """獲取cos對象存儲客戶端"""
        conf = CosConfig(
            Region=os.getenv("COS_REGION"),
            SecretId=os.getenv("COS_SECRET_ID"),
            SecretKey=os.getenv("COS_SECRET_KEY"),
            Token=None,
            Scheme=os.getenv("COS_SCHEME","https")
        )
        return CosS3Client(conf)

    @classmethod
    def _get_bucket(cls) -> str:
        """獲取存儲桶的名字"""
        return os.getenv("COS_BUCKET")