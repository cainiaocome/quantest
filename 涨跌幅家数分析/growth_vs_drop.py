import pandas as pd
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from matplotlib.dates import AutoDateLocator, DateFormatter
import matplotlib.dates as dt
import datetime
import os
from sqlalchemy import create_engine

# 股票涨跌家数分析

if __name__ == '__main__':
    start_date = '2015-01-01'
    end_date = '2016-01-01'



    index = pd.read_csv('/Users/yanghui/Documents/tushare/StockDaily/Index.csv',encoding='GBK')
    money_supply = pd.read_csv('/Users/yanghui/Documents/sina/货币供应量(1978.1-2016.10)_宏观数据_新浪财经.csv',encoding='GBK')
    index['month'] = index.apply(lambda x: x['date'][:7], axis=1)

    x = list(index.date)
    y = list(index.open)

    index_sh = index[(index.code != 399001)]
    index_sh['date_num'] = index_sh['date'].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d'))
    index_sh = index_sh.sort_values(by='date_num')



    index_sz = index[(index.code == 399001)]
    index_sz['date_num'] = index_sz['date'].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d'))
    index_sz = index_sz.sort_values(by='date_num')
    index_sz['amount_sz'] = index_sz['amount']
    index_sz['close_sz'] = index_sz['close']

    index_merge = index_sh.merge(index_sz[['amount_sz','close_sz','date']], on='date')
    index_merge = index_merge[(index_merge.date >= start_date) &
                                            (index_merge.date <= end_date)]



    """
    loading all stocks and save to the memory
    """

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
    print(stock_list)

    for order_book_id in stock_list:
        print('Now loading: ', order_book_id)
        if order_book_id[7:11] == 'XSHG':
            filename = 'sh' + order_book_id[0:6]
        else:
            filename = 'sz' + order_book_id[0:6]
        filepath = '/Users/yanghui/Documents/trading-data@full/stock data/' + filename + '.csv'
        if os.path.exists(filepath):
            stock_fundamentals = pd.read_csv(filepath)
            stock_fundamentals = stock_fundamentals[(stock_fundamentals.date >= start_date) &
                                                (stock_fundamentals.date <= end_date)]
            stock_fundamentals_all = stock_fundamentals_all.append(stock_fundamentals)

    stock_fundamentals_all['code_6'] = stock_fundamentals_all['code'].map(
                    lambda x: x[2:8])

    index_merge['grow_count_percentage_sh'] = 0
    index_merge['grow_count_percentage_sz'] = 0
    index_merge_all = pd.DataFrame([])
    for date in index_merge['date']:
        stock_fundamentals_current_date = stock_fundamentals_all[(stock_fundamentals_all.date == date) &
                                                                 (stock_fundamentals_all.code_6 >= '600000')]
        print('Now calculating: ', date)
        total_count = len(stock_fundamentals_current_date)
        grow_count = len(stock_fundamentals_current_date[(stock_fundamentals_current_date.change >= 0)])
        percentage = 100 * grow_count / total_count
        percentage = percentage * 10 # 调整显示
        index_row = index_merge[index_merge.date == date]
        index_row.loc[:,('grow_count_percentage_sh')] = percentage
        stock_fundamentals_current_date = stock_fundamentals_all[(stock_fundamentals_all.date == date) &
                                                                 (stock_fundamentals_all.code_6 < '300000')]

        total_count = len(stock_fundamentals_current_date)
        grow_count = len(stock_fundamentals_current_date[(stock_fundamentals_current_date.change >= 0)])
        percentage = 100 * grow_count / total_count
        percentage = percentage * 10 # 调整显示
        index_row.loc[:,('grow_count_percentage_sz')] = percentage
        index_merge_all = index_merge_all.append(index_row)

    plt.style.use('ggplot')
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(18, 6))
    axes[0].set_title('shanghai index')
    axes[0].grid(color='gray', which='both', linestyle='-', linewidth=1)
    axes[0].plot(index_merge_all['date_num'], index_merge_all['close'], 'r', linewidth=1,)
    axes[0].plot(index_merge_all['date_num'], index_merge_all['grow_count_percentage_sh'], 'yellow', linewidth=1,)

    axes[1].set_title('shenzhen index')
    axes[1].grid(color='gray', which='both', linestyle='-', linewidth=1)
    axes[1].plot(index_merge_all['date_num'], index_merge_all['close_sz'], 'g', linewidth=1,)
    axes[1].plot(index_merge_all['date_num'], index_merge_all['grow_count_percentage_sz'], 'yellow', linewidth=1,)

    plt.show()

    #plt.plot(index_merge_money['date_num'], index_merge_money['M0_percent_amp'], 'b', linewidth=1,)
    #plt.plot(index_merge_money['date_num'], index_merge_money['M2_percent_amp'], 'brown', linewidth=1,)
    #plt.hist(index_merge_money['M0_percent'],50,normed=1)




