# -*- coding: utf-8 -*-
# @Time    : 2020/7/14 10:43 上午
# @Author  : yan.zhao
# @FileName: view.py
# @Software: PyCharm
# @Email ：yan.zhao@bowmicro.com
import hashlib

from flask import Blueprint, url_for, render_template, request, redirect
from sqlalchemy import or_

from apps.user.models import User
from exts import db

user_bp = Blueprint('user', __name__)


# 用户中心
@user_bp.route('/')
def user_center():
    # 查询数据库中的数据,User有query方法是因为User类继承了Model类
    users = User.query.filter(User.isdelete == False).all()  # select * from user;
    print(users)  # 列表 [User_objectA, User_objectB],是具有User类属性的对象
    return render_template('user/center.html', users=users)


# 注册
@user_bp.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        repassword = request.form.get('repassword')
        phone = request.form.get('phone')
        if password == repassword:
            # 注册用户
            user = User()
            user.username = username
            # 密码加密
            user.password = hashlib.sha256(password.encode('utf-8')).hexdigest()
            user.phone = phone
            # 添加并提交
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('user.user_center'))

    return render_template('user/register.html')


# 登录，按钮点击后，把username+password去跟数据库中的数据进行匹配
@user_bp.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # 查询匹配 select * from user where username='zhaoyan'
        new_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        # 查询 第一个username是字段名，后一个是从表单上获取的
        user_list = User.query.filter_by(username=username)
        print(user_list)  # 返回的是一个SQL语句，是python中的列表结构
        # 会返回所有的用户对象，包括重复的
        for u in user_list:
            print(u)
            if u.password == new_password:
                return '用户登录成功'
        else:
            return render_template('user/login.html', msg='用户名或密码有误')
    return render_template('user/login.html')


# 搜索按钮
@user_bp.route('/search')
def search():
    keyword = request.args.get('search')
    # 查询
    user_list = User.query.filter(or_(User.username.contains(keyword), User.phone.contains(keyword))).all()
    return render_template('user/center.html', users=user_list)


# 用户信息更新
@user_bp.route('/update', endpoint='update', methods=['POST', 'GET'])
def user_update():
    if request.method == 'POST':
        username = request.form.get('username')
        phone = request.form.get('phone')
        id = request.form.get('id')
        # 找用户
        user = User.query.get(id)
        # 改用户信息
        user.phone = phone
        user.username = username
        # 提交
        db.session.commit()
        return redirect(url_for('user.user_center'))
    else:
        id = request.args.get('id')
        user = User.query.get(id)
        return render_template('user/update.html', user=user)


# 用户删除
@user_bp.route('/delete')
def user_delete():
    # 获取用户id
    id = request.args.get('id')
    # 获取该id的用户
    user = User.query.get(id)
    # 逻辑删除
    user.isdelete = True
    # 提交
    db.session.commit()
    """
    物理删除
    # 获取用户id
    id = request.args.get('id')
    # 获取该id的用户
    user = User.query.get(id)
    # 将对象放到缓存准备删除，类似于放到回收站中
    db.session.delete(user)
    # 提交删除，应该加上是否确认删除的弹框
    db.session.commit()
    """
    return redirect(url_for('user.user_center'))
