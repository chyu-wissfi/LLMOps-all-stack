"""
@Time: 2026/3/8
@Author: chyu.wissfi@gmail.com
@Description: AI 应用基础模型类
"""
from datetime import datetime
import uuid
from internal.extension.database_extension import db
from sqlalchemy import (
    Column,
    UUID,
    String,
    Text,
    DateTime,
    PrimaryKeyConstraint,
    Index,
)


class App(db.Model):
    """
    AI 应用基础模型类
    APP ORM
    """
    __tablename__ = 'app'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='pk_app_id'),
        Index('idx_app_account_id', 'account_id'),
    )

    id = Column(UUID, default=uuid.uuid4, nullable=False)       # 应用ID
    account_id = Column(UUID, nullable=False)                   # 应用所属账号ID
    name = Column(String(255), default='', nullable=False)
    icon = Column(String(255), default='', nullable=False)
    description = Column(Text, default='', nullable=False)
    status = Column(String(255), default='', nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)