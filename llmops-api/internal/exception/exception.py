"""
@Time: 2026/3/6
@Author: chyu.wissfi@gmail.com
@Description: App exception
"""
from typing import Any
from dataclasses import field
from pkg.response import HttpCode

class CustomException(Exception):
    """
    基础自定义异常类
    """
    code: HttpCode = HttpCode.FAIL
    message: str = ""
    data: Any = field(default_factory=dict)

    def __init__(self, message: str = "", data: Any = None):
        super().__init__()
        self.message = message
        self.data = data

class FailException(CustomException):
    """
    失败异常类
    """
    pass

class NotFoundException(CustomException):
    """
    资源不存在异常类
    """
    code: HttpCode = HttpCode.NOT_FOUND

class UnauthorizedException(CustomException):
    """
    未授权异常类
    """
    code: HttpCode = HttpCode.UNAUTHORIZED

class ForbiddenException(CustomException):
    """
    无权限异常类
    """
    code: HttpCode = HttpCode.FORBIDDEN

class ValidationException(CustomException):
    """
    数据验证异常类
    """
    code: HttpCode = HttpCode.VALIDATE_ERROR
