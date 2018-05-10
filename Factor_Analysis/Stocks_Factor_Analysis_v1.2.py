#encoding: UTF-8
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
from matplotlib_ch import set_ch

def industryFactorAnalysis():
    working_folder = '/Users/huiyang/Documents/SPSS modeler/复盘/'
    filename = 'today_all_roe_pb_rsi'
    today_all_roe_pb_rsi = pd.read_excel(working_folder + filename + '.xlsx')

    industry = topIndustry(count=20, time_period=5).index[0]

    today_all_roe_pb_rsi = today_all_roe_pb_rsi[today_all_roe_pb_rsi.industry == industry]
    #today_all_roe_pb_rsi['code'] = today_all_roe_pb_rsi['code'].map(lambda x: str(x).zfill(6))

    plt.style.use('ggplot')
    fig, axes = plt.subplots(nrows=2, ncols=4, figsize=(50, 10))
    fig.suptitle(industry + '行业因子分析')

    axes[0, 0].set_title(u'市值分布')
    axes[0, 0].grid(color='white', which='both', linestyle='-', linewidth=0.4)
    axes[0, 0].set_ylabel('mktcap')
    axes[0, 0].plot(today_all_roe_pb_rsi['rsi_14days'], today_all_roe_pb_rsi['mktcap'], 'o')
    axes[0, 0].set_xlim([0, 100])

    axes[0, 1].set_title(u'价格分布')
    axes[0, 1].grid(color='white', which='both', linestyle='-', linewidth=0.4)
    axes[0, 1].set_ylabel('open')
    axes[0, 1].plot(today_all_roe_pb_rsi['rsi_14days'], today_all_roe_pb_rsi['open'], 'o')
    axes[0, 1].set_xlim([0, 100])

    axes[0, 2].set_title(u'roe/pb 分布')
    axes[0, 2].set_ylabel('roe/pb')
    axes[0, 2].grid(color='white', which='both', linestyle='-', linewidth=0.4)
    axes[0, 2].plot(today_all_roe_pb_rsi['rsi_14days'], today_all_roe_pb_rsi['roe/pb'], 'o')
    axes[0, 2].set_xlim([0, 100])

    axes[0, 3].set_title(u'profit 分布')
    axes[0, 3].set_ylabel('profit')
    axes[0, 3].grid(color='white', which='both', linestyle='-', linewidth=0.4)
    axes[0, 3].plot(today_all_roe_pb_rsi['rsi_14days'], today_all_roe_pb_rsi['profit'], 'o')
    axes[0, 3].set_xlim([0, 100])

    axes[1, 0].set_title(u'PE分布')
    axes[1, 0].set_ylabel('pe')
    axes[1, 0].grid(color='white', which='both', linestyle='-', linewidth=0.4)
    axes[1, 0].plot(today_all_roe_pb_rsi['rsi_14days'], today_all_roe_pb_rsi['pe'], 'o')
    axes[1, 0].set_xlim([0, 100])

    axes[1, 1].set_title(u'PB分布')
    axes[1, 1].set_ylabel('pb')
    axes[1, 1].grid(color='white', which='both', linestyle='-', linewidth=0.4)
    axes[1, 1].plot(today_all_roe_pb_rsi['rsi_14days'], today_all_roe_pb_rsi['pb'], 'o')
    axes[1, 1].set_xlim([0, 100])

    axes[1, 2].set_title(u'ROE分布')
    axes[1, 2].set_ylabel('roe_mean')
    axes[1, 2].grid(color='white', which='both', linestyle='-', linewidth=0.4)
    axes[1, 2].plot(today_all_roe_pb_rsi['rsi_14days'], today_all_roe_pb_rsi['roe_mean'], 'o')
    axes[1, 2].set_xlim([0, 100])

    axes[1, 3].set_title(u'地区分布')
    axes[1, 3].set_ylabel('area')
    axes[1, 3].grid(color='white', which='both', linestyle='-', linewidth=0.4)
    axes[1, 3].plot(today_all_roe_pb_rsi['rsi_14days'], today_all_roe_pb_rsi['area'], 'o')
    axes[1, 3].set_xlim([0, 100])

    #axes[1, 3].set_title('PC分布')
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
    plt.style.use('ggplot')
    fig, axes = plt.subplots(nrows=2, ncols=4, figsize=(50, 10))
    fig.suptitle('市场分析')
    #fig.autofmt_xdate()


    try:
        index_000001 = hindenburgOmen(index='000001').tail(20)
        axes[0, 0].set_title(u'兴登堡凶兆（上证指数）')
        axes[0, 0].grid(color='white', which='both', linestyle='-', linewidth=0.4)
        axes[0, 0].set_ylabel('R_square')
        axes[0, 0].plot(index_000001['date'], index_000001['hindenburg_omen_000001'], 'blue', linewidth=1)
        axes[0, 0].plot(index_000001['date'], index_000001['close_adjust'], 'red', linewidth=1)
        axes[0, 0].set_ylim([0, 1])
        labels = axes[0, 0].get_xticklabels()
        for label in labels:
            label.set_rotation(45)
    except:
        pass
    

    try:
        index_399001 = hindenburgOmen(index='399001').tail(20)

        axes[0, 1].set_title(u'兴登堡凶兆（深证成指）')
        axes[0, 1].grid(color='white', which='both', linestyle='-', linewidth=0.4)
        axes[0, 1].set_ylabel('R_square')
        axes[0, 1].plot(index_399001['date'], index_399001['hindenburg_omen_399001'], 'blue', linewidth=1)
        axes[0, 1].plot(index_399001['date'], index_399001['close_adjust'], 'red', linewidth=1)
        axes[0, 1].set_ylim([0, 1])
        labels = axes[0, 1].get_xticklabels()
        for label in labels:
            label.set_rotation(45)
    except:
        pass

    try:
        index_399006 = hindenburgOmen(index='399006').tail(20)

        axes[0, 2].set_title(u'兴登堡凶兆（创业板指）')
        axes[0, 2].grid(color='white', which='both', linestyle='-', linewidth=0.4)
        axes[0, 2].set_ylabel('R_square')
        axes[0, 2].plot(index_399006['date'], index_399006['hindenburg_omen_399006'], 'blue', linewidth=1)
        axes[0, 2].plot(index_399006['date'], index_399006['close_adjust'], 'red', linewidth=1)
        axes[0, 2].set_ylim([0, 1])
        labels = axes[0, 2].get_xticklabels()
        for label in labels:
            label.set_rotation(45)
    except:
        pass

    try:
        money_supply = moneySupply().tail(20)
        axes[0, 3].set_title(u'成交量占比')
        axes[0, 3].grid(color='white', which='both', linestyle='-', linewidth=0.4)
        axes[0, 3].set_ylabel('成交量占M0/M1百分比')
        axes[0, 3].plot(money_supply['date'], money_supply['M0_percent'], 'blue', linewidth=1)
        axes[0, 3].plot(money_supply['date'], money_supply['M1_percent'], 'red', linewidth=1)
        axes[0, 3].set_ylim([0, 20])
        labels = axes[0, 3].get_xticklabels()
        for label in labels:
            label.set_rotation(45)
    except:
        pass


    try: 
        top_industry = topIndustry(count=20, time_period=14)
        top_industry['rsi_count'] = top_industry['rsi_count'].map(lambda x: str(x))
        axes[1, 0].set_title(u'最近14日热门行业')
        axes[1, 0].grid(color='white', which='both', linestyle='-', linewidth=0.4)
        axes[1, 0].barh(top_industry.index + '(' + top_industry['rsi_count'] + ')', top_industry['rsi_mean'], color='red')
        axes[1, 0].set_xlim([0, 100])
    except:
        pass

    try: 
        top_industry = topIndustry(count=20, time_period=10)
        top_industry['rsi_count'] = top_industry['rsi_count'].map(lambda x: str(x))
        axes[1, 1].set_title(u'最近10日热门行业')
        axes[1, 1].grid(color='white', which='both', linestyle='-', linewidth=0.4)
        axes[1, 1].barh(top_industry.index + '(' + top_industry['rsi_count'] + ')', top_industry['rsi_mean'], color='red')
        axes[1, 1].set_xlim([0, 100])
    except:
        pass
    
    try: 
        top_industry = topIndustry(count=20, time_period=5)
        top_industry['rsi_count'] = top_industry['rsi_count'].map(lambda x: str(x))
        axes[1, 2].set_title(u'最近5日热门行业')
        axes[1, 2].grid(color='white', which='both', linestyle='-', linewidth=0.4)
        axes[1, 2].barh(top_industry.index + '(' + top_industry['rsi_count'] + ')', top_industry['rsi_mean'], color='red')
        axes[1, 2].set_xlim([0, 100])
    except:
        pass

    try:
        top_stock = topStock(count=20, time_period=5, top_industry=True)
        industry = top_stock.iloc[0, 36]
        axes[1, 3].set_title('5日行业热门股票(' + industry +')')
        axes[1, 3].grid(color='white', which='both', linestyle='-', linewidth=0.4)
        axes[1, 3].barh(top_stock['name'], top_stock['rsi_5days'], color='red')
        axes[1, 3].set_xlim([0, 100])
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
    plt.style.use('ggplot')
    fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(50, 10))
    fig.suptitle('股票分析')
    #fig.autofmt_xdate()

    try:
        top_stock = topStock(count=count, time_period=14, top_industry=False)
        axes[0, 0].set_title(u'趋势跟踪 - 14日热门股票')
        axes[0, 0].grid(color='white', which='both', linestyle='-', linewidth=0.4)
        axes[0, 0].barh(top_stock['name'] + '(' + top_stock['industry'] + ')', top_stock['rsi_14days'], color='red')
        axes[0, 0].set_xlim([0, 100])
    except:
        pass

    try:
        top_stock = topStock(count=count, time_period=10, top_industry=False)
        axes[0, 1].set_title(u'趋势跟踪 - 10日热门股票')
        axes[0, 1].grid(color='white', which='both', linestyle='-', linewidth=0.4)
        axes[0, 1].barh(top_stock['name'] + '(' + top_stock['industry'] + ')', top_stock['rsi_10days'], color='red')
        axes[0, 1].set_xlim([0, 100])
    except:
        pass

    try:
        top_stock = topStock(count=count, time_period=5, top_industry=False)
        axes[0, 2].set_title(u'趋势跟踪 - 5日热门股票')
        axes[0, 2].grid(color='white', which='both', linestyle='-', linewidth=0.4)
        axes[0, 2].barh(top_stock['name'] + '(' + top_stock['industry'] + ')', top_stock['rsi_5days'], color='red')
        axes[0, 2].set_xlim([0, 100])
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
        axes[1, 0].set_title(u'趋势跟踪 - 2日涨幅股票')
        axes[1, 0].grid(color='white', which='both', linestyle='-', linewidth=0.4)
        axes[1, 0].barh(top_stock['name'] + '(' + top_stock['industry'] + ')', top_stock['2days_percentage'], color='red')
        #axes[1, 0].set_xlim([0, 100])
    except:
        pass

    try:
        top_stock = topPercentStock(count=count, time_period=5, top_industry=False)
        axes[1, 1].set_title(u'趋势跟踪 - 5日涨幅股票')
        axes[1, 1].grid(color='white', which='both', linestyle='-', linewidth=0.4)
        axes[1, 1].barh(top_stock['name'] + '(' + top_stock['industry'] + ')', top_stock['5days_percentage'], color='red')
        #axes[1, 0].set_xlim([0, 100])
    except:
        pass

    try:
        top_stock = topPercentStock(count=count, time_period=10, top_industry=False)
        axes[1, 2].set_title(u'趋势跟踪 - 10日涨幅股票')
        axes[1, 2].grid(color='white', which='both', linestyle='-', linewidth=0.4)
        axes[1, 2].barh(top_stock['name'] + '(' + top_stock['industry'] + ')', top_stock['10days_percentage'], color='red')
        #axes[1, 0].set_xlim([0, 100])
    except:
        pass


    plt.show()
    return

def hindenburgOmen(index='000001'):
    path = '/Users/huiyang/Documents/quantest/复盘/notification_monitoring_files/'
    filename = 'hindenburg_omen'
    hindenburg_omen = pd.read_excel(path + filename + '.xlsx')
    working_folder = '/Users/huiyang/Documents/'


    # read index
    if index == '000001':
        filename = 'index_000001'
        index_000001 = pd.read_excel(io=working_folder + \
             'SPSS modeler/复盘/' + filename + '.xlsx')
        index_000001['date'] = index_000001['date'].map(lambda x: x.isoformat()[:10])
        index_000001 = pd.merge(index_000001, hindenburg_omen, how='left', left_on='date', right_on='date', suffixes=('_x', '_y'))
        index_000001['close_adjust'] = index_000001['close'].map(lambda x: x/10000)
        index_000001.sort_values(by='date', ascending=True, inplace=True)
        index_df = index_000001

    if index == '399001':
        filename = 'index_399001'
        index_399001 = pd.read_excel(io=working_folder + \
            'SPSS modeler/复盘/' + filename + '.xlsx')
        index_399001['date'] = index_399001['date'].map(lambda x: x.isoformat()[:10])
        index_399001 = pd.merge(index_399001, hindenburg_omen, how='left', left_on='date', right_on='date', suffixes=('_x', '_y'))
        index_399001['close_adjust'] = index_399001['close'].map(lambda x: x/20000)
        index_399001.sort_values(by='date', ascending=True, inplace=True)
        index_df = index_399001

    if index == '399006':
        filename = 'index_399006'
        index_399006 = pd.read_excel(io=working_folder + \
             'SPSS modeler/复盘/' + filename + '.xlsx')
        index_399006['date'] = index_399006['date'].map(lambda x: x.isoformat()[:10])
        index_399006 = pd.merge(index_399006, hindenburg_omen, how='left', left_on='date', right_on='date', suffixes=('_x', '_y'))
        index_399006['close_adjust'] = index_399006['close'].map(lambda x: x/10000)
        index_399006.sort_values(by='date', ascending=True, inplace=True)
        index_df = index_399006

    return index_df


def moneySupply():
    path = '/Users/huiyang/Documents/quantest/复盘/notification_monitoring_files/'
    working_folder = '/Users/huiyang/Documents/'

    # read index
    filename = 'index_000001'
    index_000001 = pd.read_excel(io=working_folder + \
         'SPSS modeler/复盘/' + filename + '.xlsx')
    index_000001['date'] = index_000001['date'].map(lambda x: x.isoformat()[:10])

    filename = 'index_399001'
    index_399001 = pd.read_excel(io=working_folder + \
         'SPSS modeler/复盘/' + filename + '.xlsx')
    index_399001['date'] = index_399001['date'].map(lambda x: x.isoformat()[:10])

    filename = 'index_399006'
    index_399006 = pd.read_excel(io=working_folder + \
         'SPSS modeler/复盘/' + filename + '.xlsx')
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
    working_folder = '/Users/huiyang/Documents/'
    filename = 'today_all_roe_pb_rsi'
    today_all_roe_pb_rsi = pd.read_excel(io=working_folder + \
         'SPSS modeler/复盘/' + filename + '.xlsx')

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
    working_folder = '/Users/huiyang/Documents/'
    filename = 'today_all_roe_pb_rsi'
    today_all_roe_pb_rsi = pd.read_excel(io=working_folder + \
         'SPSS modeler/复盘/' + filename + '.xlsx')

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
    working_folder = '/Users/huiyang/Documents/'
    filename = 'today_all_roe_pb_rsi'
    today_all_roe_pb_rsi = pd.read_excel(io=working_folder + \
         'SPSS modeler/复盘/' + filename + '.xlsx')

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
    today_all_roe_pb_rsi['timeToMarket'] = today_all_roe_pb_rsi['timeToMarket'].map(lambda x: str(x)[:4] + '-' + str(x)[4:2] + '-' + str(x)[6:2])
    today_all_roe_pb_rsi = today_all_roe_pb_rsi[today_all_roe_pb_rsi.timeToMarket < market_date]

    today_all_roe_pb_rsi = today_all_roe_pb_rsi.head(count)
    return today_all_roe_pb_rsi



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
    
    topStockAnalysis(count=20)
    marketAnalysis(time_period=14)
    industryFactorAnalysis()
    