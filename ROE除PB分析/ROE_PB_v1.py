#encoding: UTF-8
from time import strftime, localtime

import tushare as ts
import pandas as pd
if __name__ == '__main__':
    """
    跌破净值分析
    """

    # 基本面数据
    basic = ts.get_stock_basics()
    #print(basic)

    # 读取年报季报信息
    filename = 'stock_fundamentals_all'
    filepath = '/Users/yanghui/Documents/tushare/StockFundamentals_merge/'
    report_data = pd.read_excel(filepath + filename + '.xlsx')
    report_data['code'] = report_data['code'].map(lambda x: str(x).zfill(6))

    basic['roe_mean'] = None
    basic['roe_pb'] = None

    for stk in basic.index:
        print(strftime("%Y-%m-%d %H:%M:%S", localtime()) + '- Now calculating: ' + str(stk))
        report_data_code = report_data[report_data.code == stk]
        if len(report_data_code) > 0:
            report_data_code.sort_values(by='report_date', inplace=True)
            report_data_code = report_data_code.tail(3)
            #print(report_data_code)
            roe_mean = report_data_code['roe'].mean(axis=0)
            #print(roe_mean)
            basic.loc[stk, 'roe_mean'] = roe_mean
            pb = basic.loc[stk, 'pb']
            if pb > 0:
                basic.loc[stk, 'roe_pb'] = roe_mean / pb

    basic.sort_values(by=['industry','roe_pb'], inplace=True)
    filename = 'stock_fundamentals_roe_pb'
    basic.to_excel(filepath + filename + '.xlsx', encoding='GBK')
