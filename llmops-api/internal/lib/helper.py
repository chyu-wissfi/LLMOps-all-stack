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
