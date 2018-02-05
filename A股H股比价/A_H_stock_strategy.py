"""
A + H 股比价策略
策略逻辑： 选出 A股价格比H股价格便宜的5个股票，买入并持有，直至A股价格比H股贵
卖出条件：
A股价格比H股贵
"""

# 可以自己import我们平台支持的第三方python模块，比如pandas、numpy等。
import os
import pandas as pd
import numpy as np


# 在这个方法中编写任何的初始化逻辑。context对象将会在你的算法策略的任何方法之间做传递。
from rqalpha.api import order_target_percent, history_bars,update_universe, logger, plot, order_value
from rqalpha.utils import is_trading


def init(context):
    logger.info('initializing the strategy...')
    context.show_progress = True
    context.buyStkCount = 5
    context.blackList = []

    load_A_H_stock_price(context)
    logger.info('initialization completed!')
    context.stocks = []
    context.holding_A = False
    context.sold_A  = False

# before_trading此函数会在每天交易开始前被调用，当天只会被调用一次
def before_trading(context):
    context.today = context.now.date()
    context.today = str(context.today)

    update_universe(context.stocks)

    calculate_if_A_stock_premium_rate(context,context.today)


    context.stocks = list(context.A_H_price_compare_result[(context.A_H_price_compare_result.A股溢价率 < -60)].A_code)

    context.stocks = context.stocks[0:context.buyStkCount]

    update_universe(context.stocks)
    update_universe(['000002.XSHE'])
    #logger.info('buyList:' + str(context.universe))


# 你选择的证券的数据更新将会触发此段逻辑，例如日或分钟历史数据切片或者是实时数据切片更新
def handle_bar(context, bar_dict):
    #count = context.buyStkCount
    #context.today = context.now.date()
    #context.today = str(context.today)
    #context.prev_calendar_date = get_prev_trade_date(context,context.today)
    #for stk in context.A_H_price_compare_result.A_code:
    #    df = context.A_H_price_compare_result[(context.A_H_price_compare_result.A_code == stk)]
    #    plot(stk, df.iloc[0,7])
    df = context.A_H_price_compare_result[(context.A_H_price_compare_result.A_code == '000002.XSHE')]
    plot('000002.XSHE', df.iloc[0,8])


        # 买入新股
    A_stk = '000002.XSHE'
    H_stk = ''
    if not context.holding_A:
        order_target_percent('000002.XSHE', 1)
        context.holding_A = True
    if bar_dict[A_stk].is_trading:
        if df.iloc[0,8] <= -10:
            order_value('000002.XSHE', 20000)
        if df.iloc[0,8] >= -5 and A_stk in context.portfolio.positions:
            order_value('000002.XSHE', -20000)
    #logger.info('portfolio.positions: ' + str(context.portfolio.positions))


def load_A_H_stock_price(context):
    # loading A_H_stock list
    filepath = '/Users/yanghui/Documents/yahoo/A股H股代码对照表.csv'
    A_H_stock_df = pd.read_csv(filepath)
    #A_H_stock_df['A_code2'] = A_H_stock_df['A_code'].map(
    #    lambda x: x[0:6] + '.SS' if x[7:11] == 'XSHG' else x[0:6] + '.SZ')
    #A_H_stock_df.drop(['A_code'], inplace=True, axis=1, errors='ignore')
    #A_H_stock_df.rename(columns={'A_code2': 'A_code'}, inplace=True)
    context.A_H_stock_df = A_H_stock_df

    # loading all H_stock price
    stock_price_all = pd.DataFrame([])
    for H_code in context.A_H_stock_df.H_code:
        filename = H_code
        filepath = '/Users/yanghui/Documents/yahoo/H_History/' + filename + '.csv'
        if os.path.exists(filepath):
            stock_price = pd.read_csv(filepath)
            #stock_price = stock_price[(stock_price.Date >= context.start_date) &
            #                                        (stock_price.Date <= context.end_date)]
            stock_price_all = stock_price_all.append(stock_price)
    context.H_stock_price_all = stock_price_all

    # loading all exchange rate
    filepath = '/Users/yanghui/Documents/yahoo/港币兑人民币历史汇率.csv'
    context.exchange_rate_df = pd.read_csv(filepath, encoding='GBK')

    return context

def calculate_if_A_stock_premium_rate(context,today):
    exchange_rate_row = context.exchange_rate_df[(context.exchange_rate_df.日期 <= today)].tail(1)
    exchange_rate = exchange_rate_row.loc[:,'收盘价(元)'].values[0]

    # inquiry H stock prices
    H_price = pd.DataFrame([])
    for H_code in context.A_H_stock_df.H_code:
        H_price_row = context.H_stock_price_all[(context.H_stock_price_all.Date <= today) &
                                                (context.H_stock_price_all.H_code == H_code)].tail(1)
        H_price = H_price.append(H_price_row)
    H_price.drop(['Open', 'High', 'Low', 'Volume', 'Adj Close'], inplace=True, axis=1, errors='ignore')
    H_price.rename(columns={'Close': 'H_price_HKD'}, inplace=True)
    H_price['H_price_RMB'] = H_price['H_price_HKD'].map(
        lambda x: x * exchange_rate)

    # inquiry A stock prices
    A_price = pd.DataFrame([])
    for A_code in context.A_H_stock_df.A_code:
        A_price_hist = history_bars(order_book_id=A_code,bar_count=1,frequency='1d',fields='close')
        A_price_row = pd.DataFrame(data={'A_code': A_code, 'A_price': A_price_hist[0]},index=np.arange(1))
        A_price = A_price.append(A_price_row)

    # join the A+H prices
    A_H_price_compare_result = pd.merge(context.A_H_stock_df,H_price,how='left',on=['H_code'])
    A_H_price_compare_result = pd.merge(A_H_price_compare_result,A_price,how='left',on=['A_code'])
    A_H_price_compare_result['A股溢价率'] = 100 * (A_H_price_compare_result['A_price'] -
                                               A_H_price_compare_result['H_price_RMB']) \
                                        / A_H_price_compare_result['H_price_RMB']
    A_H_price_compare_result = A_H_price_compare_result.sort_values(by='A股溢价率',ascending=1)

    context.A_H_price_compare_result = A_H_price_compare_result
    #logger.info(context.A_H_price_compare_result)
    return context