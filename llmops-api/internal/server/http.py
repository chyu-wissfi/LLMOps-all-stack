"""
@Time: 2026/3/5
@Author: chyu.wissfi@gmail.com
@Description: HTTP server module
"""
from flask import Flask
from internal.router import Router
from config import Config
from internal.exception import CustomException
from pkg.response import json, Response, HttpCode
import os
from flask_sqlalchemy import SQLAlchemy
from internal.model.app import App


class Http(Flask):
    """
    HTTP 服务引擎
    """
    def __init__(self, *args, conf: Config, db: SQLAlchemy, router: Router, **kwargs) -> None:
        super().__init__(*args, **kwargs) 
        # 1. 初始化应用配置
        self.config.from_object(conf)
        
        # 2.注册绑定异常处理
        self.register_error_handler(Exception, self._register_error_handler)

        # 3.初始化Flask扩展
        db.init_app(self)
        with self.app_context():
            _ = App()      #  这么写的作用是为了触发App模型的注册，否则可能会报错
            db.create_all()

        # 4. 注册应用路由
        router.register_router(self)

    def _register_error_handler(self, error: Exception):
        """
        注册异常处理函数
        """
        # 1. 异常信息是不是我们自定义的异常，如果是可以提取message和code等信息
        if isinstance(error, CustomException):
            return json(Response(
                code = error.code,
                message = error.message,
                data = error.data if error.data is not None else {}
            ))
        # 2. 如果不是我们自定义的异常，则有可能是程序或数据库抛出的异常，也可以提取信息，设置为FAIL状态码
        if self.debug or os.getenv("Flask_ENV") == "development": 
            raise error
        else:
            return json(Response(code=HttpCode.FAIL, message=str(error), data={}))
