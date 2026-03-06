"""
@Time: 2026/3/5
@Author: chyu.wissfi@gmail.com
@Description: HTTP server application
"""
from injector import Injector
from internal.server import Http
from internal.router import Router
from dotenv import load_dotenv
from config import Config

# 导入环境变量
load_dotenv()

conf = Config()

# 初始化依赖注入容器
injector = Injector()

app = Http(__name__, conf=conf, router=injector.get(Router))


if __name__ == "__main__":
    app.run(debug=True)
    # app.run(debug=False)
