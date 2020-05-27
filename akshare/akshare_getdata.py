# -*- coding: utf-8 -*-
# @Time    : 2020/3/12 11:47 上午
# @Author  : yan.zhao
# @FileName: akshare_getdata.py
# @Software: PyCharm
# @Email ：yan.zhao@bowmicro.com
import akshare as ak
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd


def df_getdata():
    df = ak.covid_19_baidu(indicator="国外分国详情")
    # print(type(epidemic_dxy_df))  <class 'pandas.core.frame.DataFrame'>
    film_dict = {}
    film = []

    film_dict['area'] = df['area'].tolist()
    film_dict['confirm'] = df['confirmed'].tolist()
    film_dict['confirm_total'] = df['curConfirm'].tolist()
    film_dict['dead'] = df['died'].tolist()
    film_dict['heal'] = df['crued'].tolist()
    film.append(film_dict)
    # 把DataFrame写入excel中
    df.to_excel('test1.xlsx', sheet_name='Data1', encoding='utf-8')

    plt.figure('2019-nCoV_table', facecolor='#f4f4f4', figsize=(10, 8))
    plt.title('2019-nCoV_curve', fontsize=20)

    plt.bar(film_dict['area'], film_dict['confirm'])


    #plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))  # 格式化时间轴标注
    plt.gcf().autofmt_xdate()  # 优化标注（自动倾斜）
    plt.grid(linestyle=':')  # 显示网格
    plt.legend(loc='best')  # 显示图例
    plt.savefig('2019-nCoV_bar.png')  # 保存为文件
    plt.show()


if __name__ == "__main__":
    # 显示所有行
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)

    covid_19_baidu_df = ak.covid_19_baidu(indicator="中国分城市详情")
    print(covid_19_baidu_df)

    city = ak.covid_19_dxy(indicator="中国疫情分市统计详情")
    print(city)
    #province = ak.covid_19_dxy(indicator="中国疫情分省统计详情")


    covid_19_baidu_df.to_excel('city1.xlsx', sheet_name='Data1', encoding='utf-8')
    #province.to_excel('province1.xlsx', sheet_name='Data1', encoding='utf-8')