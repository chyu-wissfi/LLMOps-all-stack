"""
@Time: 2026/3/5
@Author: chyu.wissfi@gmail.com
@Description: App schema
"""

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length

class CompletionReq(FlaskForm):
    """
    Completion request form
    基础聊天接口请求验证
    """
    # 必填、长度最大为2048
    query = StringField("query", validators=[
        DataRequired(message="query is required"), 
        Length(max=2048, message="query length must be less than 2048")
    ])