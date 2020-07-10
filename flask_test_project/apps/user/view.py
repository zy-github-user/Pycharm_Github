# -*- coding: utf-8 -*-
# @Time    : 2020/7/10 2:21 下午
# @Author  : yan.zhao
# @FileName: view.py
# @Software: PyCharm
# @Email ：yan.zhao@bowmicro.com
from flask import Blueprint

user_bp = Blueprint('user', __name__)


@user_bp.route('/')
def user_center():
    return '用户中心'


@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    return '用户注册'


@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    return '用户登录'


@user_bp.route('/loginout', methods=['GET', 'POST'])
def loginout():
    return '用户退出'
