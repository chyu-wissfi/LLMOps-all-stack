"""
@Time: 2026/3/4
@Author: chyu.wissfi@gmail.com
@Description: Application handler
"""
from openai import OpenAI
import os
from internal.schema.app_schema import CompletionReq
from pkg.response import success_json, validate_error_json
from internal.exception import FailException


class AppHandler:
    """
    Application handler
    """
    def completion(self) -> dict:
        """
        聊天接口
        基础聊天接口，接收用户输入，调用OpenAI API，返回模型响应
        """
        # 1.提取从接口中获取的输入，POST
        req = CompletionReq()
        if not req.validate():
            return validate_error_json(req.errors)

        # 2.构建OpenAI 客户端并发起请求
        client = OpenAI(
            api_key=os.getenv("API_KEY"),
            base_url=os.getenv("BASE_URL")
        )
        
        # 3.得到请求响应，然后将OpenAI的响应传递给前端
        completion = client.chat.completions.create(
            model="gpt-5",
            messages=[
                {"role": "system", "content": "你是一个专业的助手,请回答用户的问题"},
                {"role": "user", "content": req.query.data},
            ],
        )

        content = completion.choices[0].message.content

        return success_json({"content": content})   # 这个接口返回的状态码永远是200

    def ping(self):
        raise FailException("数据未找到")


if __name__ == "__main__":
    print(os.getenv("API_KEY"))
    print(os.getenv("BASE_URL"))