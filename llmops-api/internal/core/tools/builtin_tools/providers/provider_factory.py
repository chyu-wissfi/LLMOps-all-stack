"""
Time: 2026/3/18
@Author: chyu.wissfi@gmail.com
@Description: Provider factory
"""
import os
import yaml
from injector import inject, singleton
from typing import Any
from internal.core.tools.builtin_tools.entities import ProviderEntity, Provider



@inject
@singleton
class ProviderFactory:
    """
    服务提供商工厂类
    """
    provider_map: dict[str, Provider] = {}

    def __init__(self):
        """
        初始化对应的provider_tool_map
        """
        self._get_provider_map()

    def get_provider(self, provider_name: str) -> Provider:
        """
        根据服务提供商名字获取服务提供商
        """
        return self.provider_map.get(provider_name, None)

    def get_providers(self) -> list[Provider]:
        """
        获取所有服务提供商
        """
        return list(self.provider_map.values())

    def get_provider_entities(self) -> list[ProviderEntity]:
        """
        获取所有服务提供商实体实体
        """
        return [provider.provider_entity for provider in self.provider_map.values()]

    def get_tool(self, provider_name: str, tool_name: str) -> Any:
        """
        根据服务提供商名字和工具名字获取工具实体
        """
        provider = self.get_provider(provider_name)
        if provider:
            return provider.get_tool(tool_name)
        return None

    def _get_provider_map(self):
        """
        项目初始化的时候获取服务提供商的映射关系并填充provider_map
        """
        if self.provider_map:
            return

        current_path = os.path.dirname(os.path.abspath(__file__))
        providers_yaml_path = os.path.join(current_path, "providers.yaml")

        # 读取providers.yaml文件
        with open(providers_yaml_path, encoding="utf-8") as f:
            providers_yaml_data = yaml.safe_load(f)

            for idx, provider_data in enumerate(providers_yaml_data):
                provider_entity = ProviderEntity(**provider_data)
                self.provider_map[provider_entity.name] = Provider(
                    name=provider_entity.name,
                    position=idx + 1,
                    provider_entity=provider_entity,
                )
               
