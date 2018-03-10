from time import strptime, strftime
import pandas as pd
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from matplotlib.dates import AutoDateLocator, DateFormatter
import matplotlib.dates as dt
from datetime import *
import tushare as ts
import sys,os


# M1占比分析

if __name__ == '__main__':
    path = sys.path[0]
    working_folder = '/Users/huiyang/Documents/'
    today_ISO = datetime.today().date().isoformat()

    # read index
    filename = 'index_000001'
    index_sh = pd.read_excel(io=working_folder + \
         'SPSS modeler/复盘/' + filename + '.xlsx')
    filename = 'index_399001'
    index_sz = pd.read_excel(io=working_folder + \
         'SPSS modeler/复盘/' + filename + '.xlsx')

    money_supply = pd.read_excel(path + '/sina/货币供应量_宏观数据_新浪财经.xlsx')
    index_sh['date_str'] = index_sh['date'].apply(lambda x: str(x))
    index_sh = index_sh.sort_values(by='date')
    index_sz['date_str'] = index_sz['date'].apply(lambda x: str(x))
    index_sz = index_sz.sort_values(by='date')

    index_sh['month'] = index_sh.apply(lambda x: x['date_str'][:7], axis=1)
    index_sz['month'] = index_sz.apply(lambda x: x['date_str'][:7], axis=1)
    index_sz['amount_sz'] = index_sz['amount']
    index_sz['close_sz'] = index_sz['close']
    index_merge = index_sh.merge(index_sz[['amount_sz','close_sz','date']], on='date')
    index_merge_money = index_merge.merge(money_supply[[' 流通中现金(M0)(亿元)', ' 货币(狭义货币M1)(亿元)', 'month']], on='month')
    index_merge_money['amount_total'] = index_merge_money['amount'] + index_merge_money['amount_sz']
    index_merge_money['M0_percent'] = 100 * (index_merge_money['amount_total']/100000000)/index_merge_money[' 流通中现金(M0)(亿元)']
    index_merge_money['M1_percent'] = 100 * (index_merge_money['amount_total']/100000000)/index_merge_money[' 货币(狭义货币M1)(亿元)']
    index_merge_money['M0_percent_amp'] = 1000 * index_merge_money['M0_percent']
    index_merge_money['M1_percent_amp'] = 10000 * index_merge_money['M1_percent']
    #print(index_merge_money)
    #index_merge_money.to_csv('/Users/huiyang/Desktop/temp.csv', encoding='GBK')

    plt.grid(color='gray', which='both', linestyle='-', linewidth=1)
    plt.plot(index_merge_money['date'], index_merge_money['close'], 'r', linewidth=1,)
    plt.plot(index_merge_money['date'], index_merge_money['close_sz'], 'g', linewidth=1,)
    plt.plot(index_merge_money['date'], index_merge_money['M0_percent_amp'], 'b', linewidth=1,)
    plt.plot(index_merge_money['date'], index_merge_money['M1_percent_amp'], 'brown', linewidth=1,)
    #plt.hist(index_merge_money['M0_percent'],50,normed=1)

    plt.show()

