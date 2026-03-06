"""
@Time: 2026/3/6
@Author: chyu.wissfi@gmail.com
@Description: Test app handler
"""
from pkg.response import HttpCode
import pytest

class TestAppHandler:
    """
    app控制器的测试类
    """
    @pytest.mark.parametrize("query", [None, "你好，你是?"])
    def test_completion(self, client, query):
        """
        测试聊天接口
        """
        resp = client.post("/app/completion", json={"query": query})
        assert resp.status_code == 200
        if query is None:
            assert resp.json.get("code") == HttpCode.VALIDATE_ERROR
        else:
            assert resp.json.get("code") == HttpCode.SUCCESS
