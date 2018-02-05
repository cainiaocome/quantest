"""
涨停敢死队
这个策略比较适合平衡市

"""
import rqalpha as pd
import pandas as pd
import datetime
# 可以自己import我们平台支持的第三方python模块，比如pandas、numpy等。
# 在这个方法中编写任何的初始化逻辑。context对象将会在你的算法策略的任何方法之间做传递。
from rqalpha import logger
from rqalpha.api import order_target_percent, check_is_trading
from rqalpha.utils import convert_date_to_int, convert_int_to_date
from sqlalchemy import create_engine
from rqalpha.data.bar import *
from rqalpha.data.data_accessor import *
import matplotlib.pyplot


def init(context):
    print('initializing the strategy...')
    context.universe = []
    context.stock = '000001.XSHE'
    context.today = ''

    #load the 3rd party data into memory
    #context.term_suspended = load_term_suspended()
    #context.all_instruments = load_all_instruments()
    context.trade_cal = load_trade_cal()
    #context.stock_all = list(context.all_instruments.order_book_id)
    #context.stock_all = list(set(context.stock_all))
    context.stock_all_d1 = load_stock_d1()
    #context.all_d1 = load_all_limit_up(context.stock_all)
    print('initializing finished!')


# before_trading此函数会在每天交易开始前被调用，当天只会被调用一次
def before_trading(context, bar_dict):
    """
    """
    context.today = context.now.date()
    context.today = str(context.today)
    prev_date_df = context.trade_cal[context.trade_cal.calendarDate == context.today]
    prev_calendar_date = prev_date_df.iloc[0]['prevTradeDate']
    context.universe = []
    #check if the stock is limit up in the previous trading date
    top_up = context.stock_all_d1[(context.stock_all_d1.date == prev_calendar_date) &
                (context.stock_all_d1.open < context.stock_all_d1.ma20) &
                (context.stock_all_d1.close > context.stock_all_d1.ma20)]
    if len(top_up) > 0:
        context.universe.append(context.stock)



    # 去除停牌股票
    #today = str(today)
    #for stk in context.stock_all:
    #   if is_suspended(stk=stk,all=context.suspend_all,today=today):
    #        context.universe.remove(stk)
    #for stk in context.universe:
    #    if not is_trading(stk,today)
    #        context.universe.remove(stk)


    # 对筛选好的股票池切片
    #context.universe = context.universe[0:context.buyStkCount]
    #logger.info('buyList:' + str(context.universe))


# 你选择的证券的数据更新将会触发此段逻辑，例如日或分钟历史数据切片或者是实时数据切片更新

def handle_bar(context, bar_dict):
    # 根据前一交易日的股票池入市买卖
    for order_book_id in context.portfolio.positions:
        if order_book_id not in context.universe:
            order_target_percent(order_book_id, 0)
    for order_book_id in context.universe:
        if order_book_id not in context.portfolio.positions:
            order_target_percent(order_book_id, 1)
    #matplotlib.pyplot.style.use()


##################################################################################################################
#
# APIs to load the 3rd party data
#
##################################################################################################################


def load_all_instruments():
    """
    load all stock and filter the blacklist
    :return: dict of StockBasics table
    """
    stock_blackList = ["600656.XSHG", "300372.XSHE", "600403.XSHG", "600421.XSHG",
                       "600733.XSHG", "300399.XSHE", "600145.XSHG", "002679.XSHE", "000020.XSHE", "002330.XSHE",
                       "300117.XSHE", "300135.XSHE",
                       "002566.XSHE", "002119.XSHE", "300208.XSHE", "002237.XSHE", "002608.XSHE", "000691.XSHE",
                       "002694.XSHE", "002715.XSHE", "002211.XSHE", "000788.XSHE", "300380.XSHE", "300028.XSHE",
                       "000668.XSHE", "300033.XSHE", "300126.XSHE", "300340.XSHE", "300344.XSHE", "002473.XSHE",
                       '000594.XSHE','603859.XSHG']

    engine_stock_fundamentals = create_engine("mysql+mysqldb://root:good@localhost:3306/TUSHARE_STOCK_FUNDAMENTALS",
                                          encoding='utf-8', echo=False)
    connection = engine_stock_fundamentals.connect()
    sql = "select * from TUSHARE_STOCK_FUNDAMENTALS.StockBasics"

    stock_all = pd.read_sql(sql, engine_stock_fundamentals)
    connection.close()
    stock_all['order_book_id'] = stock_all['code'].map(
        lambda x: x + '.XSHG' if x >= '600000' else x + '.XSHE')

    #remove the stock in blacklist
    for stock in stock_blackList:
        stock_all = stock_all[stock_all.order_book_id != stock]
    return stock_all


# load the stocks is not suspended and terminated till the day
# it will added to the main stock list as we don't know when it will be termed or suspended.
def load_term_suspended():
    """
    load all stocks term and suspended
    :return: dict of StockTermSuspended table
    """
    #load the stock which is suspended
    engine_stock_fundamentals = create_engine("mysql+mysqldb://root:good@localhost:3306/TUSHARE_STOCK_FUNDAMENTALS",
                                          encoding='utf-8', echo=False)
    connection = engine_stock_fundamentals.connect()
    sql = "select * from StockTermSuspend where code < '700000'"
    stock_term_suspended = pd.read_sql(sql, engine_stock_fundamentals)
    connection.close()
    stock_term_suspended['order_book_id'] = stock_term_suspended['code'].map(lambda x: x + '.XSHG' if x >= '600000' else x + '.XSHE')
    return stock_term_suspended


def load_trade_cal():
    """
    load all stocks term and suspended
    :return: dict of StockTermSuspended table
    """
    #load the trade calendar
    engine_stock_fundamentals = create_engine("mysql+mysqldb://root:good@localhost:3306/TUSHARE_STOCK_FUNDAMENTALS",
                                          encoding='utf-8', echo=False)
    connection = engine_stock_fundamentals.connect()
    sql = "select * from StockTradeCal"
    stock_trade_cal = pd.read_sql(sql, engine_stock_fundamentals)
    connection.close()
    return stock_trade_cal



def load_stock_d1():
    return pd.read_csv('/Users/yanghui/Documents/tushare_download/StockDaily/daily_all.csv')



#TODO: to be deprecated
#load all limit up stocks
def load_all_limit_up(stock_list):
    """
    load all stocks price touch the limit up to 10%
    :param :
    :return: dict of the table - TUSHARE_STOCK_D1
    """

    stock_d1_all = pd.DataFrame(columns={'code'})
    for order_book_id in stock_list:
        code = order_book_id[0:6]
        engine_stock_d1 = create_engine("mysql+mysqldb://root:good@localhost:3306/TUSHARE_STOCK_D1",
                                        encoding='utf-8', echo=False)
        connection = engine_stock_d1.connect()
        sql = "select * from `" + code + "` where code = '" + code + "'"
        stock_d1= pd.read_sql(sql, engine_stock_d1)
        connection.close()
        stock_d1_all.append(stock_d1)
    stock_d1_all['order_book_id'] = stock_d1_all['code'].map(lambda x: x + '.XSHG' if x >= '600000' else x + '.XSHE')
    return stock_d1_all



#TODO: to be deprecated
def is_suspended(stk,all,today):
    stk = stk[0:6]
    for row in all:
        if row['code'] == stk and row['tDate'] <= today :
            return True
    return False

#TODO: to be finished
def is_trading(id_or_symbols,today):
    id_or_symbols = id_or_symbols[0:6]
    engine_stock_d1 = create_engine("mysql+mysqldb://root:good@localhost:3306/TUSHARE_STOCK_D1",
                                          encoding='utf-8', echo=False)
    connection = engine_stock_d1.connect()
    sql = "select * from `" + id_or_symbols + "` where code = '" + id_or_symbols + "'" + " and date = '" + today + "'"
    stock_data = connection.execute(sql)
    connection.close()
    if stock_data.rowcount > 0:
        return True
    else:
        return False

#TODO: to be deprecated
def get_history(order_book_id,dt, bar_count):
    engine_stock_d1 = create_engine("mysql+mysqldb://root:good@localhost:3306/TUSHARE_STOCK_D1",
                                        encoding='utf-8', echo=False)
    code = order_book_id[0:6]
    connection = engine_stock_d1.connect()
    n = str(bar_count)
    sql = "select * from `" + code + "` where code = '" + code + "'" + " and date < '" + dt + "' order by date desc LIMIT " + n
    stock_data = connection.execute(sql)
    connection.close()
    return stock_data.fetchall()


#判断是否涨停
def is_limit_up(order_book_id='',prev_calendar_date='2000-01-01'):
    code = order_book_id[0:6]
    engine_stock_d1 = create_engine("mysql+mysqldb://root:good@localhost:3306/TUSHARE_STOCK_D1",
                                        encoding='utf-8', echo=False)
    connection = engine_stock_d1.connect()
    sql = "select * from `" + code + "` where date = " + prev_calendar_date + " and p_change > 9.9 order by date LIMIT 1"
    stock_d1 = pd.read_sql(sql=sql, con=engine_stock_d1)
    connection.close()
    if stock_d1 is not None:
        return True
    else:
        return False

