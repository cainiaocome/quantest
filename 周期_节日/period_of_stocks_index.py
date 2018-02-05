import pandas as pd
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from matplotlib.dates import AutoDateLocator, DateFormatter
import matplotlib.dates as dt
import datetime
import os
from sqlalchemy import create_engine


if __name__ == '__main__':


    year_start = 2000
    year_end = 2016
    period_1_start = '01-01'
    period_1_end = '01-31'
    period_2_start = '02-01'
    period_2_end = '02-29'
    period_3_start = '03-01'
    period_3_end = '03-31'
    period_4_start = '04-01'
    period_4_end = '04-30'
    period_5_start = '05-01'
    period_5_end = '05-31'
    period_6_start = '06-01'
    period_6_end = '06-30'
    period_7_start = '07-01'
    period_7_end = '07-31'
    period_8_start = '08-01'
    period_8_end = '08-31'
    period_9_start = '09-01'
    period_9_end = '09-30'
    period_10_start = '10-01'
    period_10_end = '10-31'
    period_11_start = '11-01'
    period_11_end = '11-30'
    period_12_start = '12-01'
    period_12_end = '12-31'

    start_date = str(year_start) + '-' + period_1_start
    end_date = str(year_end) + '-' + period_12_end




    stock_list = ['000001.XSHG', '000002.XSHG', '000003.XSHG', '000004.XSHG', '000005.XSHG', '000006.XSHG'
        , '000007.XSHG', '000008.XSHG', '000009.XSHG', '0000010.XSHG', '0000016.XSHG', '0000017.XSHG'
        , '0000020.XSHG', '000032.XSHG', '000033.XSHG', '000034.XSHG', '000035.XSHG', '000036.XSHG'
        , '000037.XSHG', '000038.XSHG', '000039.XSHG', '000040.XSHG', '000041.XSHG', '000043.XSHG'
        , '000044.XSHG', '000045.XSHG', '000046.XSHG', '000047.XSHG', '000090.XSHG', '000104.XSHG'
        , '000105.XSHG', '000106.XSHG', '000107.XSHG', '000108.XSHG', '000109.XSHG', '000110.XSHG'
        , '000111.XSHG', '000112.XSHG', '000113.XSHG', '000132.XSHG', '000133.XSHG', '000155.XSHG'
        , '000300.XSHG', '000852.XSHG', '000902.XSHG', '000903.XSHG', '000904.XSHG', '000905.XSHG'
        , '000906.XSHG', '000907.XSHG', '000980.XSHG', '000985.XSHG', '399001.XSHE'
        , '399003.XSHE', '399004.XSHE', '399005.XSHE', '399006.XSHE', '399007.XSHE', '399008.XSHE'
        , '399009.XSHE', '399010.XSHE', '399011.XSHE', '399012.XSHE', '399015.XSHE', '399300.XSHE'
        , '399903.XSHE', '399904.XSHE', '399905.XSHE', '399907.XSHE', '399980.XSHE'
        ]
    print(stock_list)

    stock_fundamentals_all = pd.DataFrame([])

    for order_book_id in stock_list:
        print('Now loading: ', order_book_id)
        if order_book_id[7:11] == 'XSHG':
            filename = 'sh' + order_book_id[0:6]
        else:
            filename = 'sz' + order_book_id[0:6]
        filepath = '/Users/yanghui/Documents/trading-data@full/index data/' + filename + '.csv'
        if os.path.exists(filepath):
            stock_fundamentals = pd.read_csv(filepath)
            stock_fundamentals = stock_fundamentals[(stock_fundamentals.date >= start_date) &
                                                (stock_fundamentals.date <= end_date)]
            stock_fundamentals_all = stock_fundamentals_all.append(stock_fundamentals)
            stock_fundamentals_all['order_book_id'] = stock_fundamentals_all['index_code'].map(
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
            period_start = str(year) + '-' + period_1_start
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

            #period_3
            period_start = str(year) + '-' + period_3_start
            period_end = str(year) + '-' + period_3_end
            stock_fundamentals = stock_fundamentals_all[(stock_fundamentals_all.date >= period_start) &
                                                         (stock_fundamentals_all.date <= period_end) &
                                                          (stock_fundamentals_all.order_book_id == order_book_id)]
            if len(stock_fundamentals) > 0:
                stock_fundamentals = stock_fundamentals.sort_values(by='date')
                price_start = stock_fundamentals.head(1).iloc[0]['open']
                price_end = stock_fundamentals.tail(1).iloc[0]['open']
                percent = 100 * (price_end - price_start)/price_start
                result_df_row.loc[0,'period_3'] = percent
            else:
                result_df_row.loc[0,'period_3'] = 'null'

            #period_4
            period_start = str(year) + '-' + period_4_start
            period_end = str(year) + '-' + period_4_end
            stock_fundamentals = stock_fundamentals_all[(stock_fundamentals_all.date >= period_start) &
                                                         (stock_fundamentals_all.date <= period_end) &
                                                          (stock_fundamentals_all.order_book_id == order_book_id)]
            if len(stock_fundamentals) > 0:
                stock_fundamentals = stock_fundamentals.sort_values(by='date')
                price_start = stock_fundamentals.head(1).iloc[0]['open']
                price_end = stock_fundamentals.tail(1).iloc[0]['open']
                percent = 100 * (price_end - price_start)/price_start
                result_df_row.loc[0,'period_4'] = percent
            else:
                result_df_row.loc[0,'period_4'] = 'null'

            #period_5
            period_start = str(year) + '-' + period_5_start
            period_end = str(year) + '-' + period_5_end
            stock_fundamentals = stock_fundamentals_all[(stock_fundamentals_all.date >= period_start) &
                                                         (stock_fundamentals_all.date <= period_end) &
                                                          (stock_fundamentals_all.order_book_id == order_book_id)]
            if len(stock_fundamentals) > 0:
                stock_fundamentals = stock_fundamentals.sort_values(by='date')
                price_start = stock_fundamentals.head(1).iloc[0]['open']
                price_end = stock_fundamentals.tail(1).iloc[0]['open']
                percent = 100 * (price_end - price_start)/price_start
                result_df_row.loc[0,'period_5'] = percent
            else:
                result_df_row.loc[0,'period_5'] = 'null'

            #period_6
            period_start = str(year) + '-' + period_6_start
            period_end = str(year) + '-' + period_6_end
            stock_fundamentals = stock_fundamentals_all[(stock_fundamentals_all.date >= period_start) &
                                                         (stock_fundamentals_all.date <= period_end) &
                                                          (stock_fundamentals_all.order_book_id == order_book_id)]
            if len(stock_fundamentals) > 0:
                stock_fundamentals = stock_fundamentals.sort_values(by='date')
                price_start = stock_fundamentals.head(1).iloc[0]['open']
                price_end = stock_fundamentals.tail(1).iloc[0]['open']
                percent = 100 * (price_end - price_start)/price_start
                result_df_row.loc[0,'period_6'] = percent
            else:
                result_df_row.loc[0,'period_6'] = 'null'

            #period_7
            period_start = str(year) + '-' + period_7_start
            period_end = str(year) + '-' + period_7_end
            stock_fundamentals = stock_fundamentals_all[(stock_fundamentals_all.date >= period_start) &
                                                         (stock_fundamentals_all.date <= period_end) &
                                                          (stock_fundamentals_all.order_book_id == order_book_id)]
            if len(stock_fundamentals) > 0:
                stock_fundamentals = stock_fundamentals.sort_values(by='date')
                price_start = stock_fundamentals.head(1).iloc[0]['open']
                price_end = stock_fundamentals.tail(1).iloc[0]['open']
                percent = 100 * (price_end - price_start)/price_start
                result_df_row.loc[0,'period_7'] = percent
            else:
                result_df_row.loc[0,'period_7'] = 'null'

            #period_8
            period_start = str(year) + '-' + period_8_start
            period_end = str(year) + '-' + period_8_end
            stock_fundamentals = stock_fundamentals_all[(stock_fundamentals_all.date >= period_start) &
                                                         (stock_fundamentals_all.date <= period_end) &
                                                          (stock_fundamentals_all.order_book_id == order_book_id)]
            if len(stock_fundamentals) > 0:
                stock_fundamentals = stock_fundamentals.sort_values(by='date')
                price_start = stock_fundamentals.head(1).iloc[0]['open']
                price_end = stock_fundamentals.tail(1).iloc[0]['open']
                percent = 100 * (price_end - price_start)/price_start
                result_df_row.loc[0,'period_8'] = percent
            else:
                result_df_row.loc[0,'period_8'] = 'null'

            #period_9
            period_start = str(year) + '-' + period_9_start
            period_end = str(year) + '-' + period_9_end
            stock_fundamentals = stock_fundamentals_all[(stock_fundamentals_all.date >= period_start) &
                                                         (stock_fundamentals_all.date <= period_end) &
                                                          (stock_fundamentals_all.order_book_id == order_book_id)]
            if len(stock_fundamentals) > 0:
                stock_fundamentals = stock_fundamentals.sort_values(by='date')
                price_start = stock_fundamentals.head(1).iloc[0]['open']
                price_end = stock_fundamentals.tail(1).iloc[0]['open']
                percent = 100 * (price_end - price_start)/price_start
                result_df_row.loc[0,'period_9'] = percent
            else:
                result_df_row.loc[0,'period_9'] = 'null'

            #period_10
            period_start = str(year) + '-' + period_10_start
            period_end = str(year) + '-' + period_10_end
            stock_fundamentals = stock_fundamentals_all[(stock_fundamentals_all.date >= period_start) &
                                                         (stock_fundamentals_all.date <= period_end) &
                                                          (stock_fundamentals_all.order_book_id == order_book_id)]
            if len(stock_fundamentals) > 0:
                stock_fundamentals = stock_fundamentals.sort_values(by='date')
                price_start = stock_fundamentals.head(1).iloc[0]['open']
                price_end = stock_fundamentals.tail(1).iloc[0]['open']
                percent = 100 * (price_end - price_start)/price_start
                result_df_row.loc[0,'period_10'] = percent
            else:
                result_df_row.loc[0,'period_10'] = 'null'

            #period_11
            period_start = str(year) + '-' + period_11_start
            period_end = str(year) + '-' + period_11_end
            stock_fundamentals = stock_fundamentals_all[(stock_fundamentals_all.date >= period_start) &
                                                         (stock_fundamentals_all.date <= period_end) &
                                                          (stock_fundamentals_all.order_book_id == order_book_id)]
            if len(stock_fundamentals) > 0:
                stock_fundamentals = stock_fundamentals.sort_values(by='date')
                price_start = stock_fundamentals.head(1).iloc[0]['open']
                price_end = stock_fundamentals.tail(1).iloc[0]['open']
                percent = 100 * (price_end - price_start)/price_start
                result_df_row.loc[0,'period_11'] = percent
            else:
                result_df_row.loc[0,'period_11'] = 'null'

            #period_12
            period_start = str(year) + '-' + period_12_start
            period_end = str(year) + '-' + period_12_end
            stock_fundamentals = stock_fundamentals_all[(stock_fundamentals_all.date >= period_start) &
                                                         (stock_fundamentals_all.date <= period_end) &
                                                          (stock_fundamentals_all.order_book_id == order_book_id)]
            if len(stock_fundamentals) > 0:
                stock_fundamentals = stock_fundamentals.sort_values(by='date')
                price_start = stock_fundamentals.head(1).iloc[0]['open']
                price_end = stock_fundamentals.tail(1).iloc[0]['open']
                percent = 100 * (price_end - price_start)/price_start
                result_df_row.loc[0,'period_12'] = percent
            else:
                result_df_row.loc[0,'period_12'] = 'null'

            #year increase
            year = year + 1
            result_df = result_df.append(result_df_row)

        count = count + 1

    result_df = result_df.sort_values(by=['code','year'])
    print(result_df)
    result_df.to_csv('/Users/yanghui/Desktop/temp_index.csv')


