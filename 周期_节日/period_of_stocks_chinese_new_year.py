import pandas as pd
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from matplotlib.dates import AutoDateLocator, DateFormatter
import matplotlib.dates as dt
import datetime
import os
from sqlalchemy import create_engine
#计算历年春节前，春节后涨幅

if __name__ == '__main__':


    year_start = 2005
    year_end = 2016


    #2016
    period_1_start_2016 = '2016-02-01'
    period_1_end_2016 = '2016-02-19'
    #period_2_start_2016 = '2016-09-30'
    #period_2_end_2016 = '2016-10-8'

    #2015
    period_1_start_2015 = '2015-02-12'
    period_1_end_2015 = '2015-03-02'
    #period_2_start_2015 = '2015-09-30'
    #period_2_end_2015 = '2015-10-8'

    #2014
    period_1_start_2014 = '2014-01-24'
    period_1_end_2014 = '2014-02-11'

    # 2013
    period_1_start_2013 = '2013-02-03'
    period_1_end_2013 = '2013-02-21'

    # 2012
    period_1_start_2012 = '2012-01-16'
    period_1_end_2012 = '2012-03-06'

    # 2011
    period_1_start_2011 = '2011-01-27'
    period_1_end_2011 = '2011-02-15'

    # 2010
    period_1_start_2010 = '2010-02-07'
    period_1_end_2010 = '2010-02-25'

    # 2009
    period_1_start_2009 = '2009-01-19'
    period_1_end_2009 = '2009-02-07'

    # 2008
    period_1_start_2008 = '2008-01-31'
    period_1_end_2008 = '2008-02-18'

    # 2007
    period_1_start_2007 = '2007-02-11'
    period_1_end_2007 = '2007-03-01'
    # 2006
    period_1_start_2006 = '2006-01-22'
    period_1_end_2006 = '2006-02-09'
    # 2005
    period_1_start_2005 = '2005-02-02'
    period_1_end_2005 = '2005-02-20'


    start_date = period_1_start_2005
    end_date = period_1_end_2016

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
            if year == 2005:
                period_start = period_1_start_2005
                period_end = period_1_end_2005
            if year == 2006:
                period_start = period_1_start_2006
                period_end = period_1_end_2006
            if year == 2007:
                period_start = period_1_start_2007
                period_end = period_1_end_2007
            if year == 2008:
                period_start = period_1_start_2008
                period_end = period_1_end_2008
            if year == 2009:
                period_start = period_1_start_2009
                period_end = period_1_end_2009
            if year == 2010:
                period_start = period_1_start_2010
                period_end = period_1_end_2010
            if year == 2011:
                period_start = period_1_start_2011
                period_end = period_1_end_2011
            if year == 2012:
                period_start = period_1_start_2012
                period_end = period_1_end_2012
            if year == 2013:
                period_start = period_1_start_2013
                period_end = period_1_end_2013
            if year == 2014:
                period_start = period_1_start_2014
                period_end = period_1_end_2014
            if year == 2015:
                period_start = period_1_start_2015
                period_end = period_1_end_2015
            if year == 2016:
                period_start = period_1_start_2016
                period_end = period_1_end_2016

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

            #year increase
            year = year + 1
            result_df = result_df.append(result_df_row)

        count = count + 1

    result_df = result_df.sort_values(by=['code','year'])
    print(result_df)
    result_df.to_csv('/Users/yanghui/Desktop/holiday2005_2016D18.csv')


