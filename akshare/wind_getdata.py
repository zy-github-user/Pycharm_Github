# -*- coding: utf-8 -*-
# @Time    : 2020/3/12 11:58 上午
# @Author  : yan.zhao
# @FileName: wind_getdata.py
# @Software: PyCharm
# @Email ：yan.zhao@bowmicro.com
import numpy as np
import pandas as pd
import datetime as dt
import time
import requests
import json
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
mpl.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
from scipy.optimize import curve_fit
from sklearn.metrics import mean_squared_error

def load_data():
    # 下载原始数据，数据来源为WindQuant提供的Wind数据接口
    # "Nation","Hubei","Outside"，分别表示全国、省内和省外的累计确诊人数
    # 需要填写自己的WindQuant用户ID
    userid = "94ac606a-c220-46af-abf3"
    indicators = "S6274770,S6275447,S6291523"
    factors_name = ["Nation","Hubei","Outside"]
    startdate = "2020-01-16"
    enddate = dt.datetime.strftime(dt.date.today() + dt.timedelta(-1),"%Y-%m-%d")# 数据的结束日期设置为昨天
    url = '''https://www.windquant.com/qntcloud/data/edb?userid={}&indicators={}&startdate={}&enddate={}'''.format(
            userid,indicators,startdate,enddate)
    response = requests.get(url)
    data = json.loads(response.content.decode("utf-8"))
    try:
        time_list = data["times"]
        value_list = data["data"]
        for i in range(len(time_list)):
            time_list[i] = time.strftime("%Y-%m-%d", time.localtime(time_list[i]/1000))
        result = pd.DataFrame(columns=factors_name, index = time_list)
        for i in range(len(factors_name)):
            result[factors_name[i]] = value_list[i]
        print(result)
        result.to_csv(r"Data\LogisticData.csv")
        return result
    except Exception as e:
        print("服务异常")

def data_abstract(result,area):
    # result：下载的原始数据
    # area：“Hubei”或“Outside”，分别返回省内和省外的累计确诊人数
    y_data = result[area]
    # 删除缺失值并转换为float型
    y_data[y_data == 'NaN'] = np.NAN
    y_data = y_data.dropna()
    y_data = y_data.astype(float)
    global first_date # 后续数据可视化需要
    first_date = dt.datetime.strptime(y_data.index[0],'%Y-%m-%d')
    # 返回与数据集等长的从0开始的时间序列作为logistic函数的自变量
    x_data = np.asarray(range(0,len(y_data)))
    return x_data, y_data

hyperparameters_r = None
hyperparameters_K = None
def logistic_increase_function(t,P0):
    # logistic生长函数：t:time   P0:initial_value    K:capacity  r:increase_rate
    # 后面将对r和K进行网格优化
    r = hyperparameters_r
    K = hyperparameters_K
    exp_value = np.exp(r * (t))
    return (K * exp_value * P0) / (K + (exp_value - 1) * P0)

def fitting(logistic_increase_function, x_data, y_data):
    # 传入要拟合的logistic函数以及数据集
    # 返回拟合结果
    popt = None
    mse = float("inf")
    i = 0
    # 网格搜索来优化r和K参数
    r = None
    k = None
    k_range = np.arange(10000, 80000, 1000)
    r_range = np.arange(0, 1, 0.01)
    for k_ in k_range:
        global hyperparameters_K
        hyperparameters_K = k_
        for r_ in r_range:
            global hyperparameters_r
            hyperparameters_r = r_
            # 用非线性最小二乘法拟合
            popt_, pcov_ = curve_fit(logistic_increase_function, x_data, y_data, maxfev = 4000)
            # 采用均方误准则选择最优参数
            mse_ = mean_squared_error(y_data, logistic_increase_function(x_data, *popt_))
            if mse_ <= mse:
                mse = mse_
                popt = popt_
                r = r_
                k = k_
            i = i+1
            print('\r当前进度：{0}{1}%'.format('▉'*int(i*10/len(k_range)/len(r_range)),int(i*100/len(k_range)/len(r_range))), end='')
    print('拟合完成')
    hyperparameters_K = k
    hyperparameters_r = r
    popt, pcov = curve_fit(logistic_increase_function, x_data, y_data)
    print("K:capacity  P0:initial_value   r:increase_rate")
    print(hyperparameters_K, popt, hyperparameters_r)
    return hyperparameters_K, hyperparameters_r, popt

def predict(logistic_increase_function, popt):
    # 根据最优参数进行预测
    future = np.linspace(0, 60, 60)
    future = np.array(future)
    future_predict = logistic_increase_function(future, popt)
    diff = np.diff(future_predict)
    diff = np.insert(diff, 0, np.nan)
    return future, future_predict, diff

def visualize(area, future, future_predict, x_data, y_data, diff):
    # 绘图
    x_show_data_all = [(first_date + (dt.timedelta(days=i))).strftime("%m-%d") for i in future]
    x_show_data = x_show_data_all[:len(x_data)]
    plt.figure(figsize=(12, 6), dpi=300)
    plt.scatter(x_show_data, y_data, s=35, marker='.', c = "dimgray", label="确诊人数")
    plt.plot(x_show_data_all, future_predict, 'r', linewidth=1.5, label='预测曲线')
    plt.plot(x_show_data_all, diff, "r", c='darkorange',linewidth=1.5, label='一阶差分')
    plt.tick_params(labelsize=10)
    plt.xticks(x_show_data_all)
    plt.grid()  # 显示网格
    plt.legend()  # 指定legend的位置右下角
    ax = plt.gca()
    for label in ax.xaxis.get_ticklabels():
        label.set_rotation(45)
    if area == "Hubei":
        plt.ylabel('湖北省累计确诊人数')
        plt.savefig(r"Data\Hubei.png",dpi=300)
    else:
        plt.ylabel('湖北省外累计确诊人数')
        plt.savefig(r"Data\Outside.png",dpi=300)
    plt.show()

if __name__ == '__main__':
    # 载入数据
    result = load_data()
    for area in ["Outside", "Hubei"]:
        # 从原始数据中提取对应数据
        x_data, y_data = data_abstract(result, area)
        # 拟合并通过网格调参寻找最优参数
        K, r, popt = fitting(logistic_increase_function, x_data, y_data)
        # 模型预测
        future, future_predict, diff= predict(logistic_increase_function, popt)
        # 绘制图像
        visualize(area, future, future_predict, x_data, y_data, diff)
