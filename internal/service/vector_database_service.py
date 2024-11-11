#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2024/9/2 下午4:57
@Author : www.mingerzeng@gmail.com
@File : vector_database_service.py
"""
import os

from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_openai import OpenAIEmbeddings
from injector import inject
from langchain_weaviate import WeaviateVectorStore
from weaviate import WeaviateClient
import weaviate
from weaviate.auth import AuthApiKey


@inject
class VectorDatabaseService:
    """向量資料庫服務"""
    client: WeaviateClient
    vector_store: WeaviateVectorStore

    def __init__(self):
        """構造函數，完成向量資料庫服務的客戶端+LangChain向量資料庫實例的創建"""
        # 1. 創建/連接weaviate向量資料庫
        self.client = weaviate.connect_to_wcs(
            skip_init_checks=True,
            # cluster_url="https://1cwbsxhorsetiynee05qjw.c0.us-west3.gcp.weaviate.cloud",
            # auth_credentials=AuthApiKey(os.environ.get("AUTH_API_KEY")),
            auth_credentials=AuthApiKey(os.getenv("AUTH_API_KEY")),
            # cluster_url=os.environ.get("WEAVIATE_HOST"),
            cluster_url=os.getenv("WEAVIATE_HOST"),
            # auth_credentials=os.getenv("AUTH_API_KEY")
        )

        # 2. 創建LangChain向量資料庫
        self.vector_store = WeaviateVectorStore(
            client=self.client,
            index_name="Dataset",
            text_key="text",
            embedding=OpenAIEmbeddings(model="text-embedding-3-small")
        )


    def get_retriever(self) -> VectorStoreRetriever:
        """獲取檢索器"""
        return self.vector_store.as_retriever()

    @classmethod
    def combine_documents(cls, documents: list[Document]) -> str:
        """將對應的文檔列表使用換行符進行合併"""
        return "\n\n".join([document.page_content for document in documents])