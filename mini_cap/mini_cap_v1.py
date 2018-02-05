"""
这个策略比较适合平衡市
策略逻辑： 选出市值最小市值股票，去除ST股票，成交量大于3000万，前一交易日涨跌幅在-3% - 9.9%之间，加入股票池并买入5只。
卖出条件：
不在选股范围的股票
"""

# 可以自己import我们平台支持的第三方python模块，比如pandas、numpy等。
import os
import pandas as pd


# 在这个方法中编写任何的初始化逻辑。context对象将会在你的算法策略的任何方法之间做传递。
import talib
from rqalpha.api import order_target_percent, plot
from sqlalchemy import create_engine



def init(context):
    logger.info('initializing the strategy...')
    context.SHORTPERIOD = 20
    context.LONGPERIOD = 120
    context.show_progress = True
    context.buyStkCount = 5
    context.total = 50
    #scheduler.run_weekly(func=before_trading,weekday=1)
    #scheduler.run_weekly(func=handle_bar,weekday=1)
    #context.blackList = ["600656.XSHG", "300372.XSHE", "600403.XSHG", "600421.XSHG", "600733.XSHG", "300399.XSHE",
    #                     "600145.XSHG", "002679.XSHE", "000020.XSHE", "002330.XSHE", "300117.XSHE", "300135.XSHE",
    #                     "002566.XSHE", "002119.XSHE", "300208.XSHE", "002237.XSHE", "002608.XSHE", "000691.XSHE",
    #                     "002694.XSHE", "002715.XSHE", "002211.XSHE", "000788.XSHE", "300380.XSHE", "300028.XSHE",
    #                     "000668.XSHE", "300033.XSHE", "300126.XSHE", "300340.XSHE", "300344.XSHE", "002473.XSHE",
    #                    '000594.XSHE']
    context.blackList = []

    load_trade_cal(context)
    load_all_instruments(context)
    load_stock_fundamentals(context)
    #context.stock_all = list(context.all_instruments.order_book_id)
    load_st_classified(context)
    logger.info('initialization completed!')
    #scheduler.run_daily(function)
    #scheduler.run_weekly(function, weekday=x, tradingday=t)
    #scheduler.run_monthly(before_trading, tradingday=1)
    #scheduler.run_monthly(handle_bar, tradingday=1)



# before_trading此函数会在每天交易开始前被调用，当天只会被调用一次
def before_trading(context, bar_dict):
    context.today = context.now.date()
    context.today = str(context.today)

    #get previous trading date
    context.prev_calendar_date = get_prev_trade_date(context,context.today)
    context.universe = []

    # 筛市值最小的股票，并按市值升序排列

    fundamental_df = context.fundamentals_all[(context.fundamentals_all.date == context.prev_calendar_date) &
                                              (context.fundamentals_all.market_value < 5000000000) &
                                              (context.fundamentals_all.open < 7)
                                              ]
    fundamental_df = fundamental_df.sort_values(by='market_value',ascending=1)

    context.stocks = []
    context.buylist = []

    # 过滤st股票
    context.stocks = list(fundamental_df['order_book_id'])
    for stk in context.stocks:
        if stk in context.st_classified['order_book_id'].values:
            context.stocks.remove(stk)


    # 过滤前一交易日跌3%和涨停的股票
    for stk in context.stocks:
        percentage_yesterday = get_percentage(context,context.prev_calendar_date,stk)
        if percentage_yesterday >= 0.099 or percentage_yesterday <= -0.03:
            context.stocks.remove(stk)
            #logger.info('removed stock for 涨停和跌3% :' + stk + ' percent prev date: %.2f%%' % (percentage * 100))

    # 对筛选好的股票池切片

    context.universe = context.stocks[0:context.buyStkCount]
    logger.info('buyList:' + str(context.universe))


#    update_universe(context.stocks)


# 你选择的证券的数据更新将会触发此段逻辑，例如日或分钟历史数据切片或者是实时数据切片更新
def handle_bar(context, bar_dict):
    #count = context.buyStkCount
    context.today = context.now.date()
    context.today = str(context.today)
    #context.prev_calendar_date = get_prev_trade_date(context,context.today)

    for stk in context.portfolio.positions:
        percentage_today = get_percentage(context, context.today, stk)
        if percentage_today >= 0.099 or percentage_today <= -0.03:
            if stk in context.universe:
                context.universe.remove(stk)
        if stk not in context.universe:
            if (bar_dict[stk].close == bar_dict[stk].open == bar_dict[stk].high == bar_dict[stk].low) and \
                            percentage_today <= - 0.099:
                logger.info('跌停无法卖出：' + stk)
            else:
                order_target_percent(stk, 0)
                logger.info('sell:' + str(stk) + ' percent today: %.2f%%' % (percentage_today * 100))
        # 买入新股
    for stk in context.universe:
        if stk not in context.portfolio.positions:
            percentage_today = get_percentage(context, context.today, stk)
            if (bar_dict[stk].close == bar_dict[stk].open == bar_dict[stk].high == bar_dict[stk].low) and \
                            percentage_today >= 0.099:
                logger.info('涨停无法买入：' + stk)
            else:
                if len(context.portfolio.positions) < context.buyStkCount:
                    percentage_today = get_percentage(context, context.today, stk)
                    logger.info('buyin:' + str(stk) + ' percent today: %.2f%%' % (percentage_today * 100))
                    order_shares(stk, 500)


def load_all_instruments(context):
    """
    load all stock and filter the blacklist
    :return: dict of StockBasics table
    """
    #stock_blackList = ["600656.XSHG", "300372.XSHE", "600403.XSHG", "600421.XSHG",
    #                   "600733.XSHG", "300399.XSHE", "600145.XSHG", "002679.XSHE", "000020.XSHE", "002330.XSHE",
    #                   "300117.XSHE", "300135.XSHE",
    #                   "002566.XSHE", "002119.XSHE", "300208.XSHE", "002237.XSHE", "002608.XSHE", "000691.XSHE",
    #                   "002694.XSHE", "002715.XSHE", "002211.XSHE", "000788.XSHE", "300380.XSHE", "300028.XSHE",
    #                   "000668.XSHE", "300033.XSHE", "300126.XSHE", "300340.XSHE", "300344.XSHE", "002473.XSHE",
    #                   '000594.XSHE','603859.XSHG']
    stock_blackList = ["300372.XSHE"]

    engine_stock_fundamentals = create_engine("mysql+mysqldb://root:good@localhost:3306/TUSHARE_STOCK_FUNDAMENTALS",
                                          encoding='utf-8', echo=False)
    connection = engine_stock_fundamentals.connect()
    sql = "select * from TUSHARE_STOCK_FUNDAMENTALS.StockBasics"

    context.stock_all = pd.read_sql(sql, engine_stock_fundamentals)
    connection.close()
    context.stock_all['order_book_id'] = context.stock_all['code'].map(
        lambda x: x + '.XSHG' if x >= '600000' else x + '.XSHE')

    #remove the stock in blacklist
    for stock in stock_blackList:
        context.stock_all = context.stock_all[context.stock_all.order_book_id != stock]


def load_st_classified(context):
    context.st_classified = pd.read_csv('/Users/yanghui/Documents/tushare/StockFundamentals/ST_classified.csv',encoding='GBK')


def load_stock_fundamentals(context):
    stock_fundamentals_all = pd.DataFrame([])
    context.stock_list = list(set(context.stock_all.order_book_id))
    for order_book_id in context.stock_list:
        if order_book_id[7:4] == 'XSHG':
            filename = 'sh' + order_book_id [0:6]
        else:
            filename = 'sz' + order_book_id [0:6]
        filepath = '/Users/yanghui/Documents/trading-data@full/stock data/' + filename + '.csv'
        if os.path.exists(filepath):
            stock_fundamentals = pd.read_csv(filepath)
            stock_fundamentals = stock_fundamentals[(stock_fundamentals.date >= '2014-01-01') &
                                                    (stock_fundamentals.date <= '2016-05-30')]
            stock_fundamentals_all = stock_fundamentals_all.append(stock_fundamentals)
    stock_fundamentals_all['order_book_id'] = stock_fundamentals_all['code'].map(lambda x: x[2:8] + '.XSHG' if x[0:2] == 'sh' else x[2:8] + '.XSHE')
    context.fundamentals_all = stock_fundamentals_all

def load_trade_cal(context):
    """
    load the trade calendar
    """
    engine_stock_fundamentals = create_engine("mysql+mysqldb://root:good@localhost:3306/TUSHARE_STOCK_FUNDAMENTALS",
                                          encoding='utf-8', echo=False)
    connection = engine_stock_fundamentals.connect()
    sql = "select * from StockTradeCal"
    stock_trade_cal = pd.read_sql(sql, engine_stock_fundamentals)
    connection.close()
    context.trade_cal = stock_trade_cal


def get_prev_trade_date(context,date):
    """
    get previous trading date.
    """

    prev_date_df = context.trade_cal[context.trade_cal.calendarDate == date]
    return prev_date_df.iloc[0]['prevTradeDate']


def get_percentage(context,date,stk):
    """
    get the percentage of the stock

    """
    prev_date = get_prev_trade_date(context,date)

    this_date_df = context.fundamentals_all[(context.fundamentals_all.date == date) &
                                              (context.fundamentals_all.order_book_id == stk)
                                            ]
    prev_date_df = context.fundamentals_all[(context.fundamentals_all.date == prev_date) &
                                              (context.fundamentals_all.order_book_id == stk)
                                            ]
    if len(this_date_df) > 0 and len(prev_date_df) > 0:
        percentage = (this_date_df.iloc[0]['close'] - prev_date_df.iloc[0]['close'])/prev_date_df.iloc[0]['close']
        return percentage
    else:
        logger.info(stk + ' prev day/today is not trading')
        return 0



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

