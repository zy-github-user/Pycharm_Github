# -*- coding: utf-8 -*-
# @Time    : 2020/3/13 10:35 上午
# @Author  : yan.zhao
# @FileName: logitic_3.py
# @Software: PyCharm
# @Email ：yan.zhao@bowmicro.com

import json
from datetime import datetime
import xlrd
import time
import math
import matplotlib.pyplot as plt
import numpy as np
import requests
from matplotlib.font_manager import FontProperties
from scipy.optimize import curve_fit
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error

plt.rcParams['font.family'] = ['Hiragino Sans GB']

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


"""Logistic模型集合，不同r情况下的模型"""


# K是种群极限容量，P0为种群初始数量，r为增长率
# 该模型符合病毒感染的大体规律，即开始很快，后面变慢，总感染人数趋于常数。
def logistic_increase_function(t, K, P0, r):
     r = 0.231
     t0 = 1
     exp_value = np.exp(r * (t - t0))
     return (K * exp_value * P0) / (K + (exp_value - 1) * P0)


# 黄色
def logistic_increase_function_2(t, K, P0, r):
    r = 0.09
    t0 = 1
    exp_value = np.exp(r * (t - t0))
    return (K * exp_value * P0) / (K + (exp_value - 1) * P0)


"""模拟计算过程"""
# 日期与感染人数
data, date_list, confirm_list, suspect_list, dead_list, heal_list = catch_daily()  # 获取数据
print(date_list)
# 美国
x_amrican = xlrd.open_workbook("UK.xlsx")
sheet1 = x_amrican.sheet_by_name("plan")
am_confirm = sheet1.col_values(1, 2, 108)  # 取第2列，第1~71行（不含第5行）,返回一个list

date_list_am = date_list
print(date_list_am)

t = range(len(confirm_list)-22)
t = np.array(t)
P = confirm_list[22:]
Q = am_confirm

P = np.array(P)
Q = np.array(Q)
# 最小二乘拟合，使用Logistic方程对t和p进行最小二乘拟合，其中r通过手动调整，K和P0通过拟合自动优化成参数
popt, pocv = curve_fit(logistic_increase_function, t, P)
popt1, pocv1 = curve_fit(logistic_increase_function, t, Q)
popt2, pocv2 = curve_fit(logistic_increase_function_2, t, Q)

print(popt[0], popt[1], popt[2])
print(popt1[0], popt1[1], popt1[2])
print(popt2[0], popt2[1], popt2[2])

# 拟合后对未来情况进行预测
# 利用curve_fit作简单的拟合，popt为拟合得到的参数,pcov是参数的协方差矩阵

P_predict = logistic_increase_function(t, popt[0], popt[1], popt[2])
P_predict_1 = logistic_increase_function(t, popt1[0], popt1[1], popt1[2])
P_predict_2 = logistic_increase_function_2(t, popt2[0], popt2[1], popt2[2])

# 以中国r预测英国的数据
future = range(len(confirm_list)-23, len(confirm_list)-13)
future = np.array(future)
future_predict = logistic_increase_function(future, popt1[0], popt1[1], popt1[2])

# 以英国的r预测英国的数据
tomorrow = range(len(confirm_list)-23, len(confirm_list)-13)
tomorrow = np.array(tomorrow)
tomorrow_predict = logistic_increase_function_2(tomorrow, popt2[0], popt2[1], popt2[2])

plt.figure('2019-nCoV_table', facecolor='#f4f4f4', figsize=(10, 8))
# 英国新冠病毒趋势分析及预测
plt.title('英国新冠病毒趋势分析及预测', fontsize=20)

'''图像绘制'''
# 英国实际数据
plot_US = plt.plot(t, Q, '.', label="英国实际数据")
# 英国实际数据测算趋势
plot4 = plt.plot(t, P_predict_2, 'y', label='英国实际数据测算趋势')
# 英国未来预测数据
plot5 = plt.plot(tomorrow, tomorrow_predict, label='英国未来预测数据')
# 基于中国的r数值所测算的实际趋势
plot3 = plt.plot(t, P_predict_1, 'g', label='基于中国的r数值所测算的实际趋势')
# 基于中国的r数值所预测的未来趋势
plot2 = plt.plot(future, future_predict, 'r', label='基于中国的r数值所预测的未来趋势')


r2 = r2_score(Q, P_predict_2)
print('指数函数拟合R方为:', r2)
mse = mean_squared_error(Q, P_predict_2)
rmse = mse ** 0.5
print('指数函数拟合rmse为:', rmse)


plt.xlabel('时间')
plt.ylabel('种群数目（感染人数）')
plt.gcf().autofmt_xdate()  # 优化标注（自动倾斜）
plt.grid(linestyle=':')  # 显示网格
plt.legend(loc='upper left')  # 显示图例
plt.savefig('2019-nCoV_predict_uk.png')  # 保存为文件
plt.show()
