# -*- coding: utf-8 -*-
# @Time    : 2020/7/15 12:04 下午
# @Author  : yan.zhao
# @FileName: models.py
# @Software: PyCharm
# @Email ：yan.zhao@bowmicro.com
from datetime import datetime

from exts import db


class Article_type(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type_name = db.Column(db.String(20), nullable=False)
    articles = db.relationship('Article', backref='articletype')


class Article(db.Model):
    # 主键
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 标题
    title = db.Column(db.String(50), nullable=False)
    # 内容
    content = db.Column(db.Text, nullable=False)
    # 发布时间
    pdatetime = db.Column(db.DateTime, default=datetime.now)
    # 点击量阅读量
    click_num = db.Column(db.Integer, default=0)
    # 收藏数
    save_num = db.Column(db.Integer, default=0)
    # 点赞
    love_num = db.Column(db.Integer, default=0)
    # 外键 同步到数据库的外键关系
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey('article_type.id'), nullable=False)
    comments = db.relationship('Comment', backref='article')


class Comment(db.Model):
    # 自定义表名
    # __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    comment = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'))
    cdatetime = db.Column(db.DateTime, default=datetime.now)

    def __str__(self):
        return self.comment
