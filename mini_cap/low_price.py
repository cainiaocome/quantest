import pandas as pd
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from matplotlib.dates import AutoDateLocator, DateFormatter
import matplotlib.dates as dt
import datetime
import os
from sqlalchemy import create_engine

# 低价股策略

if __name__ == '__main__':

    start_date = '2005-01-01'
    end_date = '2016-05-01'
    low_price = 5

    index = pd.read_csv('/Users/yanghui/Documents/tushare_download/StockDaily/Index.csv',encoding='GBK')
    index = index[(index.date >= start_date) &
                (index.date <= end_date)]

    #index['date'] = index.apply(lambda x: x['date'][:7], axis=1)
    #x = list(index.date)
    #y = list(index.open)
    index['date_num'] = index['date'].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d'))
    index = index.sort_values(by='date_num')
    index_sh = index[(index.code != 399001)]
    #index_sh['date_num'] = index_sh['date'].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d'))
    index_sh = index_sh.sort_values(by='date_num')
    index_sz = index[(index.code == 399001)]
    #index_sz['date_num'] = index_sz['date'].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d'))
    index_sz = index_sz.sort_values(by='date_num')
    print(index)



    # loading stock list
    engine_stock_fundamentals = create_engine("mysql+mysqldb://root:good@localhost:3306/TUSHARE_STOCK_FUNDAMENTALS",
                                                  encoding='utf-8', echo=False)
    connection = engine_stock_fundamentals.connect()
    sql = "select * from TUSHARE_STOCK_FUNDAMENTALS.StockBasics"

    stock_all = pd.read_sql(sql, engine_stock_fundamentals)
    connection.close()
    stock_all['order_book_id'] = stock_all['code'].map(
            lambda x: x + '.XSHG' if x >= '600000' else x + '.XSHE')


    # checking all stocks daily price
    stock_fundamentals_all = pd.DataFrame([])
    stock_list = list(set(stock_all.order_book_id))
    print(stock_list)
    for order_book_id in stock_list:
        print('Now loading : ', order_book_id)
        if order_book_id[7:] == 'XSHG':
            filename = 'sh' + order_book_id[0:6]
        else:
            filename = 'sz' + order_book_id[0:6]
        filepath = '/Users/yanghui/Documents/trading-data@full/stock data/' + filename + '.csv'
        if os.path.exists(filepath):
            stock_fundamentals = pd.read_csv(filepath)
            stock_fundamentals = stock_fundamentals[(stock_fundamentals.date >= start_date) &
                                                    (stock_fundamentals.date <= end_date)]
            #stock_fundamentals = stock_fundamentals.sort_values(by='date')
            stock_fundamentals_all = stock_fundamentals_all.append(stock_fundamentals)

    for date in index.date:
        low_price_counter = 0
        stock_fundamentals = stock_fundamentals_all[(stock_fundamentals_all.date <= date)]
        stock_fundamentals = stock_fundamentals.sort_values(by='date',ascending=False)
        stock_fundamentals = stock_fundamentals.groupby('code').first()  # take only the first row for each group, make sure all other rows with this key have the same values
        total = len(stock_fundamentals)

        stock_fundamentals = stock_fundamentals[(stock_fundamentals.close <= low_price)]
        low_price_counter = len(stock_fundamentals)


        percentage = 100000 * low_price_counter/total
        index.loc[index['date'] == date, 'low_price_percentage'] = percentage
        print('date: ', date, ',', low_price_counter, '/', total, '=', percentage)
    #fundamentals_all = stock_funda mentals_all.sort_values(by='percentage',ascending=False)
    #fundamentals_all = fundamentals_all[(fundamentals_all.market_value <= 5.000000e+09) &
    #                                   (fundamentals_all.open <= 7) &
    #                                   (fundamentals_all.traded_market_value <= 2.5e+09)]
    print(index)


    plt.grid(color='gray', which='both', linestyle='-', linewidth=1)
    plt.plot(index_sh['date_num'], index_sh['close'], 'r', linewidth=1,)
    plt.plot(index_sz['date_num'], index_sz['close'], 'g', linewidth=1,)
    plt.plot(index['date_num'], index['low_price_percentage'], 'b', linewidth=1,)

    plt.show()

