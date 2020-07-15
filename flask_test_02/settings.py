# -*- coding: utf-8 -*-
# @Time    : 2020/7/10 10:49 下午
# @Author  : yan.zhao
# @FileName: settings.py
# @Software: PyCharm
# @Email ：yan.zhao@bowmicro.com


class Config:
    DEBUG = True
    # mysql + pymysql://user:password@host:port/databasename
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@127.0.0.1:3306/flask_test'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True


class DevelopmentConfig(Config):
    ENV = 'development'


class ProductionConfig(Config):
    ENV = 'production'
    DEBUG = False
