#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2024/10/21 上午10:44
@Author : www.mingerzeng@gmail.com
@File : upload_file_schema.py
"""
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed, FileSize
from internal.entity.upload_file_entity import ALLOWED_DOCUMENT_EXTENSION, ALLOWED_IMAGE_EXTENSION
from marshmallow import Schema, fields, pre_dump
from internal.model import UploadFile

class UploadFileReq(FlaskForm):
    """上傳文件請求"""
    file = FileField("file", validators=[
        FileRequired("上傳文件不能為空"),
        FileSize(max_size=15*1024*1024, message="上傳文件最大不能超過15MB"),
        FileAllowed(ALLOWED_DOCUMENT_EXTENSION,message=f"僅允許上傳{'/'.join(ALLOWED_DOCUMENT_EXTENSION)}")
    ])

class UploadFileResp(Schema):
    """上傳文件接口響應接口"""
    id = fields.UUID(dump_default="")
    account_id = fields.UUID(dump_default="")
    name = fields.String(dump_default="")
    key = fields.String(dump_default="")
    size = fields.Integer(dump_default=0)
    extension = fields.String(dump_default="")
    mime_type = fields.String(dump_default="")
    created_at = fields.Integer(dump_default=0)

class UploadImageReq(FlaskForm):
    """上传图片请求结构体"""
    file = FileField("file", validators=[
        FileRequired("上传图片不能为空"),
        FileSize(max_size=15 * 1024 * 1024, message="上传图片最大不能超过15MB"),
        FileAllowed(ALLOWED_IMAGE_EXTENSION, message=f"仅允许上传{'/'.join(ALLOWED_IMAGE_EXTENSION)}文件")
    ])

    @pre_dump
    def process_data(self, data: UploadFile, **kwargs):
        return {
            "id": data.id,
            "account_id": data.account_id,
            "name": data.name,
            "key": data.key,
            "size": data.size,
            "extension": data.extension,
            "mime_type": data.mime_type,
            "created_at": int(data.created_at.timestamp()),
        }

