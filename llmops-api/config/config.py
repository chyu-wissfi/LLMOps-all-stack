"""
@Time: 2026/3/4
@Author: chyu.wissfi@gmail.com
@Description: Config file
"""

class Config:
    """
    Config class
    """
    def __init__(self):
        # 关闭 WTF 的 CSRF保护
        self.WTF_CSRF_ENABLED = False
