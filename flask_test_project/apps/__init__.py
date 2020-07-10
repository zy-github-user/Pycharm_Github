# -*- coding: utf-8 -*-
# @Time    : 2020/7/10 2:01 下午
# @Author  : yan.zhao
# @FileName: __init__.py.py
# @Software: PyCharm
# @Email ：yan.zhao@bowmicro.com
from flask import Flask
import settings
from apps.user.view import user_bp


# 工厂函数
def create_app():
    app = Flask(__name__)  # app是一个核心对象
    app.config.from_object(settings)  # 加载配置
    # 蓝图
    app.register_blueprint(user_bp)  # 将蓝图对象绑定到app上
    return app
