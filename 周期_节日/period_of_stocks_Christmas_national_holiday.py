import pandas as pd
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from matplotlib.dates import AutoDateLocator, DateFormatter
import matplotlib.dates as dt
import datetime
import os
from sqlalchemy import create_engine

#计算一下节日涨幅
#圣诞节-元旦结束
#国庆节


if __name__ == '__main__':


    year_start = 2005
    year_end = 2016
    period_1_start = '12-18'
    period_1_end = '01-12'
    period_2_start = '09-22'
    period_2_end = '10-15'

    start_date = str(year_start - 1) + '-' + period_1_start
    end_date = str(year_end) + '-' + period_2_end

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
    stock_list.sort()
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
            stock_fundamentals_all['order_book_id'] = stock_fundamentals_all['code'].map(
                    lambda x: x[2:8] + '.XSHG' if x[0:2] == 'sh' else x[2:8] + '.XSHE')

    result_df = pd.DataFrame([])
    result_df_row = pd.DataFrame(
        columns=['code', 'year', 'period_1', 'period_2', 'period_3', 'period_4', 'period_5', 'period_6', 'period_7',
                 'period_8', 'period_9', 'period_10', 'period_11', 'period_12', ])

    # calculating the percent of the price for each period.
    total_count = len(stock_list)
    count = 1
    for order_book_id in stock_list:
        year = year_start
        result_df_row.loc[0,'code'] = order_book_id
        result_df_row.loc[0,'year'] = year
        result_df_row.loc[0,'period_1'] = 'null'
        result_df_row.loc[0,'period_2'] = 'null'
        result_df_row.loc[0,'period_3'] = 'null'
        result_df_row.loc[0,'period_4'] = 'null'
        result_df_row.loc[0,'period_5'] = 'null'
        result_df_row.loc[0,'period_6'] = 'null'
        result_df_row.loc[0,'period_7'] = 'null'
        result_df_row.loc[0,'period_8'] = 'null'
        result_df_row.loc[0,'period_9'] = 'null'
        result_df_row.loc[0,'period_10'] = 'null'
        result_df_row.loc[0,'period_11'] = 'null'
        result_df_row.loc[0,'period_12'] = 'null'
        progress = 100 * count / total_count
        while year_start <= year <= year_end:
            print('Now calculating: ', order_book_id, ' - ', year, ' progress:', '%.2f%%' % progress)
            result_df_row.loc[0, 'year'] = year
            #period_1
            period_start = str(year - 1) + '-' + period_1_start
            period_end = str(year) + '-' + period_1_end
            stock_fundamentals = stock_fundamentals_all[(stock_fundamentals_all.date >= period_start) &
                                                        (stock_fundamentals_all.date <= period_end) &
                                                        (stock_fundamentals_all.order_book_id == order_book_id)]
            if len(stock_fundamentals) > 0:
                stock_fundamentals = stock_fundamentals.sort_values(by='date')
                price_start = stock_fundamentals.head(1).iloc[0]['open']
                price_end = stock_fundamentals.tail(1).iloc[0]['open']
                percent = 100 * (price_end - price_start)/price_start
                result_df_row.loc[0,'period_1'] = percent
            else:
                result_df_row.loc[0,'period_1'] = 'null'


            #period_2
            period_start = str(year) + '-' + period_2_start
            period_end = str(year) + '-' + period_2_end
            stock_fundamentals = stock_fundamentals_all[(stock_fundamentals_all.date >= period_start) &
                                                         (stock_fundamentals_all.date <= period_end) &
                                                          (stock_fundamentals_all.order_book_id == order_book_id)]
            if len(stock_fundamentals) > 0:
                stock_fundamentals = stock_fundamentals.sort_values(by='date')
                price_start = stock_fundamentals.head(1).iloc[0]['open']
                price_end = stock_fundamentals.tail(1).iloc[0]['open']
                percent = 100 * (price_end - price_start)/price_start
                result_df_row.loc[0,'period_2'] = percent
            else:
                result_df_row.loc[0,'period_2'] = 'null'

            #year increase
            year = year + 1
            result_df = result_df.append(result_df_row)

        count = count + 1

    result_df = result_df.sort_values(by=['code','year'])
    print(result_df)
    result_df.to_csv('/Users/yanghui/Desktop/Christmas_national_holiday_2005-2016.csv')