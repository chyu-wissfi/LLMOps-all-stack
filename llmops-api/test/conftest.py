"""
@Time: 2026/3/5
@Author: chyu.wissfi@gmail.com
@Description: Test config
"""
# import sys
# from pathlib import Path
# # 添加项目根目录到 Python 路径
# sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from app.http.app import app


@pytest.fixture()
def client():
    """
    获取Flask应用的测试应用并返回
    """
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client