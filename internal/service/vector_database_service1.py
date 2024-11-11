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
# from langchain_weaviate import WeaviateVectorStore
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from .embeddings_service import EmbeddingsService
# from weaviate import WeaviateClient
# import weaviate
# from weaviate.auth import AuthApiKey


@inject
class VectorDatabaseService1:
    """向量資料庫服務"""
    client: QdrantClient
    vector_store: QdrantVectorStore
    embeddings_service: EmbeddingsService

    def __init__(self, embeddings_services: EmbeddingsService):
        """構造函數，完成向量資料庫服務的客戶端+LangChain向量資料庫實例的創建"""

        # 1.赋值embeddings_service
        self.embeddings_service = embeddings_services

        # 2. 創建/連接weaviate向量資料庫
        self.client = QdrantClient(
            url="https://2958b366-6c1e-496f-96df-abfc43c8dba3.us-east4-0.gcp.cloud.qdrant.io",
            api_key="ThwdEgLSis6wmVRaZ_oAu06angN-IUXScd9nEFSx4qlKK2FPEhbr2A"
        )

        # 3. 創建LangChain向量資料庫
        self.vector_store = QdrantVectorStore(
            client=self.client,
            collection_name="Dataset",
            embedding=self.embeddings_service.embeddings
        )


    def get_retriever(self) -> VectorStoreRetriever:
        """獲取檢索器"""
        return self.vector_store.as_retriever()

    @classmethod
    def combine_documents(cls, documents: list[Document]) -> str:
        """將對應的文檔列表使用換行符進行合併"""
        return "\n\n".join([document.page_content for document in documents])