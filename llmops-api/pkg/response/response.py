"""
@Time: 2026/3/4
@Author: chyu.wissfi@gmail.com
@Description: Response class
"""
from dataclasses import field
from typing import Any
from .http_code import HttpCode
from dataclasses import dataclass
from flask import jsonify

@dataclass
class Response:
    """
    基础HTTP接口响应格式
    """
    code: HttpCode = HttpCode.SUCCESS
    message: str = ""
    data: Any = field(default_factory=dict)

def json(resp: Response) -> dict:
    """
    将Response对象转换为JSON格式
    """
    return jsonify(resp), 200

def success_json(data: Any = None) -> dict:
    """
    成功响应JSON格式
    """
    return json(Response(code=HttpCode.SUCCESS, message="", data=data))

def fail_json(data: Any = None) -> dict:
    """
    失败响应JSON格式
    """
    return json(Response(code=HttpCode.FAIL, message="", data=data))

def validate_error_json(errors: dict) -> dict:
    """
    验证错误响应JSON格式
    """
    first_key = next(iter(errors))
    msg = errors[first_key][0] if first_key is not None else ""
    return json(Response(code=HttpCode.VALIDATE_ERROR, message=msg, data=errors))

def message(code: HttpCode = None, msg: str = "") -> dict:
    """
    基础的消息响应JSON格式
    固定返回消息提示，数据固定为空字典
    """
    return json(Response(code=code, message=msg, data={}))

def success_message(msg: str = "") -> dict:
    """
    成功的消息响应
    """
    return message(code=HttpCode.SUCCESS, msg=msg)

def fail_message(msg: str = "") -> dict:
    """
    失败的消息响应
    """
    return message(code=HttpCode.FAIL, msg=msg)

def not_found_message(msg: str = "") -> dict:
    """
    未找到的消息响应
    """
    return message(code=HttpCode.NOT_FOUND, msg=msg)

def unauthorized_message(msg: str = "") -> dict:
    """
    未授权的消息响应
    """
    return message(code=HttpCode.UNAUTHORIZED, msg=msg)

def forbidden_message(msg: str = "") -> dict:
    """
    无权限，禁止访问的消息响应
    """
    return message(code=HttpCode.FORBIDDEN, msg=msg)