import tushare as ts
import rqalpha as rq

if __name__ == '__main__':
    stock_list = ts.get_stock_basics()
    stock_list.loc[:,'name_3'] = stock_list.apply(lambda x: x['name'][0:3], axis=1)
    ST_list = stock_list[stock_list.name_3 == '*ST']
    ST_list.drop(['name_3'], inplace=True, axis=1, errors='ignore')
    ST_list.loc[:,'5日涨幅'] = 0
    ST_list.loc[:,'10日涨幅'] = 0
    ST_list.loc[:,'20日涨幅'] = 0
    ST_list.loc[:,'最新价格'] = 0
    ST_list.loc[:,'最新价格'] = 0
    ST_list.loc[:,'限售股解禁'] = "N"
    xsg1 = ts.xsg_data(month='02')  #限售股解禁
    xsg2 = ts.xsg_data(month='03')  #限售股解禁
    xsg3 = ts.xsg_data(month='04')  #限售股解禁
    for stk in ST_list.index:
        # 20日涨幅
        hist = ts.get_hist_data(stk, start='2017-02-08', end='2017-03-07').sort_index(ascending=False)
        if len(hist) > 0:
            start_price = hist.tail(1).iloc[0,0]
            end_price = hist.head(1).iloc[0,0]
            percentage = 100 * (end_price - start_price) / start_price
            ST_list.loc[stk, '20日涨幅'] = percentage

            # 最新价格
            ST_list.loc[stk, '最新价格'] = end_price

        #10日涨幅
        hist_10 = hist[hist.index >= '2017-02-22']
        if len(hist_10) > 0:
            start_price = hist_10.tail(1).iloc[0,0]
            end_price = hist_10.head(1).iloc[0,0]
            percentage = 100 * (end_price - start_price) / start_price
            ST_list.loc[stk, '10日涨幅'] = percentage

        #5日涨幅
        hist_5 = hist[hist.index >= '2017-03-01']
        if len(hist_5) > 0:
            start_price = hist_5.tail(1).iloc[0,0]
            end_price = hist_5.head(1).iloc[0,0]
            percentage = 100 * (end_price - start_price) / start_price
            ST_list.loc[stk, '5日涨幅'] = percentage


        #检查是否有限售股解禁
        if stk in xsg1.code or  stk in xsg2.code or stk in xsg3.code:
            ST_list.loc[stk,'限售股解禁'] = "Y"



    #输出
    ST_list = ST_list.sort_index(ascending=True)
    ST_list.to_csv('/Users/yanghui/Desktop/ST_stock_v1.csv', encoding='GBK')
