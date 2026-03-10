"""
@Time: 2026/3/5
@Author: chyu.wissfi@gmail.com
@Description: 回调功能使用技巧
"""
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain_core.callbacks import StdOutCallbackHandler, BaseCallbackHandler
from typing import Any, Dict, List
from uuid import UUID
from langchain_core.messages import BaseMessage
import dotenv
dotenv.load_dotenv()

# 自定义回调函数
class LLMOpsCallbackHandler(BaseCallbackHandler):
    """自定义LLMOps回调处理器"""
    def on_chat_model_start(
        self,
        serialized: Dict[str, Any],
        messages: List[List[BaseMessage]],
        *,
        run_id: UUID,
        parent_run_id: UUID | None = None,
        tags: List[str] | None = None,
        metadata: Dict[str, Any] | None = None,
        **kwargs: Any
    ) -> Any:
        """处理聊天模型开始运行时的回调"""
        print("开始运行聊天模型")
        print("模型序列化配置:", serialized)
        print("输入消息:", messages)
        


prompt = ChatPromptTemplate.from_template("{query}")
llm = ChatOpenAI(
    api_key=os.getenv("API_KEY"),
    base_url=os.getenv("BASE_URL"),
    model_name="gpt-5",
)
parser = StrOutputParser()

chain = {"query": RunnablePassthrough()} | prompt | llm | parser

content = chain.stream(
    "你好，你是谁？",
    config={"callbacks": [StdOutCallbackHandler(), LLMOpsCallbackHandler()]}
)
for chunk in content:
    print(chunk)
