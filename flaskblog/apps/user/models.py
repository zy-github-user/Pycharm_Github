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
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    username = db.Column(db.String(15), nullable=False)
    # 密码需要加密
    password = db.Column(db.String(64), nullable=False)
    phone = db.Column(db.String(11), unique=True)
    # 逻辑删除
    isdelete = db.Column(db.Boolean, default=False)
    rdatetime = db.Column(db.DateTime, default=datetime.now)

    def __str__(self):
        return self.username