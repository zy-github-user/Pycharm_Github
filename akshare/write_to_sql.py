# -*- coding: utf-8 -*-

# @Time    : 2020/3/12 1:49 下午
# @Author  : yan.zhao
# @FileName: write_to_sql.py
# @Software: PyCharm
# @Email ：yan.zhao@bowmicro.com

import json
import requests
import time
import cx_Oracle
import psycopg2
import numpy as np
import pandas as pd
import akshare as ak
from sqlalchemy import create_engine
from sympy import *
from datetime import datetime
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from scipy.optimize import curve_fit
from sklearn.metrics import mean_squared_error

font = FontProperties(fname=r"./simsun.ttc", size=14)


def df_link_pgsql():
    epidemic_dxy_df = ak.epidemic_dxy(indicator="全国")
    # print(type(epidemic_dxy_df))  <class 'pandas.core.frame.DataFrame'>
    print(epidemic_dxy_df)

    engine = create_engine(
        "postgres://{}:{}@{}/{}".format('postgres', '123456', '127.0.0.1:5432', 'postgres'))
    con = engine.connect()  # 创建连接
    epidemic_dxy_df.to_sql(name='student',  con=engine, if_exists='replace', index=False)


def df_link_oraclesql():
    df = ak.epidemic_dxy(indicator="全国")
    # print(type(epidemic_dxy_df))  <class 'pandas.core.frame.DataFrame'>
    print(df)

    film_dict = {}
    film = []

    film_dict['area'] = df['地区简称'].tolist()
    film_dict['confirm'] = df['现存确诊'].tolist()
    film_dict['confirm_total'] = df['累计确诊'].tolist()
    film_dict['dead'] = df['死亡'].tolist()
    film_dict['heal'] = df['治愈'].tolist()
    film.append(film_dict)

    conn = cx_Oracle.connect('tableau', 'tableau', '192.168.50.80:1521/bowdev', encoding="UTF-8", nencoding="UTF-8")
    cursor = conn.cursor()

    # cursor.execute("DROP TABLE AREA")
    # cursor.execute('create table AREA(area varchar2(30),confirm int,confirm_total int ,dead int, heal int)')

    sql_delect = "DELETE FROM AREA"
    cursor.execute(sql_delect)

    for i in range(0, 35):
        try:
            sql_insert = "INSERT INTO AREA(area,confirm,confirm_total,dead,heal) VALUES ('{}',{},{},{},{})".format(film_dict['area'][i], film_dict['confirm'][i], film_dict['confirm_total'][i], film_dict['dead'][i], film_dict['heal'][i])
            cursor.execute(sql_insert)
        except:
            continue
    cursor.execute("select * from AREA")
    rows = cursor.fetchall()
    print('--------------------------------------------------------------------------------------')
    for row in rows:
        print('地区=' + str(row[0]) + ' 现存确诊=' + str(row[1]) + '累计确诊 =' + str(row[2]) + ' 死亡=' + str(row[3]) + ' 治愈=' + str(row[4]))
    print('--------------------------------------------------------------------------------------\n')

    cursor.close()
    conn.commit()
    conn.close()


def catch_daily():
    """抓取每日确诊和死亡数据"""

    url = 'https://view.inews.qq.com/g2/getOnsInfo?name=wuwei_ww_cn_day_counts&callback=&_=%d' % int(time.time() * 1000)
    data = json.loads(requests.get(url=url).json()['data'])
    data.sort(key=lambda x: x['date'])

    date_list = list()  # 日期
    confirm_list = list()  # 确诊
    suspect_list = list()  # 疑似
    dead_list = list()  # 死亡
    heal_list = list()  # 治愈
    for item in data:
        month, day = item['date'].split('/')
        date_list.append(datetime.strptime('2020-%s-%s' % (month, day), '%Y-%m-%d'))
        confirm_list.append(int(item['confirm']))
        suspect_list.append(int(item['suspect']))
        dead_list.append(int(item['dead']))
        heal_list.append(int(item['heal']))

    return date_list, confirm_list, suspect_list, dead_list, heal_list

def fitting():
    """对数据进行多项式拟合"""
    date_list, confirm_list, suspect_list, dead_list, heal_list = catch_daily()  # 获取数据

    data_x = range(len(confirm_list))
    data_y = confirm_list

    x = np.asarray(data_x)
    y = np.asarray(data_y)

    # 用n次多项式拟合
    f1 = np.polyfit(x, y, 10)
    p1 = np.poly1d(f1)
    print(p1)

    # 也可使用yvals=np.polyval(f1, x)
    yvals = p1(x)  # 拟合y值
    return yvals


def plot_confirm():
    """绘制拟合数据图像"""

    yvals = fitting()

    date_list, confirm_list, suspect_list, dead_list, heal_list = catch_daily()  # 获取数据
    # 绘图

    plt.rcParams['font.sans-serif'] = 'SimHei'    # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False   # 用来正常显示负号

    plot1 = plt.plot(date_list, confirm_list, linestyle='-', color='b', label='original values')
    plot2 = plt.plot(date_list, yvals, color='r', label='polyfit values')
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))  # 格式化时间轴标注
    plt.gcf().autofmt_xdate()  # 优化标注（自动倾斜）
    plt.grid(linestyle=':')  # 显示网格
    plt.xlabel('Date')
    plt.ylabel('China Confirm')
    plt.legend(loc=4)  # 指定legend的位置右下角
    plt.title('China Confirm Curve')
    plt.show()


def diff_dx():
    x, p1 = fitting()
    x = Symbol("x")
    dx = diff(p1, x)
    print(dx)


if __name__ == '__main__':
    # df_link_pgsql()
    # df_link_oraclesql()
    plot_confirm()

