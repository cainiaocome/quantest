# encoding: UTF-8
from time import strftime, localtime
import pandas as pd
from datetime import *
import tushare as ts
from deprecated import deprecated



def download_stock_W1(year=2010, end=2018):
    """
    下载周线数据（前复权）
    """
    
    working_folder = '/Users/huiyang/Documents/quantest/data_shared/tuShare/'

    #print('downloading the stock weekly data...')
    path = '/Users/huiyang/Documents/quantest/data_Shared/baoStock/'
    all_stock = pd.read_csv(path + "all_stock.csv")
    all_stock['code'] = all_stock['code'].map(lambda x: x[3:9])
    stock_list = all_stock.code.drop_duplicates().tolist()
    print(stock_list)

    stock_data = pd.DataFrame([])
    for code in stock_list:
        #code = code[3:9]
        print(code)
        year_count = year
        while year_count <= end:
            #print(str(year_count))
            start_date = str(year_count) + '-01-01'
            end_date = str(year_count) + '-12-31'
            #try:
            #stock_data_latest = ts.get_k_data(code=code, ktype='W', autype=None, \
            #                    index=False, start=start_date, end=end_date)
            stock_data_latest = ts.get_hist_data(code=code, ktype='W',  \
                                 start=start_date, end=end_date)
            if  stock_data_latest is not None:
                stock_data_latest['code'] = code    
                stock_data = stock_data.append(stock_data_latest)
            #except:
            #    pass
            year_count = year_count + 1
        #total = total + 1
        #print('downloading-' + stock + ' for the weekly data, total count: ' + str(len(stock_data)))

    filename = 'hist_data_W1.xlsx'
    stock_data.to_excel(working_folder + filename)
    #print('download_stock_W1_qfq successful ' + str(total))
    return

def download_stock_M1(year=2010, end=2018):
    """
    下载周线数据（前复权）
    """
    
    working_folder = '/Users/huiyang/Documents/quantest/data_shared/tuShare/'

    #print('downloading the stock weekly data...')
    path = '/Users/huiyang/Documents/quantest/data_Shared/baoStock/'
    all_stock = pd.read_csv(path + "all_stock.csv")
    all_stock['code'] = all_stock['code'].map(lambda x: x[3:9])
    stock_list = all_stock.code.drop_duplicates().tolist()
    print(stock_list)

    stock_data = pd.DataFrame([])
    for code in stock_list:
        #code = code[3:9]
        print(code)
        year_count = year
        while year_count <= end:
            #print(str(year_count))
            start_date = str(year_count) + '-01-01'
            end_date = str(year_count) + '-12-31'
            #try:
            stock_data_latest = ts.get_hist_data(code=code, ktype='M',  \
                                 start=start_date, end=end_date)
            if  stock_data_latest is not None:
                stock_data_latest['code'] = code    
                stock_data = stock_data.append(stock_data_latest)
            #except:
            #    pass
            year_count = year_count + 1
        #total = total + 1
        #print('downloading-' + stock + ' for the weekly data, total count: ' + str(len(stock_data)))

    filename = 'hist_data_M1.xlsx'
    stock_data.to_excel(working_folder + filename)
    return


if __name__ == '__main__':    
    #download_stock_W1(year=2010, end=2018)
    download_stock_M1(year=2010, end=2018)