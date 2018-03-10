#encoding: UTF-8
import pandas as pd
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from matplotlib.dates import AutoDateLocator, DateFormatter
from matplotlib.font_manager import FontManager, FontProperties  
import matplotlib.dates as dt
import datetime
import sys,os
from matplotlib_ch import set_ch



if __name__ == '__main__':
    """
    股票上涨因素分析， 分析最近15日股票上涨的因素：
    市值分布
    价格分布
    流通市值分布
    ROE分布
    PE分布
    PB分布
    PS分布？
    PC分布？
    """
    set_ch()
    #start_date = '2012-08-10'
    #end_date = '2014-02-01'
    industry_filter = '软件服务'
    working_folder = '/Users/huiyang/Documents/SPSS modeler/复盘/'
    filename = 'today_all_roe_pb_rsi'
    today_all_roe_pb_rsi = pd.read_excel(working_folder + filename + '.xlsx')
    if industry_filter:
        today_all_roe_pb_rsi = today_all_roe_pb_rsi[today_all_roe_pb_rsi.industry == industry_filter]
    #today_all_roe_pb_rsi['code'] = today_all_roe_pb_rsi['code'].map(lambda x: str(x).zfill(6))

    fig, axes = plt.subplots(nrows=2, ncols=4, figsize=(50, 10))
    fig.suptitle('股票因子分析')

    axes[0, 0].set_title(u'市值分布')
    axes[0, 0].grid(color='gray', which='both', linestyle='-', linewidth=1)
    axes[0, 0].set_ylabel('mktcap')
    axes[0, 0].plot(today_all_roe_pb_rsi['rsi_14days'], today_all_roe_pb_rsi['mktcap'], 'o')

    axes[0, 1].set_title(u'价格分布')
    axes[0, 1].grid(color='gray', which='both', linestyle='-', linewidth=1)
    axes[0, 1].set_ylabel('open')
    axes[0, 1].plot(today_all_roe_pb_rsi['rsi_14days'], today_all_roe_pb_rsi['open'], 'o')

    axes[0, 2].set_title(u'roe/pb 分布')
    axes[0, 2].set_ylabel('roe/pb')
    axes[0, 2].grid(color='gray', which='both', linestyle='-', linewidth=1)
    axes[0, 2].plot(today_all_roe_pb_rsi['rsi_14days'], today_all_roe_pb_rsi['roe/pb'], 'o')

    axes[0, 3].set_title(u'profit 分布')
    axes[0, 3].set_ylabel('profit')
    axes[0, 3].grid(color='gray', which='both', linestyle='-', linewidth=1)
    axes[0, 3].plot(today_all_roe_pb_rsi['rsi_14days'], today_all_roe_pb_rsi['profit'], 'o')

    axes[1, 0].set_title(u'PE分布')
    axes[1, 0].set_ylabel('pe')
    axes[1, 0].grid(color='gray', which='both', linestyle='-', linewidth=1)
    axes[1, 0].plot(today_all_roe_pb_rsi['rsi_14days'], today_all_roe_pb_rsi['pe'], 'o')

    axes[1, 1].set_title(u'PB分布')
    axes[1, 1].set_ylabel('pb')
    axes[1, 1].grid(color='gray', which='both', linestyle='-', linewidth=1)
    axes[1, 1].plot(today_all_roe_pb_rsi['rsi_14days'], today_all_roe_pb_rsi['pb'], 'o')

    axes[1, 2].set_title(u'ROE分布')
    axes[1, 2].set_ylabel('roe_mean')
    axes[1, 2].grid(color='gray', which='both', linestyle='-', linewidth=1)
    axes[1, 2].plot(today_all_roe_pb_rsi['rsi_14days'], today_all_roe_pb_rsi['roe_mean'], 'o')

    axes[1, 3].set_title(u'地区分布')
    axes[1, 3].set_ylabel('area')
    axes[1, 3].grid(color='gray', which='both', linestyle='-', linewidth=1)
    axes[1, 3].plot(today_all_roe_pb_rsi['rsi_14days'], today_all_roe_pb_rsi['area'], 'o')

    #axes[1, 3].set_title('PC分布')
    #axes[1, 3].grid(color='gray', which='both', linestyle='-', linewidth=1)
    #axes[1, 3].plot(today_all_roe_pb_rsi['percentage'], today_all_roe_pb_rsi['PC_TTM'], 'o')


    plt.show()

