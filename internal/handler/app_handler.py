#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2024/8/11 1:57 上午
@Author : www.mingerzeng@gmail.com
@File : app_handler.py
"""
import json
from queue import Queue
from dataclasses import dataclass
import uuid
from operator import itemgetter
from threading import Thread
from typing import Dict, Any, Literal, Generator
from uuid import UUID
from injector import inject
from langchain_core.memory import BaseMemory
from langchain_core.tracers import Run
from langgraph.constants import END
from langgraph.graph import MessagesState, StateGraph

from internal.schema.app_schema import CompletionReq
from pkg.response import success_json,validate_error_json,success_message, compact_generate_response
from internal.exception import FailException
from internal.service import AppService, VectorDatabaseService,VectorDatabaseService1
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferWindowMemory
from langchain_community.chat_message_histories import FileChatMessageHistory
from langchain_core.runnables import RunnablePassthrough, RunnableLambda, RunnableConfig
from langchain_core.output_parsers import StrOutputParser
from internal.task.demo_task import demo_task
from internal.service import ApiToolService
from internal.core.tools.builtin_tools.providers import BuiltinProviderManager
from langchain_core.messages import ToolMessage

@inject
@dataclass
class AppHandler:
    """應用控制器"""
    app_service : AppService
    vector_database_service: VectorDatabaseService1
    builtin_provider_manager: BuiltinProviderManager
    api_tool_service: ApiToolService

    def create_app(self):
        """調用服務創建新的App紀錄"""
        app = self.app_service.create_app()
        return success_message(f"應用已經成功創建，id為{app.id}")

    def get_app(self, id : uuid.UUID):
        app = self.app_service.get_app(id)
        return success_message(f"應用已經成功獲取，名字是{app.name}")

    def update_app(self, id : uuid.UUID):
        app = self.app_service.update_app(id)
        return success_message(f"應用已經成功修改，修改的名字是{app.name}")

    def delete_app(self, id : uuid.UUID):
        app = self.app_service.delete_app(id)
        return success_message(f"應用已經成功刪除，id為{app.id}")

    @classmethod
    def _load_memory_variables(cls, input: Dict[str, Any], config: RunnableConfig) -> Dict[str, Any]:
        """加載記憶變量資訊"""
        # 1. 從config中獲取configurable
        configurable = config.get("configurable", {})
        configurable_memory = configurable.get("memory", None)
        if configurable_memory is not None and isinstance(configurable_memory, BaseMemory):
            return configurable_memory.load_memory_variables(input)
        return {"history": []}

    @classmethod
    def _save_context(cls, run_obj: Run, config: RunnableConfig) -> None:
        """存儲對應的上下文資訊到記憶實體中"""
        configurable = config.get("configurable", {})
        configurable_memory = configurable.get("memory", None)
        if configurable_memory is not None and isinstance(configurable_memory, BaseMemory):
            configurable_memory.save_context(run_obj.inputs, run_obj.outputs)

    # def debug(self, app_id: UUID):
    #     """應用會話調適聊天接口，該接口為流式事件輸出"""
    #     # 1. 提取從接口中獲取的輸入，POST
    #     req = CompletionReq()
    #     if not req.validate():
    #         return validate_error_json(req.errors)
    #
    #     # 2. 創建隊列並提取query資料
    #     q = Queue()
    #     query = req.query.data
    #
    #     # 3. 創建graph圖程式應用
    #     def graph_app() -> None:
    #         """創建Graph圖程式應用並執行"""
    #         # 3.1 創建tools工具列表
    #         tools = [
    #             self.builtin_provider_manager.get_tool("google","google_serper")(),
    #             self.builtin_provider_manager.get_tool("dalle","dalle3")(),
    #         ]
    #
    #         # 3.2 定義大語言模型/聊天機器人節點
    #         def chatbot(state: MessagesState) -> MessagesState:
    #             """聊天機器人節點"""
    #             # 3.2.1 創建LLM大語言模型
    #             llm = ChatOpenAI(model="gpt-4o-mini",temperature=0).bind_tools(tools)
    #
    #             # 3.2.2 調用stream()函數獲取流式輸出內容，並判斷生成內容是文本還是工具調用參數
    #             is_first_chunk = True
    #             is_tool_call = False
    #             gathered = None
    #             id = str(uuid.uuid4())
    #             for chunk in llm.stream(state["messages"]):
    #                 # 3.2.3 檢測是不是第一個塊，部分LLM的第一個塊不會生成內容，需要拋棄掉
    #                 if is_first_chunk and chunk.content == "" and not chunk.tool_calls:
    #                     continue
    #
    #                 # 3.2.4 疊加相應的區塊
    #                 if is_first_chunk:
    #                     gathered = chunk
    #                     is_first_chunk = False
    #                 else:
    #                     gathered += chunk
    #
    #                 # 3.2.5 判斷是工具調用還是文本生成，往隊列中添加不同的資料
    #                 if chunk.tool_calls or is_tool_call:
    #                     is_tool_call = True
    #                     q.put({
    #                         "id": id,
    #                         "event": "agent_thought",
    #                         "data": json.dumps(chunk.tool_call_chunk),
    #                     })
    #                 else:
    #                     q.put({
    #                         "id": id,
    #                         "event": "agent_message",
    #                         "data": chunk.content
    #                     })
    #
    #             return {"messages": [gathered]}
    #
    #         # 3.3 定義工具/函數調用節點
    #         def tool_executor(state: MessagesState) -> MessagesState:
    #             """工具執行節點"""
    #             # 3.3.1 提取資料狀態中的tool_calls
    #             tool_calls = state["messages"][-1].tool_calls
    #
    #             # 3.3.2 將工具列表轉換成字典便於使用
    #             tools_by_name = {tool.name: tool for tool in tools}
    #
    #             # 3.3.3 執行工具並得到對應的結果
    #             messages = []
    #             for tool_call in tool_calls:
    #                 id = str(uuid.uuid4())
    #                 tool = tools_by_name[tool_call["name"]]
    #                 tool_result = tool.invoke(tool_call["args"])
    #                 messages.append(ToolMessage(
    #                     tool_call_id=tool_call["id"],
    #                     content=json.dumps(tool_result),
    #                     name=tool_call["name"],
    #                 ))
    #                 q.put({
    #                     "id": id,
    #                     "event": "agent_action",
    #                     "data": json.dumps(tool_result),
    #                 })
    #
    #             return {"messages": messages}
    #
    #         # 3.4 定義路由函數
    #         def route(state: MessagesState) -> Literal["tool_executor","__end__"]:
    #             """定義路由節點，用於確認下一步步驟"""
    #             ai_message = state["messages"][-1]
    #             if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0:
    #                 return "tool_executor"
    #             return END
    #
    #         # 3.5 創建狀態圖
    #         graph_builder = StateGraph(MessagesState)
    #
    #         # 3.6 添加節點
    #         graph_builder.add_node("llm", chatbot)
    #         graph_builder.add_node("tool_executor", tool_executor)
    #
    #         # 3.7 添加邊
    #         graph_builder.set_entry_point("llm")
    #         graph_builder.add_conditional_edges("llm",route)
    #         graph_builder.add_edge("tool_executor", "llm")
    #
    #         # 3.8 編譯圖程式為可運行組件
    #         graph = graph_builder.compile()
    #
    #         # 3.9 調用圖結構程式並獲取結果
    #         result = graph.invoke({"messages": [("human", query)]})
    #         print("最終結果： ",result)
    #         q.put(None)
    #
    #     def stream_event_response() -> Generator:
    #         """流式事件輸出響應"""
    #         # 1. 從隊列中獲取資料並使用yield拋出
    #         while True:
    #             item = q.get()
    #             if item is None:
    #                 break
    #             # 2. 使用yield關鍵字返回對應的資料
    #             yield f"event: {item.get('event')}\ndata: {json.dumps(item)}\n\n"
    #             q.task_done()
    #
    #     t = Thread(target=graph_app)
    #     t.start()
    #
    #     return compact_generate_response(stream_event_response())


    def debug(self, app_id: UUID):
        """聊天接口"""
        # 1. 提取從接口中獲取的輸入，POST
        req = CompletionReq()
        if not req.validate():
            return validate_error_json(req.errors)

        # 2. 創建prompt與記憶
        system_prompt = "你是一個強大的工研院客服機器人，能根據對應的上下文和歷史對話信息回覆用戶問題。在向量資料庫中找不到答案即輸出：「很抱歉，目前無法找到相關資料，將為您提供專人聯絡方式協助您。」 \n\n<context>{context}</context>"
        prompt = ChatPromptTemplate.from_messages([
            ("system",system_prompt),
            MessagesPlaceholder("history"),
            ("human","{query}"),
        ])
        memory = ConversationBufferWindowMemory(
            k=3,
            input_key="query",
            output_key="output",
            return_messages=True,
            chat_memory=FileChatMessageHistory("./storage/memory/chat_history.txt"),
        )

        # 3. 創建llm
        llm = ChatOpenAI(model="gpt-4o-mini")

        # 4. 創建鏈應用
        retriever = self.vector_database_service.get_retriever() | self.vector_database_service.combine_documents
        chain = (RunnablePassthrough.assign(
            history=RunnableLambda(self._load_memory_variables) | itemgetter("history"),
            context=itemgetter("query") | retriever
        ) | prompt | llm | StrOutputParser()).with_listeners(on_end=self._save_context)

        # 5. 調用鏈生成內容
        chain_input = {"query": req.query.data}
        content = chain.invoke(chain_input, config={"configurable":{"memory":memory}})
        # # 2. 構建組件
        # prompt = ChatPromptTemplate.from_template("{query}")
        # llm = ChatOpenAI(model="gpt-4o-mini")
        # parser = StrOutputParser()
        #
        # # 3. 構建鏈
        # chain = prompt | llm | parser
        #
        # # 4. 調用鏈得到結果
        # content = chain.invoke({"query": req.query.data})

        # # 2. 構建Openai客戶端，並發起請求
        # llm = ChatOpenAI(model="gpt-4o-mini")
        # # client = OpenAI()
        #
        # # 3. 得到請求響應，然後將Openai的響應傳遞給前端
        # ai_message = llm.invoke(prompt.invoke({"query":req.query.data}))
        #
        # parser = StrOutputParser()

        # # 4. 解析響應內容
        # content = parser.invoke(ai_message)
        # completion = client.chat.completions.create(
        #     model="gpt-4o-mini",
        #     messages=[
        #         {"role":"system","content":"你是openai開發的聊天機器人，請根據用戶的輸入回覆對應的信息"},
        #         {"role":"user","content": req.query.data}
        #     ]
        # )

        # content = completion.choices[0].message.content

        return success_json({"content":content})



    def ping(self):
        demo_task.delay(uuid.uuid4())
        return self.api_tool_service.api_tool_invoke()
        # return success_json()
        # raise FailException("資料未找到")
        # return {"ping": "pong"}
