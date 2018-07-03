#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import baostock as bs
import sys
import talib

timeperiod = 5

#### 登陆系统 ####
lg = bs.login()
# 显示登陆返回信息
#print('login respond error_code:'+lg.error_code)
#print('login respond  error_msg:'+lg.error_msg)

#### 获取历史K线数据 ####
#指数代码	指数简称	指数全称	发布时间	发布机构	指数简介
#sh.000935	中证信息	中证信息技术指数	2009/7/3	中证指数有限公司	将中证800指数800只样本股中属于信息技术行业的全部股票作为样本，以反映沪深A股中该行业公司股票的整体表现。
#sz.399620	深证信息	深证信息技术行业指数	2011/6/15	深圳证券交易所	为反映深市不同行业公司股票的整体表现，将深市个股按国证行业分类标准分为10个行业，以覆盖所属行业75%的市值为目标。
#sz.399675	深互联网	深A软件互联	2015/6/8	深圳证券交易所	
#sz.399915	300 信息	沪深300信息技术指数	2007/7/2	中证指数有限公司	将沪深300指数成份股按行业分类标准进行分类，选取归属于信息技术行业的全部股票构成指数成份股。
#sz.399935	中证信息	中证信息技术指数	2009/7/3	中证指数有限公司	将中证800指数800只样本股按行业分类标准分为10个行业，选取归属于信息技术行业的全部股票作为样本。
#sh.000858	500信息	中证500信息技术指数	2013/11/6	中证指数有限公司	从中证500指数成份股中选择信息技术行业的全部股票组成样本股，反映该行业公司股票的整体表现。
#sh.000077	信息等权	上证信息技术行业分层等权重指数	2010/8/18	上海证券交易所	与上证行业指数系列选样方法相同，但在加权方式上，上证行业分层等权重指数中各二级行业权重与其自由流通市值权重相当，并对二级行业内股票采取等权重加权方式。
# 详细指标参数，参见“历史行情指标参数”章节
rs = bs.query_history_k_data("sh.000935",
    "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,peTTM,pbMRQ,psTTM,pcfNcfTTM,isST",
    start_date='2017-05-01', end_date='2018-12-31', 
    frequency="d", adjustflag="2") #frequency="d"取日k线，adjustflag="3"默认不复权
#print('query_history_k_data respond error_code:'+rs.error_code)
#print('query_history_k_data respond  error_msg:'+rs.error_msg)

#### 打印结果集 ####
data_list = []
while (rs.error_code == '0') & rs.next():
    # 获取一条记录，将记录合并在一起
    data_list.append(rs.get_row_data())
result = pd.DataFrame(data_list, columns=rs.fields)
#### 结果集输出到csv文件 ####
path = sys.path[0]
#result.to_csv(path + "/history_k_data_sh_000935.csv", encoding="gbk", index=False)
#print(result)


close = result['close'].tail(timeperiod + 1).values
close = np.array(close, dtype=float)
#print(close)
stock_rsi = talib.RSI(close, timeperiod)[-1]
print('sh.000935	中证信息 RSI = ' + str(stock_rsi))



rs = bs.query_history_k_data("sz.399620",
    "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,peTTM,pbMRQ,psTTM,pcfNcfTTM,isST",
    start_date='2017-05-01', end_date='2018-12-31', 
    frequency="d", adjustflag="2") #frequency="d"取日k线，adjustflag="3"默认不复权
#print('query_history_k_data respond error_code:'+rs.error_code)
#print('query_history_k_data respond  error_msg:'+rs.error_msg)

#### 打印结果集 ####
data_list = []
while (rs.error_code == '0') & rs.next():
    # 获取一条记录，将记录合并在一起
    data_list.append(rs.get_row_data())
result = pd.DataFrame(data_list, columns=rs.fields)
#### 结果集输出到csv文件 ####
path = sys.path[0]
#result.to_csv(path + "/history_k_data_sh_000935.csv", encoding="gbk", index=False)
#print(result)


close = result['close'].tail(timeperiod + 1).values
close = np.array(close, dtype=float)
#print(close)
stock_rsi = talib.RSI(close, timeperiod)[-1]
print('sz.399620	深证信息 RSI = ' + str(stock_rsi))



rs = bs.query_history_k_data("sz.300059",
    "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,peTTM,pbMRQ,psTTM,pcfNcfTTM,isST",
    start_date='2017-05-01', end_date='2018-12-31', 
    frequency="d", adjustflag="2") #frequency="d"取日k线，adjustflag="3"默认不复权
#print('query_history_k_data respond error_code:'+rs.error_code)
#print('query_history_k_data respond  error_msg:'+rs.error_msg)

#### 打印结果集 ####
data_list = []
while (rs.error_code == '0') & rs.next():
    # 获取一条记录，将记录合并在一起
    data_list.append(rs.get_row_data())
result = pd.DataFrame(data_list, columns=rs.fields)

close = result['close'].tail(timeperiod + 1).values
close = np.array(close, dtype=float)
#print(close)
stock_rsi = talib.RSI(close, timeperiod)[-1]
print('sh.300059	东方财富 RSI = ' + str(stock_rsi))



#### 登出系统 ####
bs.logout()
