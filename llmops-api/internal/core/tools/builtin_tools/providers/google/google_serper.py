"""
@Time: 2026/3/18
@Author: chyu.wissfi@gmail.com
@Description: Google Serper service provider
"""
from langchain_core.tools import BaseTool
from langchain_community.tools import GoogleSerperRun
from pydantic import BaseModel, Field
from langchain_community.utilities import GoogleSerperAPIWrapper


class GoogleSerperArgsSchema(BaseModel):
    """
    Google Serper 搜索工具参数描述
    """
    query: str = Field(description="需要检索查询的语句.")


def google_serper(**kwargs) -> BaseTool:
    """
    Google Serper 搜索工具
    :param query:
    :return:
    """
    return GoogleSerperRun(
        name="google_serper",
        description="这是一个低成本的谷歌搜索API。当你需要搜索时事的时候，可以使用该工具，该工具的输入是一个查询语句。",
        args_schema=GoogleSerperArgsSchema,
        api_wrapper=GoogleSerperAPIWrapper(),
    )