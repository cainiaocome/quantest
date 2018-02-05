import pandas as pd
import os
from sqlalchemy import create_engine


if __name__ == '__main__':


    year_start = 2005
    year_end = 2009
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
    result_df.to_csv('/Users/yanghui/Desktop/temp2005_2009.csv')


