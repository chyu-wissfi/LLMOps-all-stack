"""
@Time: 2026/3/4
@Author: chyu.wissfi@gmail.com
@Description: router.py
"""
from dataclasses import dataclass
from flask import Flask, Blueprint
from internal.handler import AppHandler
from injector import Injector, inject

@inject
@dataclass
class Router:
    """
    Router class
    """
    app_handler: AppHandler

    def register_router(self, app: Flask):
        """
        Register router
        """
        # 1.创建一个蓝图
        bp = Blueprint("llmops", __name__,url_prefix="") 
        
        # 2.将url与对应的控制器做绑定
        # bp.add_url_rule("/ping", view_func=self.app_handler.ping)
        bp.add_url_rule("/app/<uuid:app_id>/debug", methods=["POST"], view_func=self.app_handler.debug)
        # bp.add_url_rule("/app", methods=["POST"], view_func=self.app_handler.create_app)
        # bp.add_url_rule("/app/<uuid:id>", view_func=self.app_handler.get_app)  # 默认GET方法
        # bp.add_url_rule("/app/<uuid:id>/update", methods=["POST"], view_func=self.app_handler.update_app)
        # bp.add_url_rule("/app/<uuid:id>/delete", methods=["POST"], view_func=self.app_handler.delete_app)
        
        # 3.将蓝图注册到app中
        app.register_blueprint(bp)

