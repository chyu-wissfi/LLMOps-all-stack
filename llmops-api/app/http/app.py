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
from .module import ExtensionModule
from pkg.sqlalchemy import SQLAlchemy
from flask_migrate import Migrate



# 导入环境变量
load_dotenv()

conf = Config()


# 初始化依赖注入容器
injector = Injector([ExtensionModule])

app = Http(
    __name__,
    conf=conf,
    db=injector.get(SQLAlchemy),
    router=injector.get(Router),
    migrate=injector.get(Migrate),
)


if __name__ == "__main__":
    app.run(debug=True)
    # app.run(debug=False)
