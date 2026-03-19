"""
@Time: 2026/3/18
@Author: chyu.wissfi@gmail.com
@Description: Helper function
"""
import importlib
from typing import Any



def dynamic_import(module_name: str, symbol_name: str) -> Any:
    """
    动态导入模块中的符号
    """

    module = importlib.import_module(module_name)
    return getattr(module, symbol_name)


def add_attribute(name: str, value: Any):
    """
    装饰器函数，为特定的函数添加相应的属性，第一个参数为属性名字，第二个参数为属性值
    """

    def decorator(func):
        setattr(func, name, value)
        return func

    return decorator
