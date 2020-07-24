# -*- coding: utf-8 -*-
# @Time    : 2020/7/15 8:26 下午
# @Author  : yan.zhao
# @FileName: models.py
# @Software: PyCharm
# @Email ：yan.zhao@bowmicro.com
from exts import db


# 模型类名首字母大写，数据库对应的表名是类名转换成小写之后的名字
class Goods(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    gname = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    # 多对多需要到第三方的表中去寻找外键关系（'User'--模型名，secondry='user_goods'--表名）
    # back reference 反向查找 relationship可以实现相互查找
    users = db.relationship('User', backref='goods', secondary='user_goods')

    def __str__(self):
        return self.gname


# 关系表： user和goods之间的关系
class User_goods(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 这里的user和goods都是数据库表名
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    goods_id = db.Column(db.Integer, db.ForeignKey('goods.id'))
    number = db.Column(db.Integer, default=1)
