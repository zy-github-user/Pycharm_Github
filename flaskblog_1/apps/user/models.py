# -*- coding: utf-8 -*-
# @Time    : 2020/7/14 10:43 上午
# @Author  : yan.zhao
# @FileName: models.py
# @Software: PyCharm
# @Email ：yan.zhao@bowmicro.com
from datetime import datetime

from exts import db


# 必须继承Model才是模型类，类名就是表名，属性就是字段
class User(db.Model):
    # 主键
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    # 用户名
    username = db.Column(db.String(15), nullable=False)
    # 密码需要加密
    password = db.Column(db.String(64), nullable=False)
    # 电话
    phone = db.Column(db.String(11), unique=True, nullable=False)
    # 邮箱
    email = db.Column(db.String(30))
    # 用户头像
    icon = db.Column(db.String(100))
    # 判断逻辑删除标识
    isdelete = db.Column(db.Boolean, default=False)
    # 注册时间
    rdatetime = db.Column(db.DateTime, default=datetime.now)
    # 一对多，实现快速表链接查询
    articles = db.relationship('Article', backref='user')

    def __str__(self):
        return self.username
