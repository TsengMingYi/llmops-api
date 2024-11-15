#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2024/11/11 上午2:59
@Author : www.mingerzeng@gmail.com
@File : dataset_service.py
"""
from dataclasses import dataclass
from uuid import UUID

from injector import inject
from sqlalchemy import desc

from pkg.sqlalchemy import SQLAlchemy
from .base_service import BaseService
from internal.schema.dataset_schema import CreateDatasetReq, UpdateDatasetReq,GetDatasetsWithPageReq
from internal.model import Dataset
from internal.exception import ValidationException, NotFoundException
from internal.entity.dataset_entity import DEFAULT_DATASET_DESCRIPTION_FORMATTER
from pkg.paginator import Paginator

@inject
@dataclass
class DatasetService(BaseService):
    """知识库服务"""
    db: SQLAlchemy

    def create_dataset(self, req: CreateDatasetReq) -> Dataset:
        """根据传递的请求信息创建知识库"""
        account_id = "308503ab-a857-db34-3bce-a2a075bd697e"
        # 1.检测该账号下是否存在同名知识库
        dataset = self.db.session.query(Dataset).filter_by(
            account_id=account_id,
            name=req.name.data,
        ).one_or_none()
        if dataset:
            raise ValidationException(f"该知识库{req.name.data}已存在")

        # 2.检测是否传递了描述信息，如果没有传递需要补充上
        if req.description.data is None or req.description.data.strip() == "":
            req.description.data = DEFAULT_DATASET_DESCRIPTION_FORMATTER.format(name=req.name.data)

        # 3. 創建知識庫紀錄並返回
        return self.create(
            Dataset,
            account_id=account_id,
            name=req.name.data,
            icon=req.icon.data,
            description=req.description.data,
        )

    def get_dataset(self, dataset_id: UUID) -> Dataset:
        """根据传递的知识库id获取知识库记录"""
        account_id = "308503ab-a857-db34-3bce-a2a075bd697e"
        dataset = self.get(Dataset, dataset_id)
        if dataset is None or str(dataset.account_id) != account_id:
            raise NotFoundException("该知识库不存在")

        return dataset

    def update_dataset(self, dataset_id: UUID, req: UpdateDatasetReq) -> Dataset:
        """根据传递的知识库id+数据更新知识库"""
        account_id = "308503ab-a857-db34-3bce-a2a075bd697e"

        # 1.检测知识库是否存在并校验
        dataset = self.get(Dataset, dataset_id)
        if dataset is None or str(dataset.account_id) != account_id:
            raise NotFoundException("该知识库不存在")

        # 2.检测修改后的知识库名称是否出现重名
        check_dataset = self.db.session.query(Dataset).filter(
            Dataset.account_id == account_id,
            Dataset.name == req.name.data,
            Dataset.id != dataset_id,
        ).one_or_none()
        if check_dataset:
            raise ValidationException(f"该知识库名称{req.name.data}已存在，请修改")

        # 3.校验描述信息是否为空，如果为空则人为设置
        if req.description.data is None or req.description.data.strip() == "":
            req.description.data = DEFAULT_DATASET_DESCRIPTION_FORMATTER.format(name=req.name.data)

        # 4.更新数据
        self.update(
            dataset,
            name=req.name.data,
            icon=req.icon.data,
            description=req.description.data,
        )

        return dataset

    def get_datasets_with_page(self, req: GetDatasetsWithPageReq) -> tuple[list[Dataset], Paginator]:
        """根据传递的信息获取知识库列表分页数据"""
        account_id = "308503ab-a857-db34-3bce-a2a075bd697e"

        # 1.构建分页查询器
        paginator = Paginator(db=self.db, req=req)

        # 2.构建筛选器
        filters = [Dataset.account_id == account_id]
        if req.search_word.data:
            filters.append(Dataset.name.ilike(f"%{req.search_word.data}%"))

        # 3.执行分页并获取数据
        datasets = paginator.paginate(
            self.db.session.query(Dataset).filter(*filters).order_by(desc("created_at"))
        )

        return datasets, paginator