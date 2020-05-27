# -*- coding: utf-8 -*-

# @Time    : 2020/3/10
# @Author  : yan.zhao
# @FileName: getdate_1.py
# @Software: pycharm
# @Email ：yan.zhao@bowmicro.com

import time
import json
import sched
import requests
import time
import xlrd
import cx_Oracle
import psycopg2
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.figure
from datetime import datetime
from matplotlib.font_manager import FontProperties
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
import matplotlib.animation as animation

plt.rcParams['font.sans-serif'] = ['FangSong']  # 设置默认字体
plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像时'-'显示为方块的问题


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
        date_list.append(datetime.strptime('2020-%s-%s' % (month, day), '%Y-%m-%d').date())
        confirm_list.append(int(item['confirm']))
        suspect_list.append(int(item['suspect']))
        dead_list.append(int(item['dead']))
        heal_list.append(int(item['heal']))

    return data, date_list, confirm_list, suspect_list, dead_list, heal_list


def write_to_excel():

    data, date_list, confirm_list, suspect_list, dead_list, heal_list = catch_daily()  # 获取数据
    c = {"date_list": date_list, "confirm_list": confirm_list}  # 将列表转换成字典
    china_data = pd.DataFrame(c)  # 将字典转换成为数据框
    # print(china_data)
    # 把DataFrame写入数据库中
    china_data.to_excel('test2.xlsx', sheet_name='Data1', encoding='utf-8')


def link_to_pgsql():
    """写入到postgre数据库"""

    data, date_list, confirm_list, suspect_list, dead_list, heal_list = catch_daily()  # 获取数据
    # 连接数据库
    conn = psycopg2.connect(database="postgres", user="postgres", password="123456", host="127.0.0.1", port="5432")
    cursor = conn.cursor()
    # 创建表
    cursor.execute('create table CHINA(id serial primary key,date date,confirm int,suspect int ,dead int, heal int);')

    film_dict = {}
    film = []

    film_dict['date'] = date_list
    film_dict['confirm'] = confirm_list
    film_dict['suspect'] = suspect_list
    film_dict['dead'] = dead_list
    film_dict['heal'] = heal_list
    film.append(film_dict)

    for i in range(len(data)):
        sql = "INSERT INTO CHINA (date,confirm,suspect,dead,heal) VALUES ('{}',{},{},{},{});".format(film_dict['date'][i],
                film_dict['confirm'][i], film_dict['suspect'][i], film_dict['dead'][i], film_dict['heal'][i])
        cursor.execute(sql)

    conn.commit()

    cursor.close()
    conn.close()


def link_to_oracle():
    """写入到oracle数据库"""

    data, date_list, confirm_list, suspect_list, dead_list, heal_list = catch_daily()  # 获取数据
    # 连接数据库
    # conn = cx_Oracle.connect('tableau/tableau@192.168.50.80:1521/bowdev')
    conn = cx_Oracle.connect('tableau', 'tableau', '192.168.50.80:1521/bowdev')
    cursor = conn.cursor()
    # 创建表
    #cursor.execute('create table CHINA(chinadate date,confirm int,suspect int ,dead int, heal int);')

    film_dict = {}
    film = []

    film_dict['date'] = date_list
    film_dict['confirm'] = confirm_list
    film_dict['suspect'] = suspect_list
    film_dict['dead'] = dead_list
    film_dict['heal'] = heal_list
    film.append(film_dict)

    #sql = "INSERT INTO CHINA(chinadate,confirm,suspect,dead,heal) VALUES(to_date('2019-01-10','YYYY-MM-DD'),20,10,11,12)"

    sql_delect = "DELETE FROM CHINA"
    cursor.execute(sql_delect)

    for i in range(len(data)):
        sql_insert = "INSERT INTO CHINA (chinadate,confirm,suspect,dead,heal) VALUES (to_date('{}','YYYY-MM-DD'),{},{},{},{})".format(film_dict['date'][i],
                film_dict['confirm'][i], film_dict['suspect'][i], film_dict['dead'][i], film_dict['heal'][i])
        cursor.execute(sql_insert)
        print(sql_insert)  # 打印出执行sql的结果

    sql_select = "SELECT * FROM CHINA"
    cursor.execute(sql_select)

    # oracle此处顺序不能错
    cursor.close()
    conn.commit()

    conn.close()


def plot_daily():
    """绘制每日确诊和死亡数据"""

    data, date_list, confirm_list, suspect_list, dead_list, heal_list = catch_daily()  # 获取数据

    plt.figure('2019-nCoV_table', facecolor='#f4f4f4', figsize=(10, 8))
    plt.title('2019-nCoV_curve', fontsize=20)

    plt.plot(date_list, confirm_list, label='CN_confirmed')
    plt.plot(date_list, suspect_list, label='CN_suspected')
    plt.plot(date_list, dead_list, label='CN_died')
    plt.plot(date_list, heal_list, label='CN_healed')

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))  # 格式化时间轴标注
    plt.gcf().autofmt_xdate()  # 优化标注（自动倾斜）
    plt.grid(linestyle=':')  # 显示网格
    plt.legend(loc='best')  # 显示图例
    plt.savefig('2019-nCoV_add.png')  # 保存为文件
    plt.show()


def plot_globel():
    """绘制每日确诊和死亡数据"""

    data, date_list, confirm_list, suspect_list, dead_list, heal_list = catch_daily()  # 获取数据

    #print(len(date_list))

    # 意大利
    x_itali = xlrd.open_workbook("itail.xlsx")
    sheet1 = x_itali.sheet_by_name("工作表1")
    itali_confirm = sheet1.col_values(1, 1, 62)  # 取第2列，第1~71行（不含第5行）,返回一个list
    date_list_itali = date_list[18:]

    # 美国
    x_amrican = xlrd.open_workbook("amrican_china.xlsx")
    sheet1 = x_amrican.sheet_by_name("plan")
    am_confirm = sheet1.col_values(1, 2, 98)  # 取第2列，第1~71行（不含第5行）,返回一个list
    #am_add = sheet1.col_values(2, 1, 72)
    #print(len(am_add))
    date_list_am = date_list

    # 韩国
    x_korea = xlrd.open_workbook("korea.xlsx")
    sheet1 = x_korea.sheet_by_name("工作表1")
    korea_confirm = sheet1.col_values(1, 1, 72)  # 取第2列，第1~71行（不含第5行）,返回一个list
    date_list_korea = date_list[8:]

    # 伊朗
    x_iran = xlrd.open_workbook("iran.xlsx")
    sheet1 = x_iran.sheet_by_name("工作表1")
    iran_confirm = sheet1.col_values(1, 1, 42)  # 取第2列，第1~71行（不含第5行）,返回一个list
    date_list_iran = date_list[38:]

    # 中国的每日增长
    x2 = xlrd.open_workbook("test1.xlsx")
    sheet1 = x2.sheet_by_name("Data1")
    cn_add = sheet1.col_values(1, 1, 72)  # 取第2列，第0~5行（不含第5行）,返回一个list
    #print(len(cn_add))

    plt.figure('2019-nCoV_table', facecolor='#f4f4f4', figsize=(10, 8))
    plt.title('2019-nCoV_curve', fontsize=20)

    plt.plot(date_list, confirm_list, 'b', label='CN_confirmed')
    plt.plot(date_list_itali, itali_confirm, 'g', label='IT_confirmed')
    plt.plot(date_list_iran, iran_confirm, 'y', label='IR_confirmed')
    plt.plot(date_list_am, am_confirm, 'r', label='US_confirmed')
    plt.plot(date_list_korea, korea_confirm, 'c', label='KR_confirmed')

    #plt.plot(date_list, suspect_list, label='suspect')
    #plt.plot(date_list, dead_list, label='dead')
    #plt.plot(date_list, heal_list, label='heal')

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))  # 格式化时间轴标注
    plt.gcf().autofmt_xdate()  # 优化标注（自动倾斜）
    plt.grid(linestyle=':')  # 显示网格
    plt.legend(loc='best')  # 显示图例
    plt.savefig('2019-nCoV_glb.png')  # 保存为文件
    plt.show()


def schedule_excute(inc=6000):
    """定时任务"""
    # enter四个参数分别为：间隔事件、优先级（用于同时间到达的两个事件同时执行时定序）、被调用触发的函数，
    # 给该触发函数的参数（tuple形式）
    schedule.enter(0, 0, link_to_oracle, (inc,))
    schedule.run()


def dead_heal_rate():
    """计算死亡率和治愈率"""

    data, date_list, confirm_list, suspect_list, dead_list, heal_list = catch_daily()  # 获取数据
    # 死亡率
    dead_rate = [round(dead_list[i] / confirm_list[i], 4) for i in range(min(len(dead_list), len(confirm_list)))]
    # 治愈率
    heal_rate = [round(heal_list[i] / confirm_list[i], 4) for i in range(min(len(heal_list), len(confirm_list)))]
    # 治愈/死亡
    dead_heal = [round(heal_list[i] / dead_list[i], 4) for i in range(min(len(heal_list), len(dead_list)))]

    average_dead = np.mean(dead_rate)
    print(average_dead)
    average_heal = np.mean(heal_rate)
    print(average_heal)
    average_dead_heal = np.mean(dead_heal)
    print(average_dead_heal)
    return dead_rate, heal_rate, dead_heal


def plot_dhrate():
    """绘制每日死亡率和治愈率数据"""
    data, date_list, confirm_list, suspect_list, dead_list, heal_list = catch_daily()
    dead_rate, heal_rate, dead_heal = dead_heal_rate()  # 获取数据

    plt.figure('2019-nCoV_rate_table', facecolor='#f4f4f4', figsize=(10, 8))
    plt.title('2019-nCoV_rate_curve', fontsize=20)

    plt.plot(date_list, dead_rate, label='dead_rate')
    plt.plot(date_list, heal_rate, label='heal_rate')
    plt.plot(date_list, dead_heal, label='dead_heal')

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))  # 格式化时间轴标注
    plt.gcf().autofmt_xdate()  # 优化标注（自动倾斜）
    plt.grid(linestyle=':')  # 显示网格
    plt.legend(loc='best')  # 显示图例
    plt.savefig('2019-nCoV_rate_curve.png')  # 保存为文件
    plt.show()


def plot_US_CN():
    """绘制每日确诊和死亡数据"""

    data, date_list, confirm_list, suspect_list, dead_list, heal_list = catch_daily()  # 获取数据


    # 美国
    x_amrican = xlrd.open_workbook("amrican.xlsx")
    sheet1 = x_amrican.sheet_by_name("plan")
    am_confirm = sheet1.col_values(1, 1, 80)  # 取第2列，第1~71行（不含第5行）,返回一个list
    am_add = sheet1.col_values(2, 1, 80)
    am_dead = sheet1.col_values(3, 1, 80)

    date_list_am = date_list[1:]

    # 中国的每日增长
    x_cn_add = xlrd.open_workbook("amrican_china.xlsx")
    sheet1 = x_cn_add.sheet_by_name("plan")
    cn_add = sheet1.col_values(4, 1, 80)  # 取第2列，第0~5行（不含第5行）,返回一个list
    cn_date = date_list[8:]

    plt.figure('2019-nCoV_table', facecolor='#f4f4f4', figsize=(10, 8))
    plt.title('2019-nCoV_add_curve', fontsize=20)
    # 确诊人数
    #plt.plot(date_list, confirm_list, 'b', label='CN_confirm')
    #plt.plot(date_list_am, am_confirm, 'r', label='US_confirm')
    # 死亡人数
    #plt.plot(date_list, dead_list, 'b', label='CN_Dead')
    #plt.plot(date_list_am, am_dead, 'r', label='US_Dead')
    # 增加人数
    plt.plot(cn_date, cn_add, 'b', label='CN_Add')
    plt.plot(date_list_am, am_add, 'r', label='US_Add')


    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))  # 格式化时间轴标注
    plt.gcf().autofmt_xdate()  # 优化标注（自动倾斜）
    plt.grid(linestyle=':')  # 显示网格
    plt.legend(loc='best')  # 显示图例
    plt.savefig('2019-nCoV_us&cn.png')  # 保存为文件
    plt.show()


if __name__ == '__main__':
    #write_to_excel()
    # plot_logistic
    #dead_heal_rate()
    #plot_dhrate()
    # catch_daily()
    #plot_daily()
    # link_to_oracle()
    # link_to_pgsql()
    # schedule_excute(86400)
    #plot_globel()
    plot_US_CN()
