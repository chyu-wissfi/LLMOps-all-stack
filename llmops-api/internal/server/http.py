"""
@Time: 2026/3/5
@Author: chyu.wissfi@gmail.com
@Description: HTTP server module
"""
from flask import Flask
from internal.router import Router
from config import Config



class Http(Flask):
    """
    HTTP 服务引擎
    """
    def __init__(self, *args, conf: Config, router: Router, **kwargs) -> None:
        super().__init__(*args, **kwargs) 
        # 注册应用路由
        router.register_router(self)
        self.config.from_object(conf)