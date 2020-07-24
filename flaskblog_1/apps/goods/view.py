# -*- coding: utf-8 -*-
# @Time    : 2020/7/16 9:33 上午
# @Author  : yan.zhao
# @FileName: view.py
# @Software: PyCharm
# @Email ：yan.zhao@bowmicro.com
from flask import Blueprint, render_template, request

from apps.goods.models import Goods, User_goods
from apps.user.models import User
from exts import db

goods_bp = Blueprint('goods', __name__)


# 查询用户已经购买过的商品（找商品）
@goods_bp.route('/findgoods')
def find_goods():
    user_id = request.args.get('uid')
    user = User.query.get(user_id)
    return render_template('goods/findgoods.html', user=user)


# 查询该商品有哪些用户购买 （找用户）
@goods_bp.route('/finduser')
def find_user():
    goods_id = request.args.get('gid')
    goods = Goods.query.get(goods_id)
    return render_template('goods/finduser.html', goods=goods)


# 展现商品，等待用户购买商品的操作
@goods_bp.route('/show')
def show():
    users = User.query.filter(User.isdelete == False).all()
    goods_list = Goods.query.all()
    return render_template('goods/show.html', users=users, goods_list=goods_list)


# 购买操作获取用户和商品信息
@goods_bp.route('/buy')
def buy():
    uid = request.args.get('uid')
    gid = request.args.get('gid')
    ug = User_goods()
    ug.user_id = uid
    ug.goods_id = gid
    db.session.add(ug)
    db.session.commit()
    return '购买成功'
