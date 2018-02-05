"""
新股涨停分析：
a。新股涨停个数
b。累计涨幅
"""
import os
import pandas as pd
import numpy as np
import tushare as ts
import rqalpha.api as rq
import datetime


if __name__ == '__main__':
    start_date_8 = 20170310
    start_date = '2017-03-10'
    today = datetime.datetime.today()
    df = ts.get_stock_basics()
    new_stock = df[df.timeToMarket >= start_date_8]
    #print(new_stock)
    new_stock['开盘价'] = 0
    new_stock['开板价格'] = 0
    new_stock['开板涨幅%(未开板未截止目前累计涨幅%)'] = 0
    new_stock['涨停板个数'] = 0
    new_stock['历史最高'] = 0
    new_stock['历史最高涨幅%'] = 0
    new_stock['现价'] = 0

    for stk in new_stock.index:
        print('Now calculating: ' + str(stk))
        history = ts.get_hist_data(stk, start=start_date, end=str(today)).sort_index(ascending=False)
        #print(history)
        open_price = history.tail(1).iloc[0,0]
        current_price = history.head(1).iloc[0,2]
        limit_up = history[(history.p_change <= 9.8)].tail(1)
        if len(limit_up) > 0:
            limit_up_close = limit_up.tail(1).iloc[0,2]
            percentage = 100 * (limit_up_close - open_price) / open_price
            new_stock.loc[stk, '开盘价'] = open_price
            new_stock.loc[stk, '开板价格'] = limit_up_close
            new_stock.loc[stk, '开板涨幅%(未开板未截止目前累计涨幅%)'] = percentage
            limit_up_date = limit_up.index[0]
            new_stock.loc[stk, '涨停板个数'] = len(history[(history.index < limit_up_date)])
        else:
            limit_up_close = history.head(1).iloc[0,2]
            percentage = 100 * (limit_up_close - open_price) / open_price
            new_stock.loc[stk, '开盘价'] = open_price
            new_stock.loc[stk, '开板价格'] = '未开板, 当前价格： ' + str(limit_up_close)
            new_stock.loc[stk, '开板涨幅%(未开板未截止目前累计涨幅%)'] = percentage
            new_stock.loc[stk, '涨停板个数'] = len(history)
        history_high = history.sort_values(by=['high'], ascending=False).head(1).high[0]
        percentage_high = 100 * (history_high - open_price)/open_price
        new_stock.loc[stk, '历史最高'] = history_high
        new_stock.loc[stk, '历史最高涨幅%'] = percentage_high
        new_stock.loc[stk, '现价'] = current_price

    #print(new_stock)
    new_stock.to_csv('/Users/yanghui/Desktop/new_stock_v1.1.1.csv',encoding='GBK')

