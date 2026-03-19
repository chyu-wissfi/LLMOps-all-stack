"""
Time: 2026/3/18
@Author: chyu.wissfi@gmail.com
@Description: Provider entity
"""

from pydantic import BaseModel, ConfigDict, Field
from typing import Any
from .tool_entity import ToolEntity
import os
import yaml
from internal.lib.helper import dynamic_import



class ProviderEntity(BaseModel):
    """
    服务提供商实体类,映射的数据是providers.yaml里的每条记录
    """
    name: str  # 名字
    label: str  # 标签，前端显示名称
    description: str  # 描述
    icon: str  # 图标地址
    background: str  # 图标背景颜色
    category: str  # 分类信息


class Provider(BaseModel):
    """
    服务提供商类，在该类下，可以获得该服务提供商的所有工具、描述、图标等多个信息
    """
    name: str  # 服务提供商名字
    position: int  # 服务提供商的顺序
    provider_entity: ProviderEntity  # 服务提供商实体类
    tool_entity_map: dict[str, ToolEntity] = Field(default_factory=dict)  # 工具实体类映射表
    tool_func_map: dict[str, Any] = Field(default_factory=dict)  # 工具函数映射表

    def __init__(self, **kwargs):
        """
        构造函数，初始化对应的服务提供商
        """
        super().__init__(**kwargs)
        self._provider_init()

    model_config = ConfigDict(protected_namespace=())

    def get_tool(self, tool_name: str) -> Any:
        """
        根据工具名字获取对应的服务提供商的工具函数
        """
        return self.tool_func_map.get(tool_name)

    def get_tool_entity(self, tool_name: str) -> ToolEntity:
        """
        根据工具名字获取对应的服务提供商的工具实体
        """
        return self.tool_entity_map.get(tool_name)

    def get_tool_entities(self) -> list[ToolEntity]:
        """
        获取对应的服务提供商的所有工具实体/信息列表
        """
        return list(self.tool_entity_map.values())

    def _provider_init(self):
        """
        服务提供商初始化函数
        """
        # 1.获取当前类的路径，计算对应的服务提供商地址/路径
        current_path = os.path.dirname(os.path.abspath(__file__))
        entity_path = os.path.dirname(current_path)
        provider_path = os.path.join(entity_path, "providers", self.name)

        # 2. 读取positions.yaml文件
        positions_yaml_path = os.path.join(provider_path, "positions.yaml")
        with open(positions_yaml_path, encoding="utf-8") as f:
            positions_yaml_data = yaml.safe_load(f)

        # 3. 循环读取位置信息获取服务提供商的工具名字
        for tool_name in positions_yaml_data:
            # 4. 获取工具的yaml文件
            tool_yaml_path = os.path.join(provider_path, f"{tool_name}.yaml")
            with open(tool_yaml_path, encoding="utf-8") as f:
                tool_yaml_data = yaml.safe_load(f)

            # 5. 将工具实体赋值填充到tool_entity_map中
            self.tool_entity_map[tool_name] = ToolEntity(**tool_yaml_data)
            
            # 6. 动态导入对应的工具并填充到tool_func_map中
            self.tool_func_map[tool_name] = dynamic_import(
                f"internal.core.tools.builtin_tools.providers.{self.name}",
                tool_name,
            )
                      
