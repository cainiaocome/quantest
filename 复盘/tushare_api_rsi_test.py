#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
from datetime import *
from time import strftime, localtime, sleep
import tushare as ts
from tushare_api import tushare_api
import rqalpha
from tushare_api_rsi import TushareApiRsi

if __name__ == '__main__':
    """
    tushare_download data downloader to prepare the local data environment.
    """

    #TushareApiRsi().calculate_rsi()
    #testX = ts.get_h_data('000001', index=True, start='2017-01-01', end='2017-03-01').head(30)['close'].values
    #testY = ts.get_h_data('399001', index=True, start='2017-01-01', end='2017-03-01').head(30)['close'].values

    #testX = [1, 3, 8, 7, 9]  
    #testY = [2, 6, 16, 14, 18]  
    #today_ISO = datetime.today().date().isoformat()
    #tushare_api().downloadIndex(end=today_ISO)
    #TushareApiRsi().calculate_rsi()
    TushareApiRsi().calculateHindenburgOmen()
    #closeX = [10, 10000000, 10]  # mean:11.033333
    #closeY = [3307, 3637.7, 3637.7]   #mean: 3648.72033333
    #print(TushareApiRsi().computeCorrelation(closeX, closeY))
    
