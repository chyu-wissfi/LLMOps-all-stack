"""
@Time: 2026/3/4
@Author: chyu.wissfi@gmail.com
@Description: Application handler
"""
from operator import itemgetter
import os
from internal.schema.app_schema import CompletionReq
from pkg.response import success_json, validate_error_json, success_message
from internal.exception import FailException
from internal.service import AppService, VectorDatabaseService
from dataclasses import dataclass
from injector import inject
from uuid import UUID
from typing import Any, Dict


from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda, RunnableConfig
from langchain_core.memory import BaseMemory
from langchain_core.tracers import Run
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferWindowMemory
from langchain_community.chat_message_histories import FileChatMessageHistory
from internal.core.tools.builtin_tools.providers import ProviderFactory



@inject
@dataclass
class AppHandler:
    """
    Application handler
    """
    app_service: AppService
    vector_database_service: VectorDatabaseService
    provider_factory: ProviderFactory

    def create_app(self) -> dict:
        """
        调用服务创建新的APP记录
        """
        app = self.app_service.create_app()
 
        return success_message(f"创建应用成功, 应用ID: {app.id}")

    def get_app(self, id: UUID) -> dict:
        """
        获取应用详情
        """
        app = self.app_service.get_app(id)
        return success_message(f"获取应用成功, 应用名称: {app.name}")

    def update_app(self, id: UUID) -> dict:
        """
        更新应用详情
        """
        app = self.app_service.update_app(id)
        return success_message(f"更新应用成功, 应用名称修改为: {app.name}")

    def delete_app(self, id: UUID) -> dict:
        """
        删除应用详情
        """
        app = self.app_service.delete_app(id)
        return success_message(f"删除应用成功, 应用ID: {app.id}")

    @classmethod
    def _load_memory_variables(cls, input: Dict[str, Any], config: RunnableConfig) -> Dict[str, Any]:
        """
        加载记忆变量信息
        """
        configurable = config.get("configurable", {})
        configurable_memory = configurable.get("memory", None)
        if configurable_memory is not None and isinstance(configurable_memory, BaseMemory):
            return configurable_memory.load_memory_variables(input)
        return {"history": []}

    @classmethod
    def _save_context(cls, run_obj: Run, config: RunnableConfig) -> None:
        """
        存储上下文信息到对应的记忆实体中
        """
        configurable = config.get("configurable", {})
        configurable_memory = configurable.get("memory", None)
        if configurable_memory is not None and isinstance(configurable_memory, BaseMemory):
            configurable_memory.save_context(run_obj.inputs, run_obj.outputs)

    def debug(self, app_id: UUID) -> dict:
        """
        聊天接口
        基础聊天接口，接收用户输入，调用OpenAI API，返回模型响应
        """
        # 1.提取从接口中获取的输入，POST
        req = CompletionReq()
        if not req.validate():
            return validate_error_json(req.errors)

        # 2. 构建Prompt模板与记忆
        system_prompt = "你是一个强大的聊天机器人,能根据对应的上下文和历史对话信息回复用户的问题。\n\n <context>{context}</context>"
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{query}"),
        ])

        memory = ConversationBufferWindowMemory(
            k=3,
            input_key="query",
            output_key="output",
            return_messages=True,
            chat_memory=FileChatMessageHistory(file_path="./storage/memory/chat_history.txt"),
        )

        # 3.构建OpenAI 客户端并发起请求
        llm = ChatOpenAI(
            api_key=os.getenv("API_KEY"),
            base_url=os.getenv("BASE_URL"),
            model_name="gpt-5",
        )
        # 4. 解析OpenAI的响应
        parser = StrOutputParser()
        
        retriever = self.vector_database_service.get_retriever() | self.vector_database_service.combine_documents

        # 5.创建链应用
        chain = (RunnablePassthrough.assign(
                history = RunnableLambda(self._load_memory_variables) | itemgetter("history"),
                context = itemgetter("query") | retriever,
            ) 
            | prompt 
            | llm 
            | parser
        ).with_listeners(on_end=self._save_context)

        chain_input = {"query": req.query.data}
        
        content = chain.invoke(chain_input, config = {"configurable":{"memory":memory}})

        return success_json({"content": content})

    def ping(self):
        """
        测试接口
        """
        google_serper = self.provider_factory.get_tool("google", "google_serper")()
        print(google_serper)
        print(google_serper.invoke("2024年北京半程马拉松的前3名成绩是多少"))
        return success_json()

        # raise FailException("数据未找到")


# if __name__ == "__main__":
#     print(os.getenv("API_KEY"))
#     print(os.getenv("BASE_URL"))