# -*- coding: utf-8 -*-
# @Time    : 2020/7/10 1:56 下午
# @Author  : yan.zhao
# @FileName: app2.py
# @Software: PyCharm
# @Email ：yan.zhao@bowmicro.com
from flask import Flask
from apps import create_app

app = create_app()

if __name__ == '__main__':
    app.run()