# -*- coding: utf-8 -*-
# @Time    : 2020/7/10 10:49 下午
# @Author  : yan.zhao
# @FileName: settings.py
# @Software: PyCharm
# @Email ：yan.zhao@bowmicro.com
"""
    该配置文件通常可复用，只需要改数据库的配置路径即可
"""


class Config:
    DEBUG = True
    # mysql + pymysql://user:password@host:port/databasename
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@127.0.0.1:3306/flaskblog'
    # 动态追踪修改设置，如未设置只会提示警告
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 查询时会显示原始SQL语句
    SQLALCHEMY_ECHO = True


class DevelopmentConfig(Config):
    ENV = 'development'


class ProductionConfig(Config):
    ENV = 'production'
    DEBUG = False
