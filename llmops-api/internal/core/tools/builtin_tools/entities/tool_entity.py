"""
Time: 2026/3/18
@Author: chyu.wissfi@gmail.com
@Description: Tool entity
"""

from pydantic import BaseModel
from typing import Any


class ToolEntity(BaseModel):
    """
    工具实体类,映射的数据是<工具名>.yaml里的每条记录
    """
    name: str  # 工具名字
    label: str  # 工具标签，前端显示名称
    description: str  # 工具描述
    params: list = []  # 工具的参数信息
   