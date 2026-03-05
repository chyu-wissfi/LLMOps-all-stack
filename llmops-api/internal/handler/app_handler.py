"""
@Time: 2026/3/4
@Author: chyu.wissfi@gmail.com
@Description: Application handler
"""

from flask import request
from openai import OpenAI
import os


class AppHandler:
    """
    Application handler
    """
    def completion(self) -> dict:
        """
        聊天接口
        """
        # 1.提取从接口中获取的输入，POST
        query = request.json.get("query")

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
                {"role": "user", "content": query},
            ],
        )

        content = completion.choices[0].message.content
        return content

    def ping(self):
        return {"ping": "pong"}


if __name__ == "__main__":
    print(os.getenv("API_KEY"))
    print(os.getenv("BASE_URL"))