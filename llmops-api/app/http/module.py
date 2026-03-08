"""
@Time: 2026/3/5
@Author: chyu.wissfi@gmail.com
@Description: 扩展模块的依赖注入
"""
from injector import Module, Binder
from pkg.sqlalchemy import SQLAlchemy
from internal.extension.database_extension import db
from flask_migrate import Migrate
from internal.extension.migrate_extension import migrate



class ExtensionModule(Module):
    """
    扩展模块的依赖注入
    """
    def configure(self, binder: Binder) -> None:
        binder.bind(SQLAlchemy, to=db)
        
        # 绑定数据库迁移扩展
        binder.bind(Migrate, to=migrate)
