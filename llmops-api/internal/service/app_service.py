"""
@Time: 2026/3/8
@Author: chyu.wissfi@gmail.com
@Description: ...
"""

from dataclasses import dataclass
from injector import inject
from flask_sqlalchemy import SQLAlchemy
import uuid
from internal.model.app import App

@inject
@dataclass
class AppService:
    """
    AI 应用服务逻辑
    """
    db: SQLAlchemy

    def create_app(self) -> App:
        """
        创建 AI 应用
        """
        # 创建 AI 应用实例
        app = App(
            account_id=uuid.uuid4(),
            name="测试机器人",
            icon="",
            description="这是一个简单的聊天机器人",
        )
        # 数据库会话添加应用实例
        self.db.session.add(app)
        # 数据库会话提交变更
        self.db.session.commit()
        # 返回创建的应用实例
        return app