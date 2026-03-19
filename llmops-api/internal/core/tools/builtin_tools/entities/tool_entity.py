"""
Time: 2026/3/18
@Author: chyu.wissfi@gmail.com
@Description: Tool entity
"""
from enum import Enum
from pydantic import BaseModel, Field
from typing import Any, Optional


class ToolParamType(str, Enum):
    """
    工具参数类型枚举类
    """
    STRING = "string"
    NUMBER = "number"
    BOOLEAN = "boolean"
    SELECT = "select"


class ToolParam(BaseModel):
    """
    工具参数类型
    """
    name: str  # 参数的实际名称
    label: str  # 参数的显示名称，前端显示名称
    type: ToolParamType = Field(description="参数类型")  # 参数类型
    # description: str  # 参数描述
    required: bool = False  # 是否必填
    default: Optional[Any] = None  # 默认值
    min: Optional[float] = None  # 最小值
    max: Optional[float] = None  # 最大值
    options: list[dict[str, Any]] = Field(default_factory=list)  # 下拉选项列表


class ToolEntity(BaseModel):
    """
    工具实体类,映射的数据是<工具名>.yaml里的每条记录
    """
    name: str  # 工具名字
    label: str  # 工具标签，前端显示名称
    description: str  # 工具描述
    params: list[ToolParam] = Field(default_factory=list)  # 工具的参数信息
   