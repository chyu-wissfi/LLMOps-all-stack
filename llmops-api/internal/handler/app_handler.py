"""
@Time: 2026/3/4
@Author: chyu.wissfi@gmail.com
@Description: Application handler
"""
import os
from internal.schema.app_schema import CompletionReq
from pkg.response import success_json, validate_error_json, success_message
from internal.exception import FailException
from internal.service import AppService
from dataclasses import dataclass
from injector import inject
from uuid import UUID
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

@inject
@dataclass
class AppHandler:
    """
    Application handler
    """
    app_service: AppService

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

    def debug(self, app_id: UUID) -> dict:
        """
        聊天接口
        基础聊天接口，接收用户输入，调用OpenAI API，返回模型响应
        """
        # 1.提取从接口中获取的输入，POST
        req = CompletionReq()
        if not req.validate():
            return validate_error_json(req.errors)

        # 2. 构建Prompt模板
        prompt = ChatPromptTemplate.from_messages([
            ("system", "你是一个专业的助手,请回答用户的问题"),
            ("human", "{query}"),
        ])

        # 3.构建OpenAI 客户端并发起请求
        llm = ChatOpenAI(
            api_key=os.getenv("API_KEY"),
            base_url=os.getenv("BASE_URL"),
            model_name="gpt-5",
        )
        # 4. 解析OpenAI的响应
        parser = StrOutputParser()

        # 5.得到请求响应，然后将OpenAI的响应传递给前端
        chain = prompt | llm | parser
        
        ai_message = chain.invoke(
            {"query": req.query.data}
        )

        return success_json({"content": ai_message})   # 这个接口返回的状态码永远是200

    def ping(self):
        raise FailException("数据未找到")


if __name__ == "__main__":
    print(os.getenv("API_KEY"))
    print(os.getenv("BASE_URL"))