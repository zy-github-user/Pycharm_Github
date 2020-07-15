# -*- coding: utf-8 -*-
# @Time    : 2020/7/14 9:35 上午
# @Author  : yan.zhao
# @FileName: __init__.py.py
# @Software: PyCharm
# @Email ：yan.zhao@bowmicro.com
from flask import Flask
from apps.user.view import user_bp
import settings
from exts import db


# 工厂函数
def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    # 加载settings配置
    app.config.from_object(settings.DevelopmentConfig)
    # 初始化db
    db.init_app(app=app)
    # 注册蓝图
    app.register_blueprint(user_bp)
    # 查看路由表
    print(app.url_map)
    return app
