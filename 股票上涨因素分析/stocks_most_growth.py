import pandas as pd
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from matplotlib.dates import AutoDateLocator, DateFormatter
import matplotlib.dates as dt
import datetime
import os
from sqlalchemy import create_engine

# 股票上涨因素分析

if __name__ == '__main__':

    start_date = '2012-08-10'
    end_date = '2014-02-01'


    # loading stock list
    engine_stock_fundamentals = create_engine("mysql+mysqldb://root:good@localhost:3306/TUSHARE_STOCK_FUNDAMENTALS",
                                                  encoding='utf-8', echo=False)
    connection = engine_stock_fundamentals.connect()
    sql = "select * from TUSHARE_STOCK_FUNDAMENTALS.StockBasics"

    stock_all = pd.read_sql(sql, engine_stock_fundamentals)
    connection.close()
    stock_all['order_book_id'] = stock_all['code'].map(
            lambda x: x + '.XSHG' if x >= '600000' else x + '.XSHE')


    # loading all stocks daily price
    stock_fundamentals_all = pd.DataFrame([])
    stock_list = list(set(stock_all.order_book_id))
    for order_book_id in stock_list:
        if order_book_id[7:4] == 'XSHG':
            filename = 'sh' + order_book_id[0:6]
        else:
            filename = 'sz' + order_book_id[0:6]
        filepath = '/Users/yanghui/Documents/trading-data@full/stock data/' + filename + '.csv'
        if os.path.exists(filepath):
            stock_fundamentals = pd.read_csv(filepath)
            market_dates = len(stock_fundamentals[(stock_fundamentals.date <= start_date)])
            if market_dates >= 30:
                stock_fundamentals = stock_fundamentals[(stock_fundamentals.date >= start_date) &
                                                (stock_fundamentals.date <= end_date)]
                stock_fundamentals = stock_fundamentals.sort_values(by='date')
                stock_fundamentals_final = stock_fundamentals.head(1)
                end_date_open = stock_fundamentals.tail(1)['open'].values
                start_date_open = stock_fundamentals.head(1)['open'].values
                stock_fundamentals_final['percentage'] = 100 * (end_date_open - start_date_open)/start_date_open
                stock_fundamentals_all = stock_fundamentals_all.append(stock_fundamentals_final)
                stock_fundamentals_all['order_book_id'] = stock_fundamentals_all['code'].map(
                    lambda x: x[2:8] + '.XSHG' if x[0:2] == 'sh' else x[2:8] + '.XSHE')
    fundamentals_all = stock_fundamentals_all.sort_values(by='percentage',ascending=False)
    fundamentals_all = fundamentals_all[(fundamentals_all.market_value <= 5.000000e+09) &
                                        (fundamentals_all.open <= 7) &
                                        (fundamentals_all.traded_market_value <= 2.5e+09)]
    print(fundamentals_all)



    fig, axes = plt.subplots(nrows=2, ncols=4, figsize=(36, 12))

    axes[0, 0].set_title('市值分布')
    axes[0, 0].grid(color='gray', which='both', linestyle='-', linewidth=1)
    axes[0, 0].plot(fundamentals_all['percentage'], fundamentals_all['market_value'], 'o')

    axes[0, 1].set_title('价格分布')
    axes[0, 1].grid(color='gray', which='both', linestyle='-', linewidth=1)
    axes[0, 1].plot(fundamentals_all['percentage'], fundamentals_all['open'], 'o')

    axes[0, 2].set_title('流通市值分布')
    axes[0, 2].grid(color='gray', which='both', linestyle='-', linewidth=1)
    axes[0, 2].plot(fundamentals_all['percentage'], fundamentals_all['traded_market_value'], 'o')

    axes[1, 0].set_title('PE分布')
    axes[1, 0].grid(color='gray', which='both', linestyle='-', linewidth=1)
    axes[1, 0].plot(fundamentals_all['percentage'], fundamentals_all['PE_TTM'], 'o')

    axes[1, 1].set_title('PB分布')
    axes[1, 1].grid(color='gray', which='both', linestyle='-', linewidth=1)
    axes[1, 1].plot(fundamentals_all['percentage'], fundamentals_all['PB'], 'o')

    axes[1, 2].set_title('PS分布')
    axes[1, 2].grid(color='gray', which='both', linestyle='-', linewidth=1)
    axes[1, 2].plot(fundamentals_all['percentage'], fundamentals_all['PS_TTM'], 'o')

    axes[1, 3].set_title('PC分布')
    axes[1, 3].grid(color='gray', which='both', linestyle='-', linewidth=1)
    axes[1, 3].plot(fundamentals_all['percentage'], fundamentals_all['PC_TTM'], 'o')


    plt.show()

