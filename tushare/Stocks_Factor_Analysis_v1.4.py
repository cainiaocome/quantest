# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from matplotlib.dates import AutoDateLocator, DateFormatter
from matplotlib.font_manager import FontManager, FontProperties  
import matplotlib.dates as dt
from datetime import *
import dateutil.relativedelta
import sys,os
from tushare_api import tushare_api
#from matplotlib_ch import set_ch

def industryFactorAnalysis():
    working_folder = '/Users/yanghui/Documents/quantest/data_shared/tuShare/'
    filename = 'today_all_roe_pb_rsi'
    today_all_roe_pb_rsi = pd.read_excel(working_folder + filename + '.xlsx')

    industry = topIndustry(count=20, time_period=5).index[0]

    today_all_roe_pb_rsi = today_all_roe_pb_rsi[today_all_roe_pb_rsi.industry == industry]
    #today_all_roe_pb_rsi['code'] = today_all_roe_pb_rsi['code'].map(lambda x: str(x).zfill(6))
    
    font_small = FontProperties(fname='/Library/Fonts/Songti.ttc',size=8)
    font_medium = FontProperties(fname='/Library/Fonts/Songti.ttc',size=10)
    font_large=FontProperties(fname='/Library/Fonts/Songti.ttc', size=12)
    font_xlarge=FontProperties(fname='/Library/Fonts/Songti.ttc', size=14)


    #set_ch()
    plt.style.use('ggplot')
    fig, axes = plt.subplots(nrows=4, ncols=2, figsize=(11, 17))
    fig.suptitle(industry + '行业因子分析',fontproperties=font_xlarge)

    axes[0, 0].set_title(u'市值分布', fontproperties=font_large)
    axes[0, 0].grid(color='white', which='both', linestyle='-', linewidth=0.4)
    axes[0, 0].set_ylabel('mktcap',fontproperties=font_medium)
    axes[0, 0].scatter(today_all_roe_pb_rsi['rsi_14days'], today_all_roe_pb_rsi['mktcap'], c= 'r', marker='o')
    axes[0, 0].set_xlim([0, 100])
    xlabels = axes[0, 0].get_xticklabels()
    for xlabel in xlabels:
        xlabel.set_fontproperties(font_small)
    ylabels = axes[0, 0].get_yticklabels()
    for ylabel in ylabels:
        ylabel.set_fontproperties(font_small)


    axes[0, 1].set_title(u'价格分布', fontproperties=font_large)
    axes[0, 1].grid(color='white', which='both', linestyle='-', linewidth=0.4)
    axes[0, 1].set_ylabel('open',fontproperties=font_medium)
    axes[0, 1].plot(today_all_roe_pb_rsi['rsi_14days'], today_all_roe_pb_rsi['open'], 'o')
    axes[0, 1].set_xlim([0, 100])
    xlabels = axes[0, 1].get_xticklabels()
    for xlabel in xlabels:
        xlabel.set_fontproperties(font_small)
    ylabels = axes[0, 1].get_yticklabels()
    for ylabel in ylabels:
        ylabel.set_fontproperties(font_small)


    axes[1, 0].set_title(u'roe/pb 分布', fontproperties=font_large)
    axes[1, 0].set_ylabel('roe/pb',fontproperties=font_medium)
    axes[1, 0].grid(color='white', which='both', linestyle='-', linewidth=0.4)
    axes[1, 0].plot(today_all_roe_pb_rsi['rsi_14days'], today_all_roe_pb_rsi['roe/pb'], 'o')
    axes[1, 0].set_xlim([0, 100])
    xlabels = axes[1, 0].get_xticklabels()
    for xlabel in xlabels:
        xlabel.set_fontproperties(font_small)

    ylabels = axes[1, 0].get_yticklabels()
    for ylabel in ylabels:
        ylabel.set_fontproperties(font_small)



    axes[1, 1].set_title(u'profit 分布', fontproperties=font_large)
    axes[1, 1].set_ylabel('profit',fontproperties=font_medium)
    axes[1, 1].grid(color='white', which='both', linestyle='-', linewidth=0.4)
    axes[1, 1].plot(today_all_roe_pb_rsi['rsi_14days'], today_all_roe_pb_rsi['profit'], 'o')
    axes[1, 1].set_xlim([0, 100])
    xlabels = axes[1, 1].get_xticklabels()
    for xlabel in xlabels:
        xlabel.set_fontproperties(font_small)

    ylabels = axes[1, 1].get_yticklabels()
    for ylabel in ylabels:
        ylabel.set_fontproperties(font_small)


    axes[2, 0].set_title(u'PE分布', fontproperties=font_large)
    axes[2, 0].set_ylabel('pe',fontproperties=font_medium)
    axes[2, 0].grid(color='white', which='both', linestyle='-', linewidth=0.4)
    axes[2, 0].plot(today_all_roe_pb_rsi['rsi_14days'], today_all_roe_pb_rsi['pe'], 'o')
    axes[2, 0].set_xlim([0, 100])
    xlabels = axes[2, 0].get_xticklabels()
    for xlabel in xlabels:
        xlabel.set_fontproperties(font_small)

    ylabels = axes[2, 0].get_yticklabels()
    for ylabel in ylabels:
        ylabel.set_fontproperties(font_small)

    axes[2, 1].set_title(u'PB分布', fontproperties=font_large)
    axes[2, 1].set_ylabel('pb',fontproperties=font_medium)
    axes[2, 1].grid(color='white', which='both', linestyle='-', linewidth=0.4)
    axes[2, 1].plot(today_all_roe_pb_rsi['rsi_14days'], today_all_roe_pb_rsi['pb'], 'o')
    axes[2, 1].set_xlim([0, 100])
    xlabels = axes[2, 1].get_xticklabels()
    for xlabel in xlabels:
        xlabel.set_fontproperties(font_small)

    ylabels = axes[2, 1].get_yticklabels()
    for ylabel in ylabels:
        ylabel.set_fontproperties(font_small)

    axes[3, 0].set_title(u'ROE分布', fontproperties=font_large)
    axes[3, 0].set_ylabel('roe_mean',fontproperties=font_medium)
    axes[3, 0].grid(color='white', which='both', linestyle='-', linewidth=0.4)
    axes[3, 0].plot(today_all_roe_pb_rsi['rsi_14days'], today_all_roe_pb_rsi['roe_mean'], 'o')
    axes[3, 0].set_xlim([0, 100])
    xlabels = axes[3, 0].get_xticklabels()
    for xlabel in xlabels:
        xlabel.set_fontproperties(font_small)

    ylabels = axes[3, 0].get_yticklabels()
    for ylabel in ylabels:
        ylabel.set_fontproperties(font_small)

    axes[3, 1].set_title(u'地区分布', fontproperties=font_large)
    axes[3, 1].set_ylabel('area',fontproperties=font_medium)
    axes[3, 1].grid(color='white', which='both', linestyle='-', linewidth=0.4)
    axes[3, 1].plot(today_all_roe_pb_rsi['rsi_14days'], today_all_roe_pb_rsi['area'], 'o')
    axes[3, 1].set_xlim([0, 100])
    xlabels = axes[3, 1].get_xticklabels()
    for xlabel in xlabels:
        xlabel.set_fontproperties(font_small)

    ylabels = axes[3, 1].get_yticklabels()
    for ylabel in ylabels:
        ylabel.set_fontproperties(font_small)

    #axes[1, 3].set_title('PC分布', fontproperties=font_large)
    #axes[1, 3].grid(color='gray', which='both', linestyle='-', linewidth=1)
    #axes[1, 3].plot(today_all_roe_pb_rsi['percentage'], today_all_roe_pb_rsi['PC_TTM'], 'o')
    plt.show()
    return

def marketAnalysis(time_period=14):
    """
    分析整个市场的热点股票
        a. 兴登堡凶兆的走势，热点指数
        b. 最近成交量走势，流动性指标
        c. 大盘走势
        d. 最近热点行业，平均RSI最大的行业
        e. 最近热点股票
        f. 热点行业
    param: time_period = 14, 10, 5
    return: hotspot industry list
    """
    font_small = FontProperties(fname='/Library/Fonts/Songti.ttc',size=8)
    font_medium = FontProperties(fname='/Library/Fonts/Songti.ttc',size=10)
    font_large=FontProperties(fname='/Library/Fonts/Songti.ttc', size=12)
    font_xlarge=FontProperties(fname='/Library/Fonts/Songti.ttc', size=14)

    plt.style.use('ggplot')
    fig, axes = plt.subplots(nrows=4, ncols=1, figsize=(11, 17))
    #fig, axes = plt.subplot(5,2,1)
    fig.suptitle('市场分析',fontproperties=font_xlarge)
    #fig.autofmt_xdate()


    try:
        index_000001 = hindenburgOmen(index='000001').tail(30)
        #axes[0, 0] = fig.add_subplot(111)
        axes[0].set_title(u'兴登堡凶兆（上证指数）', fontproperties=font_large)
        axes[0].grid(color='white', which='both', linestyle='-', linewidth=0.4)
        axes[0].set_ylabel('R_square（上证指数）',fontproperties=font_medium)
        axes[0].plot(index_000001['date'], index_000001['hindenburg_omen_000001'], 'black', linewidth=1)
        axes[0].axhline(y=0.3, c="red",linewidth=0.5,zorder=0)
        axes[0].set_ylim([0, 1])
        xlabels = axes[0].get_xticklabels()
        for xlabel in xlabels:
            xlabel.set_rotation(90)
            xlabel.set_fontproperties(font_small)
        ylabels = axes[0].get_yticklabels()
        for ylabel in ylabels:
            ylabel.set_fontproperties(font_small)

        axes2 = axes[0].twinx()
        axes2.set_ylabel('上证指数',fontproperties=font_medium)
        axes2.plot(index_000001['date'], index_000001['close'], 'blue', linewidth=1)
        ylabels = axes2.get_yticklabels()
        for ylabel in ylabels:
            ylabel.set_fontproperties(font_small)
    except:
        pass
    
    try:
        index_399001 = hindenburgOmen(index='399001').tail(30)

        axes[1].set_title(u'兴登堡凶兆（深证成指）', fontproperties=font_large)
        axes[1].grid(color='white', which='both', linestyle='-', linewidth=0.4)
        axes[1].set_ylabel('R_square（深证成指）',fontproperties=font_medium)
        axes[1].plot(index_399001['date'], index_399001['hindenburg_omen_399001'], 'black', linewidth=1)
        axes[1].axhline(y=0.3, c="red",linewidth=0.5,zorder=0)
        axes[1].set_ylim([0, 1])
        xlabels = axes[1].get_xticklabels()
        for xlabel in xlabels:
            xlabel.set_rotation(90)
            xlabel.set_fontproperties(font_small)
        ylabels = axes[1].get_yticklabels()
        for ylabel in ylabels:
            ylabel.set_fontproperties(font_small)

        axes2 = axes[1].twinx()
        axes2.set_ylabel('深证成指',fontproperties=font_medium)
        axes2.plot(index_399001['date'], index_399001['close'], 'blue', linewidth=1)
        ylabels = axes2.get_yticklabels()
        for ylabel in ylabels:
            ylabel.set_fontproperties(font_small)
    except:
        pass

    try:
        index_399006 = hindenburgOmen(index='399006').tail(30)
        axes[2].set_title(u'兴登堡凶兆（创业板指）', fontproperties=font_large)
        axes[2].grid(color='white', which='both', linestyle='-', linewidth=0.4)
        axes[2].set_ylabel('R_square（创业板指）',fontproperties=font_medium)
        axes[2].plot(index_399006['date'], index_399006['hindenburg_omen_399006'], 'black', linewidth=1)
        #import pdb  
        #pdb.set_trace()  
        axes[2].set_ylim([0, 1])
        axes[2].axhline(y=0.3, c="red",linewidth=0.5,zorder=3)
        xlabels = axes[2].get_xticklabels()
        for xlabel in xlabels:
            xlabel.set_rotation(90)
            xlabel.set_fontproperties(font_small)
        ylabels = axes[2].get_yticklabels()
        for ylabel in ylabels:
            ylabel.set_fontproperties(font_small)
        
        axes2 = axes[2].twinx()
        axes2.grid(color='white', which='both', linestyle='--', linewidth=0.4)
        axes2.set_ylabel('创业板指',fontproperties=font_medium)
        axes2.plot(index_399006['date'], index_399006['close'], 'blue', linewidth=1)
        ylabels = axes2.get_yticklabels()
        for ylabel in ylabels:
            ylabel.set_fontproperties(font_small)
    except:
        pass


    try:
        money_supply = moneySupply().tail(30)
        axes[3].set_title(u'成交额占比', fontproperties=font_large)
        axes[3].grid(color='white', which='both', linestyle='-', linewidth=0.4)
        axes[3].set_ylabel('成交额占M0百分比',fontproperties=font_medium)
        axes[3].plot(money_supply['date'], money_supply['M0_percent'], 'black', linewidth=1)
        #axes[3].plot(money_supply['date'], money_supply['M1_percent'], 'red', linewidth=1)
        axes[3].set_ylim([0, 20])
        xlabels = axes[3].get_xticklabels()
        for xlabel in xlabels:
            xlabel.set_rotation(90)
            xlabel.set_fontproperties(font_small)
        ylabels = axes[3].get_yticklabels()
        for ylabel in ylabels:
            ylabel.set_fontproperties(font_small)
        
        axes2 = axes[3].twinx()
        axes2.set_ylabel('成交额占M1百分比',fontproperties=font_medium)
        axes2.plot(money_supply['date'], money_supply['M1_percent'], 'blue', linewidth=1)
        ylabels = axes2.get_yticklabels()
        for ylabel in ylabels:
            ylabel.set_fontproperties(font_small)
    except:
        pass

    plt.show()
    return

def topStockAnalysis(count=20):
    """
    分析整个市场的热点股票
    param: time_period = 14, 10, 5
    return: hotspot industry list
    """
    font_small = FontProperties(fname='/Library/Fonts/Songti.ttc',size=8)
    font_medium = FontProperties(fname='/Library/Fonts/Songti.ttc',size=10)
    font_large=FontProperties(fname='/Library/Fonts/Songti.ttc', size=12)
    font_xlarge=FontProperties(fname='/Library/Fonts/Songti.ttc', size=14)

    plt.style.use('ggplot')
    fig, axes = plt.subplots(nrows=3, ncols=2, figsize=(11, 17))
    fig.suptitle('股票分析（全市场）',fontproperties=font_xlarge)
    #fig.autofmt_xdate()

    try:
        top_stock = topStock(count=count, time_period=14, top_industry=False)
        axes[0, 0].set_title(u'趋势跟踪 - 14日RSI股票', fontproperties=font_large)
        axes[0, 0].grid(color='white', which='both', linestyle='-', linewidth=0.4)
        axes[0, 0].barh(top_stock['name'] + '(' + top_stock['industry'] + ')', top_stock['rsi_14days'], color='red')
        axes[0, 0].set_xlim([0, 100])
        xlabels = axes[0, 0].get_xticklabels()
        for xlabel in xlabels:
            xlabel.set_fontproperties(font_small)

        ylabels = axes[0, 0].get_yticklabels()
        for ylabel in ylabels:
            ylabel.set_fontproperties(font_small)
    except:
        pass

    try:
        top_stock = topStock(count=count, time_period=10, top_industry=False)
        axes[0, 1].set_title(u'趋势跟踪 - 10日RSI股票', fontproperties=font_large)
        axes[0, 1].grid(color='white', which='both', linestyle='-', linewidth=0.4)
        axes[0, 1].barh(top_stock['name'] + '(' + top_stock['industry'] + ')', top_stock['rsi_10days'], color='red')
        axes[0, 1].set_xlim([0, 100])
        xlabels = axes[0, 1].get_xticklabels()
        for xlabel in xlabels:
            xlabel.set_fontproperties(font_small)

        ylabels = axes[0, 1].get_yticklabels()
        for ylabel in ylabels:
            ylabel.set_fontproperties(font_small)
    except:
        pass

    try:
        top_stock = topStock(count=count, time_period=5, top_industry=False)
        axes[1, 0].set_title(u'趋势跟踪 - 5日RSI股票', fontproperties=font_large)
        axes[1, 0].grid(color='white', which='both', linestyle='-', linewidth=0.4)
        axes[1, 0].barh(top_stock['name'] + '(' + top_stock['industry'] + ')', top_stock['rsi_5days'], color='red')
        axes[1, 0].set_xlim([0, 100])
        xlabels = axes[1, 0].get_xticklabels()
        for xlabel in xlabels:
            xlabel.set_fontproperties(font_small)

        ylabels = axes[1, 0].get_yticklabels()
        for ylabel in ylabels:
            ylabel.set_fontproperties(font_small)
    except:
        pass


    # 14 days RSI < 60 and 5 days RSI > 70
    #try:
    #    top_stock = topStock(count=count, time_period=5, top_industry=False, rsi_min=50)
    #    axes[1, 0].set_title(u'趋势反转 - 14日RSI < 50 & 5日RSI > 70')
    #    axes[1, 0].grid(color='white', which='both', linestyle='-', linewidth=0.4)
    #    axes[1, 0].barh(top_stock['name'] + '(' + top_stock['industry'] + ')', top_stock['rsi_5days'], color='red')
    #    axes[1, 0].set_xlim([0, 100])
    #except:
    #    pass

    try:
        top_stock = topPercentStock(count=count, time_period=2, top_industry=False)
        axes[1, 1].set_title(u'趋势跟踪 - 2日涨幅股票', fontproperties=font_large)
        axes[1, 1].grid(color='white', which='both', linestyle='-', linewidth=0.4)
        axes[1, 1].barh(top_stock['name'] + '(' + top_stock['industry'] + ')', top_stock['2days_percentage'], color='red')
        #axes[1, 1].set_xlim([0, 100])
        xlabels = axes[1, 1].get_xticklabels()
        for xlabel in xlabels:
            xlabel.set_fontproperties(font_small)
        ylabels = axes[1, 1].get_yticklabels()
        for ylabel in ylabels:
            ylabel.set_fontproperties(font_small)
    except:
        pass

    try:
        top_stock = topPercentStock(count=count, time_period=5, top_industry=False)
        axes[2, 0].set_title(u'趋势跟踪 - 5日涨幅股票', fontproperties=font_large)
        axes[2, 0].grid(color='white', which='both', linestyle='-', linewidth=0.4)
        axes[2, 0].barh(top_stock['name'] + '(' + top_stock['industry'] + ')', top_stock['5days_percentage'], color='red')
        #axes[1, 0].set_xlim([0, 100])
        xlabels = axes[2, 0].get_xticklabels()
        for xlabel in xlabels:
            xlabel.set_fontproperties(font_small)

        ylabels = axes[2, 0].get_yticklabels()
        for ylabel in ylabels:
            ylabel.set_fontproperties(font_small)
    except:
        pass

    try:
        top_stock = topPercentStock(count=count, time_period=10, top_industry=False)
        axes[2, 1].set_title(u'趋势跟踪 - 10日涨幅股票', fontproperties=font_large)
        axes[2, 1].grid(color='white', which='both', linestyle='-', linewidth=0.4)
        axes[2, 1].barh(top_stock['name'] + '(' + top_stock['industry'] + ')', top_stock['10days_percentage'], color='red')
        #axes[1, 0].set_xlim([0, 100])
        xlabels = axes[2, 1].get_xticklabels()
        for xlabel in xlabels:
            xlabel.set_fontproperties(font_small)
        ylabels = axes[2, 1].get_yticklabels()
        for ylabel in ylabels:
            ylabel.set_fontproperties(font_small)
    except:
        pass
    plt.show()
    return

def topIndustryAnalysis(count=20):

    font_small = FontProperties(fname='/Library/Fonts/Songti.ttc',size=8)
    font_medium = FontProperties(fname='/Library/Fonts/Songti.ttc',size=10)
    font_large=FontProperties(fname='/Library/Fonts/Songti.ttc', size=12)
    font_xlarge=FontProperties(fname='/Library/Fonts/Songti.ttc', size=14)

    plt.style.use('ggplot')
    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(11, 17))
    fig.suptitle('行业分析',fontproperties=font_xlarge)

    try: 
        top_industry = topIndustry(count=20, time_period=14)
        top_industry['rsi_count'] = top_industry['rsi_count'].map(lambda x: str(x))
        axes[0, 0].set_title(u'最近14日热门行业', fontproperties=font_large)
        axes[0, 0].grid(color='white', which='both', linestyle='-', linewidth=0.4)
        axes[0, 0].barh(top_industry.index + '(' + top_industry['rsi_count'] + ')', top_industry['rsi_mean'], color='red')
        axes[0, 0].set_xlim([0, 100])
        xlabels = axes[0, 0].get_xticklabels()
        for xlabel in xlabels:
            xlabel.set_fontproperties(font_small)

        ylabels = axes[0, 0].get_yticklabels()
        for ylabel in ylabels:
            ylabel.set_fontproperties(font_small)
    except:
        pass

    try: 
        top_industry = topIndustry(count=20, time_period=10)
        top_industry['rsi_count'] = top_industry['rsi_count'].map(lambda x: str(x))
        axes[0, 1].set_title(u'最近10日热门行业', fontproperties=font_large)
        axes[0, 1].grid(color='white', which='both', linestyle='-', linewidth=0.4)
        axes[0, 1].barh(top_industry.index + '(' + top_industry['rsi_count'] + ')', top_industry['rsi_mean'], color='red')
        axes[0, 1].set_xlim([0, 100])
        xlabels = axes[0, 1].get_xticklabels()
        for xlabel in xlabels:
            xlabel.set_fontproperties(font_small)

        ylabels = axes[0, 1].get_yticklabels()
        for ylabel in ylabels:
            ylabel.set_fontproperties(font_small)
    except:
        pass
    
    try: 
        top_industry = topIndustry(count=20, time_period=5)
        top_industry['rsi_count'] = top_industry['rsi_count'].map(lambda x: str(x))
        axes[1, 0].set_title(u'最近5日热门行业', fontproperties=font_large)
        axes[1, 0].grid(color='white', which='both', linestyle='-', linewidth=0.4)
        axes[1, 0].barh(top_industry.index + '(' + top_industry['rsi_count'] + ')', top_industry['rsi_mean'], color='red')
        axes[1, 0].set_xlim([0, 100])
        xlabels = axes[1, 0].get_xticklabels()
        for xlabel in xlabels:
            xlabel.set_fontproperties(font_small)

        ylabels = axes[1, 0].get_yticklabels()
        for ylabel in ylabels:
            ylabel.set_fontproperties(font_small)
    except:
        pass

    try:
        top_stock = topStock(count=20, time_period=5, top_industry=True)
        industry = top_stock.iloc[0, 36]
        axes[1, 1].set_title('5日热门行业热门股票(' + industry +')', fontproperties=font_large)
        axes[1, 1].grid(color='white', which='both', linestyle='-', linewidth=0.4)
        axes[1, 1].barh(top_stock['name'], top_stock['rsi_5days'], color='red')
        axes[1, 1].set_xlim([0, 100])
        xlabels = axes[1, 1].get_xticklabels()
        for xlabel in xlabels:
            xlabel.set_fontproperties(font_small)

        ylabels = axes[1, 1].get_yticklabels()
        for ylabel in ylabels:
            ylabel.set_fontproperties(font_small)
    except:
        pass
    
    plt.show()
    return

def hindenburgOmen(index='000001'):
    path = '/Users/yanghui/Documents/quantest/tuShare/notification_monitoring_files/'
    filename = 'hindenburg_omen'
    hindenburg_omen = pd.read_excel(path + filename + '.xlsx')
    working_folder = '/Users/yanghui/Documents/quantest/data_shared/tuShare/'

    # read index
    if index == '000001':
        filename = 'index_000001'
        index_000001 = pd.read_excel(io=working_folder + filename + '.xlsx')
        index_000001['date'] = index_000001['date'].map(lambda x: x.isoformat()[:10])
        index_000001 = pd.merge(index_000001, hindenburg_omen, how='left', left_on='date', right_on='date', suffixes=('_x', '_y'))
        #index_000001['close_adjust'] = index_000001['close'].map(lambda x: x/10000)
        index_000001.sort_values(by='date', ascending=True, inplace=True)
        index_df = index_000001

    if index == '399001':
        filename = 'index_399001'
        index_399001 = pd.read_excel(io=working_folder  + filename + '.xlsx')
        index_399001['date'] = index_399001['date'].map(lambda x: x.isoformat()[:10])
        index_399001 = pd.merge(index_399001, hindenburg_omen, how='left', left_on='date', right_on='date', suffixes=('_x', '_y'))
        #index_399001['close_adjust'] = index_399001['close'].map(lambda x: x/20000)
        index_399001.sort_values(by='date', ascending=True, inplace=True)
        index_df = index_399001

    if index == '399006':
        filename = 'index_399006'
        index_399006 = pd.read_excel(io=working_folder + filename + '.xlsx')
        index_399006['date'] = index_399006['date'].map(lambda x: x.isoformat()[:10])
        index_399006 = pd.merge(index_399006, hindenburg_omen, how='left', left_on='date', right_on='date', suffixes=('_x', '_y'))
        #index_399006['close_adjust'] = index_399006['close'].map(lambda x: x/10000)
        index_399006.sort_values(by='date', ascending=True, inplace=True)
        index_df = index_399006

    return index_df

def moneySupply():
    path = '/Users/yanghui/Documents/quantest/tuShare/notification_monitoring_files/'
    working_folder = '/Users/yanghui/Documents/quantest/data_shared/tuShare/'

    # read index
    filename = 'index_000001'
    index_000001 = pd.read_excel(io=working_folder + filename + '.xlsx')
    index_000001['date'] = index_000001['date'].map(lambda x: x.isoformat()[:10])

    filename = 'index_399001'
    index_399001 = pd.read_excel(io=working_folder + filename + '.xlsx')
    index_399001['date'] = index_399001['date'].map(lambda x: x.isoformat()[:10])

    filename = 'index_399006'
    index_399006 = pd.read_excel(io=working_folder + filename + '.xlsx')
    index_399006['date'] = index_399006['date'].map(lambda x: x.isoformat()[:10])

    filename = '货币供应量_宏观数据_新浪财经'
    money_supply = pd.read_excel(path + filename + '.xlsx')

    index_000001['month'] = index_000001.apply(lambda x: x['date'][:7], axis=1)
    index_399001['month'] = index_399001.apply(lambda x: x['date'][:7], axis=1)
    index_399006['month'] = index_399006.apply(lambda x: x['date'][:7], axis=1)
    index_000001 = pd.merge(index_000001, index_399001, how='left', left_on='date', right_on='date', suffixes=('_000001', '_399001'))
    index_000001 = pd.merge(index_000001, index_399006, how='left', left_on='date', right_on='date', suffixes=('_000001', '_399006'))

    index_merge_money = pd.merge(index_000001, money_supply, how='left', left_on='month', right_on='month')
    index_merge_money.set_index(keys=['date'], inplace=True, drop=False)
    for date in index_merge_money.index:
        if index_merge_money.isnull().loc[date, ' 流通中现金(M0)(亿元)']:
            index_merge_money.loc[date, ' 流通中现金(M0)(亿元)'] = money_supply.iloc[0, 5]
            index_merge_money.loc[date, ' 货币(狭义货币M1)(亿元)'] = money_supply.iloc[0, 3]
    index_merge_money['amount_total'] = index_merge_money['amount_000001'] + index_merge_money['amount_399001'] + index_merge_money['amount']
    index_merge_money['M0_percent'] = 100 * (index_merge_money['amount_total']/100000000)/index_merge_money[' 流通中现金(M0)(亿元)']
    index_merge_money['M1_percent'] = 100 * (index_merge_money['amount_total']/100000000)/index_merge_money[' 货币(狭义货币M1)(亿元)']
    index_merge_money.sort_values(by='date', ascending=True, inplace=True)
    return index_merge_money

def topIndustry(count=20, time_period=14):
    """
    列出最热门的行业，按RSI排名
    """
    working_folder = '/Users/yanghui/Documents/quantest/data_shared/tuShare/'
    filename = 'today_all_roe_pb_rsi'
    today_all_roe_pb_rsi = pd.read_excel(io=working_folder + filename + '.xlsx')

    if time_period == 5:
        top_industry = pd.pivot_table(today_all_roe_pb_rsi, index=['industry'], values=['rsi_5days'], aggfunc=[np.mean,len])
        
    if time_period == 10:
        top_industry = pd.pivot_table(today_all_roe_pb_rsi, index=['industry'], values=['rsi_10days'], aggfunc=[np.mean,len])

    if time_period == 14:
        top_industry = pd.pivot_table(today_all_roe_pb_rsi, index=['industry'], values=['rsi_14days'], aggfunc=[np.mean,len])

    top_industry.columns = ['rsi_mean', 'rsi_count']
    top_industry['rsi_count'] = top_industry['rsi_count'].map(lambda x: int(x))
    top_industry.sort_values(by='rsi_mean', ascending=False, inplace=True)
    top_industry = top_industry.head(count)
    return top_industry

def topStock(count=10, time_period=5, top_industry=False, rsi_min=0, rsi_max=0):
    """
    列出最热门的行业的热门股票，按RSI排名
    """
    working_folder = '/Users/yanghui/Documents/quantest/data_shared/tuShare/'
    filename = 'today_all_roe_pb_rsi'
    today_all_roe_pb_rsi = pd.read_excel(io=working_folder + filename + '.xlsx')

    if top_industry:
        industry = topIndustry(count=count, time_period=time_period).index[0]
        today_all_roe_pb_rsi = today_all_roe_pb_rsi[today_all_roe_pb_rsi.industry == industry]

    if time_period == 5:
        today_all_roe_pb_rsi.sort_values(by='rsi_5days', ascending=False, inplace=True)
        
    if time_period == 10:
        today_all_roe_pb_rsi.sort_values(by='rsi_10days', ascending=False, inplace=True)

    if time_period == 14:
        today_all_roe_pb_rsi.sort_values(by='rsi_14days', ascending=False, inplace=True)

    #去除上市不足30天的股票
    market_date = (date.today() - dateutil.relativedelta.relativedelta(days=30)).isoformat()
    today_all_roe_pb_rsi['timeToMarket'] = today_all_roe_pb_rsi['timeToMarket'].map(lambda x: str(x)[:4] + '-' + str(x)[4:2] + '-' + str(x)[6:2])
    today_all_roe_pb_rsi = today_all_roe_pb_rsi[today_all_roe_pb_rsi.timeToMarket < market_date]

    if rsi_min > 0:
        today_all_roe_pb_rsi = today_all_roe_pb_rsi[today_all_roe_pb_rsi.rsi_14days <= rsi_min]

    today_all_roe_pb_rsi = today_all_roe_pb_rsi.head(count)
    return today_all_roe_pb_rsi

def topPercentStock(count=20, time_period=2, top_industry=False):
    """
    列出最热门的行业的热门股票，按RSI排名
    """
    working_folder = '/Users/yanghui/Documents/quantest/data_shared/tuShare/'
    filename = 'today_all_roe_pb_rsi'
    today_all_roe_pb_rsi = pd.read_excel(io=working_folder + filename + '.xlsx')

    if top_industry:
        industry = topIndustry(count=count, time_period=time_period).index[0]
        today_all_roe_pb_rsi = today_all_roe_pb_rsi[today_all_roe_pb_rsi.industry == industry]

    if time_period == 2:
        today_all_roe_pb_rsi.sort_values(by='2days_percentage', ascending=False, inplace=True)
        
    if time_period == 5:
        today_all_roe_pb_rsi.sort_values(by='5days_percentage', ascending=False, inplace=True)

    if time_period == 10:
        today_all_roe_pb_rsi.sort_values(by='10days_percentage', ascending=False, inplace=True)

    #去除上市不足30天的股票
    market_date = (date.today() - dateutil.relativedelta.relativedelta(days=30)).isoformat()
    today_all_roe_pb_rsi['timeToMarket'] =  \
        today_all_roe_pb_rsi['timeToMarket'].map(lambda x: str(x)[:4] + '-' + str(x)[4:2] + '-' + str(x)[6:2])
    today_all_roe_pb_rsi = today_all_roe_pb_rsi[today_all_roe_pb_rsi.timeToMarket < market_date]

    today_all_roe_pb_rsi = today_all_roe_pb_rsi.head(count)
    return today_all_roe_pb_rsi

def historyROEPB(start='2018-03-15', end='2018-07-13', industry=''):
    working_folder = '/Users/yanghui/Documents/quantest/data_shared/tuShare/'
    today_all = pd.DataFrame([])
    end = today_ISO = datetime.today().date().isoformat()
    date = start
    while (date >= start and date <= end):
        filename = 'today_all_R_square_' + str(date)
        try:
            today_all_roe_pb_rsi = pd.read_excel(io=working_folder + filename + '.xlsx') 
            # select for 银行业
            if industry == '':
                pass
            else:
                today_all_roe_pb_rsi = today_all_roe_pb_rsi[today_all_roe_pb_rsi.industry == industry] 
            today_all_row = today_all_roe_pb_rsi['roe/pb'].astype(float).groupby(today_all_roe_pb_rsi['industry']).mean() 
            today_all_row = pd.DataFrame(today_all_row)
            today_all_row['date'] = date
            today_all_row.reset_index(drop=False, inplace=True)
            today_all_row.sort_values(by=['roe/pb'], ascending=False, inplace=True)
            today_all = today_all.append(today_all_row)
        except:
            pass
        date = (datetime.strptime(date, '%Y-%m-%d') +  \
                dateutil.relativedelta.relativedelta(days=1)) \
                .date().isoformat()
        #print(date)

    #print(pd.DataFrame(today_all))

    #plot

    font_small = FontProperties(fname='/Library/Fonts/Songti.ttc',size=8)
    font_medium = FontProperties(fname='/Library/Fonts/Songti.ttc',size=10)
    font_large=FontProperties(fname='/Library/Fonts/Songti.ttc', size=12)
    font_xlarge=FontProperties(fname='/Library/Fonts/Songti.ttc', size=14)

    plt.style.use('ggplot')
    fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(11, 17))
    #fig, axes = plt.subplot(5,2,1)
    fig.suptitle('history ROE/PB',fontproperties=font_xlarge)
    #fig.autofmt_xdate()


    axes.set_title(u'history ROE/PB for ' + industry, fontproperties=font_large)
    axes.grid(color='white', which='both', linestyle='-', linewidth=0.4)
    axes.set_ylabel('industry',fontproperties=font_medium)
    for industry in today_all.industry:
        today_all_industry = today_all[today_all.industry == industry]
        axes.plot(today_all_industry['date'], today_all_industry['roe/pb'], linewidth=1,label=industry)
    axes.set_ylim([-5, 15])
    xlabels = axes.get_xticklabels()
    for xlabel in xlabels:
        xlabel.set_rotation(90)
        xlabel.set_fontproperties(font_small)
    ylabels = axes.get_yticklabels()
    for ylabel in ylabels:
        ylabel.set_fontproperties(font_small)
    #handles, labels = axes.get_legend_handles_labels()
    #axes.legend(handles, labels)

    plt.show()

    return

def historyROE(year=2010, end=2018):
    #tushare_api().format_stock_fundamentals(year=2010, end=2018)
    #tushare_api().merge_stock_fundamentals(year=2010, end=2018)
    #import pdb 
    #pdb.set_trace()


    working_folder = '/Users/yanghui/Documents/quantest/data_shared/tuShare/'
    filename = 'stock_fundamentals_all'
    stock_fundamentals_all = pd.read_excel(working_folder + filename + '.xlsx')

    stock_fundamentals_group = pd.DataFrame([])
    quarter_list = stock_fundamentals_all.quarter.drop_duplicates().tolist()
    for quarter in quarter_list:
        stock_fundamentals_qt = stock_fundamentals_all[stock_fundamentals_all.quarter == quarter]
        stock_fundamentals_qt = stock_fundamentals_qt['roe'].astype(float).groupby(stock_fundamentals_qt['industry']).mean() 
        stock_fundamentals_qt = pd.DataFrame(stock_fundamentals_qt)
        stock_fundamentals_qt.reset_index(drop=False, inplace=True)
        stock_fundamentals_qt['quarter'] = quarter
        stock_fundamentals_all.sort_values(by=['roe'], ascending=False, inplace=True)
        stock_fundamentals_group = stock_fundamentals_group.append(stock_fundamentals_qt)
        #import pdb 
        #pdb.set_trace()
    print(stock_fundamentals_group)

    #plot

    font_small = FontProperties(fname='/Library/Fonts/Songti.ttc',size=8)
    font_medium = FontProperties(fname='/Library/Fonts/Songti.ttc',size=10)
    font_large=FontProperties(fname='/Library/Fonts/Songti.ttc', size=12)
    font_xlarge=FontProperties(fname='/Library/Fonts/Songti.ttc', size=14)

    plt.style.use('ggplot')
    fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(11, 17))
    #fig, axes = plt.subplot(5,2,1)
    fig.suptitle('history ROE',fontproperties=font_xlarge)
    #fig.autofmt_xdate()


    axes.set_title(u'history ROE', fontproperties=font_large)
    axes.grid(color='white', which='both', linestyle='-', linewidth=0.4)
    axes.set_ylabel('industry',fontproperties=font_medium)
    for industry in stock_fundamentals_group.industry:
        stock_fundamentals_industry = stock_fundamentals_group[stock_fundamentals_group.industry == industry]
        axes.plot(stock_fundamentals_industry['quarter'], stock_fundamentals_industry['roe'], linewidth=1)
    #axes.set_ylim([-5, 15])
    xlabels = axes.get_xticklabels()
    for xlabel in xlabels:
        xlabel.set_rotation(90)
        xlabel.set_fontproperties(font_small)
    ylabels = axes.get_yticklabels()
    for ylabel in ylabels:
        ylabel.set_fontproperties(font_small)
    #handles, labels = axes.get_legend_handles_labels()
    #axes.legend(handles, labels)

    plt.show()

    return

def historyPE(year=2010, end=2018):
    #tushare_api().format_stock_fundamentals(year=2010, end=2018)
    #tushare_api().merge_stock_fundamentals(year=2010, end=2018)
    #import pdb 
    #pdb.set_trace()


    working_folder = '/Users/yanghui/Documents/quantest/data_shared/baoStock/'
    filename = 'history_A_stock_k_data'
    history_A_stock_k_data = pd.read_csv(working_folder + filename + '.csv')
    history_A_stock_k_data['code'] = history_A_stock_k_data['code'].map(lambda x: x[3:9])
    #print(history_A_stock_k_data)

    path = '/Users/yanghui/Documents/quantest/data_shared/tuShare/'
    filename = 'industry_classified'
    industry_classified = pd.read_excel(path + filename + '.xlsx')
    industry_classified['code'] = industry_classified['code'].map(lambda x: str(x).zfill(6))

    #print(industry_classified)

    history_A_stock_k_data = pd.merge(history_A_stock_k_data, industry_classified, how='left', on=['code'])

    #testing purpose
    history_A_stock_k_data = history_A_stock_k_data[\
                            (history_A_stock_k_data.c_name == '金融行业')]

    print(history_A_stock_k_data)

    history_group_all = pd.DataFrame([])
    date_list = history_A_stock_k_data.date.drop_duplicates().tolist()
    for date in date_list:
        history_date = history_A_stock_k_data[history_A_stock_k_data.date == date]
        history_date = history_date['peTTM'].astype(float).groupby(history_date['c_name']).mean() 
        history_group = pd.DataFrame(history_date)
        history_group.reset_index(drop=False, inplace=True)
        history_group['date'] = date
        history_group.sort_values(by=['peTTM'], ascending=False, inplace=True)
        history_group_all = history_group_all.append(history_group)
        #import pdb 
        #pdb.set_trace()
    #print(history_group_all)

    #plot

    font_small = FontProperties(fname='/Library/Fonts/Songti.ttc',size=8)
    font_medium = FontProperties(fname='/Library/Fonts/Songti.ttc',size=10)
    font_large=FontProperties(fname='/Library/Fonts/Songti.ttc', size=12)
    font_xlarge=FontProperties(fname='/Library/Fonts/Songti.ttc', size=14)

    plt.style.use('ggplot')
    fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(11, 17))
    #fig, axes = plt.subplot(5,2,1)
    fig.suptitle('history PE',fontproperties=font_xlarge)
    #fig.autofmt_xdate()


    axes.set_title(u'history PE', fontproperties=font_large)
    axes.grid(color='white', which='both', linestyle='-', linewidth=0.4)
    axes.set_ylabel('peTTM',fontproperties=font_medium)
    c_name_list = industry_classified.c_name.drop_duplicates().tolist()
    print(c_name_list)
    for industry in c_name_list:
        history_group_industry = history_group_all[history_group_all.c_name == industry]
        history_group_industry.sort_values(by='date', ascending=True, inplace=True)
        axes.plot(history_group_industry['date'], history_group_industry['peTTM'], linewidth=1)
    #axes.set_ylim([-5, 15])
    xlabels = axes.get_xticklabels()
    for xlabel in xlabels:
        xlabel.set_rotation(90)
        xlabel.set_fontproperties(font_small)
    ylabels = axes.get_yticklabels()
    for ylabel in ylabels:
        ylabel.set_fontproperties(font_small)
    #handles, labels = axes.get_legend_handles_labels()
    #axes.legend(handles, labels)

    plt.show()

    return

def historyPB(year=2010, end=2018):
    #tushare_api().format_stock_fundamentals(year=2010, end=2018)
    #tushare_api().merge_stock_fundamentals(year=2010, end=2018)
    #import pdb 
    #pdb.set_trace()


    working_folder = '/Users/yanghui/Documents/quantest/data_shared/baoStock/'
    filename = 'history_A_stock_k_data'
    history_A_stock_k_data = pd.read_csv(working_folder + filename + '.csv')
    history_A_stock_k_data['code'] = history_A_stock_k_data['code'].map(lambda x: x[3:9])
    #print(history_A_stock_k_data)

    path = '/Users/yanghui/Documents/quantest/data_shared/tuShare/'
    filename = 'industry_classified'
    industry_classified = pd.read_excel(path + filename + '.xlsx')
    industry_classified['code'] = industry_classified['code'].map(lambda x: str(x).zfill(6))

    #print(industry_classified)

    history_A_stock_k_data = pd.merge(history_A_stock_k_data, industry_classified, how='left', on=['code'])

    #testing purpose
    history_A_stock_k_data = history_A_stock_k_data[\
                            (history_A_stock_k_data.c_name == '金融行业')]

    print(history_A_stock_k_data)

    history_group_all = pd.DataFrame([])
    date_list = history_A_stock_k_data.date.drop_duplicates().tolist()
    for date in date_list:
        history_date = history_A_stock_k_data[history_A_stock_k_data.date == date]
        history_date = history_date['pbMRQ'].astype(float).groupby(history_date['c_name']).mean() 
        history_group = pd.DataFrame(history_date)
        history_group.reset_index(drop=False, inplace=True)
        history_group['date'] = date
        history_group.sort_values(by=['pbMRQ'], ascending=False, inplace=True)
        history_group_all = history_group_all.append(history_group)
        #import pdb 
        #pdb.set_trace()
    #print(history_group_all)

    #plot

    font_small = FontProperties(fname='/Library/Fonts/Songti.ttc',size=8)
    font_medium = FontProperties(fname='/Library/Fonts/Songti.ttc',size=10)
    font_large=FontProperties(fname='/Library/Fonts/Songti.ttc', size=12)
    font_xlarge=FontProperties(fname='/Library/Fonts/Songti.ttc', size=14)

    plt.style.use('ggplot')
    fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(11, 17))
    #fig, axes = plt.subplot(5,2,1)
    fig.suptitle('history pbMRQ',fontproperties=font_xlarge)
    #fig.autofmt_xdate()


    axes.set_title(u'history pbMRQ', fontproperties=font_large)
    axes.grid(color='white', which='both', linestyle='-', linewidth=0.4)
    axes.set_ylabel('pbMRQ',fontproperties=font_medium)
    c_name_list = industry_classified.c_name.drop_duplicates().tolist()
    print(c_name_list)
    for industry in c_name_list:
        history_group_industry = history_group_all[history_group_all.c_name == industry]
        history_group_industry.sort_values(by='date', ascending=True, inplace=True)
        axes.plot(history_group_industry['date'], history_group_industry['pbMRQ'], linewidth=1)
    #axes.set_ylim([-5, 15])
    xlabels = axes.get_xticklabels()
    for xlabel in xlabels:
        xlabel.set_rotation(90)
        xlabel.set_fontproperties(font_small)
    ylabels = axes.get_yticklabels()
    for ylabel in ylabels:
        ylabel.set_fontproperties(font_small)
    #handles, labels = axes.get_legend_handles_labels()
    #axes.legend(handles, labels)

    plt.show()

    return




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
    #set_ch()
    #start_date = '2012-08-10'
    #end_date = '2014-02-01'

    marketAnalysis(time_period=14)
    topStockAnalysis(count=20)
    topIndustryAnalysis(count=20)
    industryFactorAnalysis()
    historyROEPB(industry='银行')
    #historyROE()
    #historyPE()
    #historyPB()