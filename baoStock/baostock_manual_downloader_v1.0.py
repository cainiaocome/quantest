import baostock as bs
import pandas as pd
import sys,os
from pathlib import Path
from datetime import *


def query_trade_dates(start_date, end_date):
    """
    交易日查询：query_trade_dates()
    方法说明：查询股票交易日信息信息，可以通过参数设置获取起止年份数据，提供2014-2018年数据。 
    返回类型：pandas的DataFrame类型。
    """
    #### 登陆系统 ####
    lg = bs.login()
    # 显示登陆返回信息
    #print('login respond error_code:'+lg.error_code)
    #print('login respond  error_msg:'+lg.error_msg)

    #### 获取交易日信息 ####
    rs = bs.query_trade_dates(start_date=start_date, end_date=end_date)
    #print('query_trade_dates respond error_code:'+rs.error_code)
    #print('query_trade_dates respond  error_msg:'+rs.error_msg)

    #### 打印结果集 ####
    data_list = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        data_list.append(rs.get_row_data())
    result = pd.DataFrame(data_list, columns=rs.fields)

    #### 结果集输出到csv文件 ####   
    result.to_csv(path + "trade_dates.csv", encoding="gbk", index=False)

    #### 登出系统 ####
    bs.logout()
    return

def query_all_stock(start_date, end_date):
    """
    证券代码查询：query_all_stock()
    方法说明：查询证券代码及股票交易状态信息信息，可以通过参数‘某交易日’获取数据（包括：A股、指数），提供2014-今数据。 
    返回类型：pandas的DataFrame类型。
    """
    trading_days = pd.read_csv(path + "trade_dates.csv")
    trading_days = trading_days[trading_days.is_trading_day == 1]
    #print(trading_days)

    #### 登陆系统 ####
    lg = bs.login()

    # 显示登陆返回信息
    #print('login respond error_code:'+lg.error_code)
    #print('login respond  error_msg:'+lg.error_msg)
    result_all = pd.DataFrame([])
    for day in trading_days.calendar_date:
        if day >= start_date:
            #### 获取证券信息 ####
            rs = bs.query_all_stock(day=day)
            #print('query_all_stock respond error_code:'+rs.error_code)
            #print('query_all_stock respond  error_msg:'+rs.error_msg)

            #### 打印结果集 ####
            data_list = []
            while (rs.error_code == '0') & rs.next():
                # 获取一条记录，将记录合并在一起
                data_list.append(rs.get_row_data())
            result = pd.DataFrame(data_list, columns=rs.fields)
            #result.drop_duplicates(subset=['code'], keep='first', inplace=True)
            result['date'] = day
            result_all = result_all.append(result)

    #### 结果集输出到csv文件 ####   
    all_stock = pd.read_csv(path + "all_stock.csv")
    result_all = result_all.append(all_stock)
    result_all.drop_duplicates(subset=['code', 'tradeStatus', 'date'], keep='first', inplace=True)
    result_all.to_csv(path + "all_stock.csv", encoding="gbk", index=False)
    #print(result_all)

    #### 登出系统 ####
    bs.logout()
    return


def query_history_k_data(start_date, end_date):
    """
    获取历史A股K线数据：query_history_k_data()
    方法说明：获取A股历史交易数据（包括均线数据），
    可以通过参数设置获取日k线、周k线、月k线，以及5分钟、15分钟、30分钟和60分钟k线数据，
    适合搭配均线数据进行选股和分析。
    返回类型：pandas的DataFrame类型。
    可查询不复权、前复权、后复权数据。
    """
    all_stock = pd.read_csv(path + "all_stock.csv")
    all_stock.drop_duplicates(subset=['code'], keep='first', inplace=True)
    #### 登陆系统 ####
    lg = bs.login()
    # 显示登陆返回信息
    #print('login respond error_code:'+lg.error_code)
    #print('login respond  error_msg:'+lg.error_msg)

    #### 获取沪深A股历史K线数据 ####
    # 详细指标参数，参见“历史行情指标参数”章节
    result_all = pd.DataFrame([])
    for code in all_stock.code:
        rs = bs.query_history_k_data(code,
            "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,peTTM,pbMRQ,psTTM,pcfNcfTTM,isST",
            start_date=start_date, end_date=end_date,
            frequency="d", adjustflag="2")
        #print('query_history_k_data respond error_code:'+rs.error_code)
        #print('query_history_k_data respond  error_msg:'+rs.error_msg)

        #### 打印结果集 ####
        data_list = []
        while (rs.error_code == '0') & rs.next():
            # 获取一条记录，将记录合并在一起
            data_list.append(rs.get_row_data())
        result = pd.DataFrame(data_list, columns=rs.fields)
        result_all = result_all.append(result)

    #### 结果集输出到csv文件 ####   
    try:
        history_A_stock_k_data = pd.read_csv(path + "history_A_stock_k_data.csv")
    except:
        history_A_stock_k_data = pd.DataFrame([])
    result_all = result_all.append(history_A_stock_k_data)
    result_all.drop_duplicates(subset=['code', 'date'], keep='first', inplace=True)
    result_all.to_csv(path + "history_A_stock_k_data.csv", index=False)
    #print(result)

    #### 登出系统 ####
    bs.logout()
    return

def query_history_k_data_w(start_date, end_date):
    """
    获取历史A股K线数据：query_history_k_data()
    方法说明：获取A股历史交易数据（包括均线数据），
    可以通过参数设置获取日k线、周k线、月k线，以及5分钟、15分钟、30分钟和60分钟k线数据，
    适合搭配均线数据进行选股和分析。
    返回类型：pandas的DataFrame类型。
    可查询不复权、前复权、后复权数据。
    """
    all_stock = pd.read_csv(path + "all_stock.csv")
    all_stock.drop_duplicates(subset=['code'], keep='first', inplace=True)
    #### 登陆系统 ####
    lg = bs.login()
    # 显示登陆返回信息
    #print('login respond error_code:'+lg.error_code)
    #print('login respond  error_msg:'+lg.error_msg)

    #### 获取沪深A股历史K线数据 ####
    # 详细指标参数，参见“历史行情指标参数”章节
    result_all = pd.DataFrame([])
    for code in all_stock.code:
        rs = bs.query_history_k_data(code,
            "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,peTTM,pbMRQ,psTTM,pcfNcfTTM,isST",
            start_date=start_date, end_date=end_date,
            frequency="w", adjustflag="2")
        #print('query_history_k_data respond error_code:'+rs.error_code)
        #print('query_history_k_data respond  error_msg:'+rs.error_msg)

        #### 打印结果集 ####
        data_list = []
        while (rs.error_code == '0') & rs.next():
            # 获取一条记录，将记录合并在一起
            data_list.append(rs.get_row_data())
        result = pd.DataFrame(data_list, columns=rs.fields)
        result_all = result_all.append(result)
        print(result_all)

    #### 结果集输出到csv文件 ####   
    try:
        history_A_stock_k_data = pd.read_csv(path + "history_A_stock_k_data_w.csv")
    except:
        history_A_stock_k_data = pd.DataFrame([])
    result_all = result_all.append(history_A_stock_k_data)
    result_all.drop_duplicates(subset=['code', 'date'], keep='first', inplace=True)
    result_all.to_csv(path + "history_A_stock_k_data_w.csv", index=False)
    #print(result)

    #### 登出系统 ####
    bs.logout()
    return


def query_profit_data(start_date, end_date):
    """
    季频盈利能力：query_profit_data()
    方法说明：查询季频盈利能力信息，可以通过参数设置获取对应年份、季度数据，提供2007年至今数据。
    返回类型：pandas的DataFrame类型。
    """
    all_stock = pd.read_csv(path + "all_stock.csv")
    all_stock.drop_duplicates(subset=['code'], keep='first', inplace=True)
    end_year = int(end_date[0:4])
    quarter_list = [1,2,3,4]


    # 登陆系统
    lg = bs.login()
    # 显示登陆返回信息
    #print('login respond error_code:'+lg.error_code)
    #print('login respond  error_msg:'+lg.error_msg)

    result_all = pd.DataFrame([])
    for code in all_stock.code:
        # 查询季频估值指标盈利能力
        year = int(start_date[0:4])
        while (year <= end_year):
            for quarter in quarter_list:
                profit_list = []
                rs_profit = bs.query_profit_data(code=code, year=year, quarter=quarter)
                while (rs_profit.error_code == '0') & rs_profit.next():
                    profit_list.append(rs_profit.get_row_data())
                result_profit = pd.DataFrame(profit_list, columns=rs_profit.fields)
                result_all = result_all.append(result_profit)

            year = year + 1
        
    # 结果集输出到csv文件
    profit_data = pd.read_csv(path + "profit_data.csv")
    result_all = result_all.append(profit_data)
    result_all.drop_duplicates(subset=['code', 'pubDate', 'statDate'], keep='first', inplace=True)
    result_all.to_csv(path + "profit_data.csv", encoding="gbk", index=False)

    # 登出系统
    bs.logout()


def query_operation_data(start_date, end_date):

    """
    季频营运能力：query_operation_data()
    方法说明：查询季频营运能力信息，可以通过参数设置获取对应年份、季度数据，提供2007年至今数据。
    返回类型：pandas的DataFrame类型。
    """
    all_stock = pd.read_csv(path + "all_stock.csv")
    all_stock.drop_duplicates(subset=['code'], keep='first', inplace=True)
    end_year = int(end_date[0:4])
    quarter_list = [1,2,3,4]

    # 登陆系统
    lg = bs.login()
    # 显示登陆返回信息
    #print('login respond error_code:'+lg.error_code)
    #print('login respond  error_msg:'+lg.error_msg)

    # 营运能力
    result_all = pd.DataFrame([])
    for code in all_stock.code:
        # 查询季频估值指标盈利能力
        year = int(start_date[0:4])
        while (year <= end_year):
            for quarter in quarter_list:
                operation_list = []
                rs_operation = bs.query_operation_data(code=code, year=year, quarter=quarter)
                while (rs_operation.error_code == '0') & rs_operation.next():
                    operation_list.append(rs_operation.get_row_data())
                result_operation = pd.DataFrame(operation_list, columns=rs_operation.fields)
                result_all = result_all.append(result_operation)

            year = year + 1
        
    # 打印输出
    #print(result_operation)
    # 结果集输出到csv文件
    operation_data = pd.read_csv(path + "operation_data.csv")
    result_all = result_all.append(operation_data)
    result_all.drop_duplicates(subset=['code', 'pubDate', 'statDate'], keep='first', inplace=True)
    result_all.to_csv(path + "operation_data.csv", encoding="gbk", index=False)

    # 登出系统
    bs.logout()


def query_growth_data(start_date, end_date):
    """
    季频成长能力：query_growth_data()
    方法说明：查询季频成长能力信息，可以通过参数设置获取对应年份、季度数据，提供2007年至今数据。 
    返回类型：pandas的DataFrame类型。 
    """
    all_stock = pd.read_csv(path + "all_stock.csv")
    all_stock.drop_duplicates(subset=['code'], keep='first', inplace=True)
    end_year = int(end_date[0:4])
    quarter_list = [1,2,3,4]

    # 登陆系统
    lg = bs.login()
    # 显示登陆返回信息
    #print('login respond error_code:'+lg.error_code)
    #print('login respond  error_msg:'+lg.error_msg)

    # 成长能力
    result_all = pd.DataFrame([])
    for code in all_stock.code:
        # 查询季频估值指标盈利能力
        year = int(start_date[0:4])
        while (year <= end_year):
            for quarter in quarter_list:
                growth_list = []
                rs_growth = bs.query_growth_data(code=code, year=year, quarter=quarter)
                while (rs_growth.error_code == '0') & rs_growth.next():
                    growth_list.append(rs_growth.get_row_data())
                result_growth = pd.DataFrame(growth_list, columns=rs_growth.fields)
                result_all = result_all.append(result_growth)

            year = year + 1
    # 打印输出
    #print(result_growth)
    # 结果集输出到csv文件
    growth_data = pd.read_csv(path + "growth_data.csv")
    result_all = result_all.append(growth_data)
    result_all.drop_duplicates(subset=['code', 'pubDate', 'statDate'], keep='first', inplace=True)
    result_all.to_csv(path + "growth_data.csv", encoding="gbk", index=False)

    # 登出系统
    bs.logout()

def query_balance_data(start_date, end_date):
    """
    季频偿债能力：query_balance_data()
    方法说明：查询季频偿债能力信息，可以通过参数设置获取对应年份、季度数据，提供2007年至今数据。 
    返回类型：pandas的DataFrame类型。 
    """
    all_stock = pd.read_csv(path + "all_stock.csv")
    all_stock.drop_duplicates(subset=['code'], keep='first', inplace=True)
    end_year = int(end_date[0:4])
    quarter_list = [1,2,3,4]

    # 登陆系统
    lg = bs.login()
    # 显示登陆返回信息
    #print('login respond error_code:'+lg.error_code)
    #print('login respond  error_msg:'+lg.error_msg)

    # 偿债能力
    result_all = pd.DataFrame([])
    for code in all_stock.code:
        # 查询季频估值指标盈利能力
        year = int(start_date[0:4])
        while (year <= end_year):
            for quarter in quarter_list:
                balance_list = []
                rs_balance = bs.query_balance_data(code=code, year=year, quarter=quarter)
                while (rs_balance.error_code == '0') & rs_balance.next():
                    balance_list.append(rs_balance.get_row_data())
                result_balance = pd.DataFrame(balance_list, columns=rs_balance.fields)
                result_all = result_all.append(result_balance)

            year = year + 1

    # 打印输出
    #print(result_balance)
    # 结果集输出到csv文件
    balance_data = pd.read_csv(path + "balance_data.csv")
    result_all = result_all.append(balance_data)
    result_all.drop_duplicates(subset=['code', 'pubDate', 'statDate'], keep='first', inplace=True)
    result_all.to_csv(path + "balance_data.csv", encoding="gbk", index=False)

    # 登出系统
    bs.logout()


def query_cash_flow_data(start_date, end_date):
    """
    季频现金流量：query_cash_flow_data()
    方法说明：查询季频现金流量信息，可以通过参数设置获取对应年份、季度数据，提供2007年至今数据。 
    返回类型：pandas的DataFrame类型。 
    """
    all_stock = pd.read_csv(path + "all_stock.csv")
    all_stock.drop_duplicates(subset=['code'], keep='first', inplace=True)
    end_year = int(end_date[0:4])
    quarter_list = [1,2,3,4]


    # 登陆系统
    lg = bs.login()
    # 显示登陆返回信息
    #print('login respond error_code:'+lg.error_code)
    #print('login respond  error_msg:'+lg.error_msg)

    # 季频现金流量
    result_all = pd.DataFrame([])
    for code in all_stock.code:
        # 查询季频估值指标盈利能力
        year = int(start_date[0:4])
        while (year <= end_year):
            for quarter in quarter_list:
                cash_flow_list = []
                rs_cash_flow = bs.query_cash_flow_data(code=code, year=year, quarter=quarter)
                while (rs_cash_flow.error_code == '0') & rs_cash_flow.next():
                    cash_flow_list.append(rs_cash_flow.get_row_data())
                result_cash_flow = pd.DataFrame(cash_flow_list, columns=rs_cash_flow.fields)
                result_all = result_all.append(result_cash_flow)

            year = year + 1

    # 打印输出
    #print(result_cash_flow)
    # 结果集输出到csv文件
    cash_flow_data = pd.read_csv(path + "cash_flow_data.csv")
    result_all = result_all.append(cash_flow_data)
    result_all.drop_duplicates(subset=['code', 'pubDate', 'statDate'], keep='first', inplace=True)
    result_all.to_csv(path + "cash_flow_data.csv", encoding="gbk", index=False)

    # 登出系统
    bs.logout()

def query_dupont_data(start_date, end_date):
    """
    季频杜邦指数：query_dupont_data()
    方法说明：查询季频杜邦指数信息，可以通过参数设置获取对应年份、季度数据，提供2007年至今数据。 
    返回类型：pandas的DataFrame类型。
    """
    all_stock = pd.read_csv(path + "all_stock.csv")
    all_stock.drop_duplicates(subset=['code'], keep='first', inplace=True)
    end_year = int(end_date[0:4])
    quarter_list = [1,2,3,4]

    # 登陆系统
    lg = bs.login()
    # 显示登陆返回信息
    #print('login respond error_code:'+lg.error_code)
    #print('login respond  error_msg:'+lg.error_msg)

    # 查询杜邦指数
    result_all = pd.DataFrame([])
    for code in all_stock.code:
        # 查询季频估值指标盈利能力
        year = int(start_date[0:4])
        while (year <= end_year):
            for quarter in quarter_list:
                dupont_list = []
                rs_dupont = bs.query_dupont_data(code=code, year=year, quarter=quarter)
                while (rs_dupont.error_code == '0') & rs_dupont.next():
                    dupont_list.append(rs_dupont.get_row_data())
                result_profit = pd.DataFrame(dupont_list, columns=rs_dupont.fields)
                result_all = result_all.append(result_profit)

            year = year + 1

    # 打印输出
    #print(result_profit)
    # 结果集输出到csv文件
    dupont_data = pd.read_csv(path+ "dupont_data.csv")
    result_all = result_all.append(dupont_data)
    result_all.drop_duplicates(subset=['code', 'pubDate', 'statDate'], keep='first', inplace=True)
    result_all.to_csv(path + "dupont_data.csv", encoding="gbk", index=False)

    # 登出系统
    bs.logout()

def query_performance_express_report(start_date, end_date):
    """
    季频公司业绩快报：query_performance_express_report()
    方法说明：查询季频公司业绩快报信息，可以通过参数设置获取起止年份数据，提供2006年至今数据。
    返回类型：pandas的DataFrame类型。
    
    """
    all_stock = pd.read_csv(path + "all_stock.csv")
    all_stock.drop_duplicates(subset=['code'], keep='first', inplace=True)

    #### 登陆系统 ####
    lg = bs.login()
    # 显示登陆返回信息
    #print('login respond error_code:'+lg.error_code)
    #print('login respond  error_msg:'+lg.error_msg)

    #### 获取公司业绩快报 ####
    result_all = pd.DataFrame([])
    for code in all_stock.code:
        rs = bs.query_performance_express_report(code, start_date=start_date, end_date=end_date)
        #print('query_performance_express_report respond error_code:'+rs.error_code)
        #print('query_performance_express_report respond  error_msg:'+rs.error_msg)

        result_list = []
        while (rs.error_code == '0') & rs.next():
            result_list.append(rs.get_row_data())
            # 获取一条记录，将记录合并在一起
        result = pd.DataFrame(result_list, columns=rs.fields)
        result_all = result_all.append(result)

    #### 结果集输出到csv文件 ####
    performance_express_report = pd.read_csv(path + "performance_express_report.csv")
    result_all = result_all.append(performance_express_report)
    result_all.drop_duplicates(subset=['code', 'performanceExpPubDate', 'performanceExpStatDate', 'performanceExpUpdateDate'], keep='first', inplace=True)
    result_all.to_csv(path + "performance_express_report.csv", encoding="gbk", index=False)
    #print(result)

    #### 登出系统 ####
    bs.logout()

def query_forcast_report(start_date, end_date):
    """
    季频公司业绩预告：query_forcast_report()
    方法说明：查询季频公司业绩预告信息，可以通过参数设置获取起止年份数据，提供2003年至今数据。 
    返回类型：pandas的DataFrame类型。
    """
    all_stock = pd.read_csv(path + "all_stock.csv")
    all_stock.drop_duplicates(subset=['code'], keep='first', inplace=True)
    #### 登陆系统 ####
    lg = bs.login()
    # 显示登陆返回信息
    #print('login respond error_code:'+lg.error_code)
    #print('login respond  error_msg:'+lg.error_msg)

    #### 获取公司业绩预告 ####
    result_all = pd.DataFrame([])
    for code in all_stock.code:
        rs_forecast = bs.query_forecast_report(code, start_date=start_date, end_date=end_date)
        #print('query_forecast_reprot respond error_code:'+rs_forecast.error_code)
        #print('query_forecast_reprot respond  error_msg:'+rs_forecast.error_msg)
        rs_forecast_list = []
        while (rs_forecast.error_code == '0') & rs_forecast.next():
            # 分页查询，将每页信息合并在一起
            rs_forecast_list.append(rs_forecast.get_row_data())
        result_forecast = pd.DataFrame(rs_forecast_list, columns=rs_forecast.fields)
        result_all = result_all.append(result_forecast)
    #### 结果集输出到csv文件 ####
    forecast_report = pd.read_csv(path + "forecast_report.csv")
    result_all = result_all.append(forecast_report)
    result_all.drop_duplicates(subset=['code', 'profitForcastExpPubDate', 'profitForcastExpStatDate'], keep='first', inplace=True)

    result_all.to_csv(path + "forecast_report.csv", encoding="gbk", index=False)
    #print(result_forecast)

    #### 登出系统 ####
    bs.logout()

if __name__ == '__main__':
    '''
    
    all APIs you can find in below website -
    http://baostock.com/

    download flow - 
        
    +-------------------+     +-----------------+     +----------------------+
    | query_trade_dates | --> | query_all_stock | --> | query_history_k_data |
    | (run once only)   |     +-----------------+  |  +----------------------+  
    +-------------------+                          |                                 
                                                   |  +----------------------+
                                                   |->| query_profit_data    |
                                                   |  +----------------------+
                                                   |  +----------------------+
                                                   |->| query_operation_data |
                                                   |  +----------------------+
                                                   |  +----------------------+
                                                   |->| query_growth_data    |
                                                   |  +----------------------+
                                                   |  +----------------------+
                                                   |->| query_balance_data   |
                                                   |  +----------------------+
                                                   |  +----------------------+
                                                   |->| query_cash_flow_data |
                                                   |  +----------------------+
                                                   |  +----------------------+
                                                   |->| query_dupont_data    |
                                                   |  +----------------------+
                                                   |  +-----------------------------------+
                                                   |->| query_performance_express_report  | 
                                                   |  +-----------------------------------+
                                                   |  +----------------------+
                                                   |->| query_forcast_report |
                                                      +----------------------+
    '''

    path = '/Users/huiyang/Documents/quantest/data_Shared/baoStock/'
    today_ISO = datetime.today().date().isoformat()

    start_date = '2018-07-01'
    end_date = today_ISO
    #end_date = '2018-12-31'
    #step 1:
    #query_trade_dates(start_date=start_date, end_date='2018-12-31')

    #step 2:
    query_all_stock(start_date=start_date, end_date=end_date)

    # depends on step 2
    #query_history_k_data(start_date=start_date, end_date=end_date)
    #query_profit_data(start_date=start_date, end_date=end_date)
    #query_operation_data(start_date=start_date, end_date=end_date)
    #query_growth_data(start_date=start_date, end_date=end_date)
    query_balance_data(start_date=start_date, end_date=end_date)
    #query_cash_flow_data(start_date=start_date, end_date=end_date)
    #query_dupont_data(start_date=start_date, end_date=end_date)
    #query_performance_express_report(start_date=start_date, end_date=end_date)
    
    # below functions not working
    #query_forcast_report(start_date=start_date, end_date=end_date)
    #query_history_k_data_w(start_date='2018-01-01', end_date=end_date)
