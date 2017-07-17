import os

from flask import Flask
from mongoengine import connect

from app import settings, ext
from app.modules import register_route


def create_app(test=False):
    """
    创建Flask app
    :param test: 如果True,连接专用的测试数据库，否则使用生产环境数据库，嗯，这个地方，pass
    :return: 
    """
    app = Flask(__name__)

    read_config(app)
    if test:
        app.config.update({"MODE": "DEV"})
        # todo: 如果test,则连接开发数据库
    # 连接数据库
    host = app.config.get("MONGODB_SETTINGS")
    connect(host=host, alias='default', tz_aware=True)
    # 注册组件
    ext.configure(app)
    # 注册路由
    register_route(app)
    return app


def read_config(app):
    # 读取配置文件
    app.config.from_object(settings)
    if 'GIT_SHARE_ENV' in os.environ:
        app.config.from_envvar('GIT_SHARE_ENV', silent=False)
