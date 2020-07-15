# -*- coding: utf-8 -*-
# @Time    : 2020/7/10 10:53 下午
# @Author  : yan.zhao
# @FileName: view.py
# @Software: PyCharm
# @Email ：yan.zhao@bowmicro.com
from flask import Blueprint, url_for

user_bp = Blueprint('user', __name__)


@user_bp.route('/')
def user_center():
    print(url_for('user.register'))
    return '用户中心'


@user_bp.route('/register')
def register():
    return '用户注册'
