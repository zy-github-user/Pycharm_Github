# -*- coding: utf-8 -*-
# @Time    : 2020/7/9 9:30 上午
# @Author  : yan.zhao
# @FileName: app1.py
# @Software: PyCharm
# @Email ：yan.zhao@bowmicro.com

from flask import Flask, request, render_template

import settings

app = Flask(__name__)
app.config.from_object(settings)


class Girl:
    def __init__(self, name, addr):
        self.name = name
        self.gender = '女'
        self.addr = addr

    def __str__(self):
        return self.name


@app.route('/show')
def show():
    name = '秦始皇'
    friends = ['张三', '李四', '王老五']
    dict1 = {'1': 'zhangsan', '2': 'lisi', '3': 'wangwu'}
    users = [
        {'username': 'zhangsan1', 'password': '123123', 'addr': '北京'},
        {'username': 'zhangsan2', 'password': '123123', 'addr': '北京'},
        {'username': 'zhangsan3', 'password': '123123', 'addr': '北京'},
        {'username': 'zhangsan4', 'password': '123123', 'addr': '北京'},
    ]
    # 创建对象
    girlfriend = Girl('如花', '美国')
    return render_template('show.html', name=name, age='20', friends=friends, dict1=dict1, girl=girlfriend, users=users)


@app.route('/filter')
def filter():
    msg = '<h1>哈哈哈</h1>'
    n1 = 'hello'
    return render_template('filter.html', msg=msg, n1=n1)


# 过滤器的本质就是函数

if __name__ == '__main__':
    app.run()
