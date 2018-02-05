"""
统计过去一个月内某板块股票的价格和成交量，并据此计算得分。
如果价格上升同时成交量上升，那么+2分；如果价格上升同时成交量下降，那么+1分；
如果价格下降同时成交量上升，那么-1分；如果价格下降同时成交量下降，那么-2分。
计算过去一个月内的总分，从大到小排名，选出最高的10个股票，每月调仓。
同时加入止损，没月初选股时，如果大盘之前一周内下跌8%则空仓。投资组合一个月内累计下跌5%则平仓。
https://www.ricequant.com/api/python/chn#other-methods-sector，主要是传入给sector的参数变化一下即可
"""
#TODO: WIP


# 可以自己import我们平台支持的第三方python模块，比如pandas、numpy等。
import math
import numpy as np
import pandas as pd
import talib
from rqalpha.api import sector, update_universe, scheduler, history_bars, order_target_percent, order_value, \
    order_target_value

# 在这个方法中编写任何的初始化逻辑。context对象将会在你的算法策略的任何方法之间做传递。



def init(context):
    context.number = 10
    context.period = 20
    context.SMAPERIOD = 5
    context.marketval = context.portfolio.market_value
    context.stocks = sector('原材料')
    update_universe(context.stocks)
    scheduler.run_monthly(get_head, monthday=1)
    scheduler.run_monthly(position, monthday=1)
    scheduler.run_daily(stoploss)


def get_head(context, bar_dict):
    prices = history_bars(bar_dict, context.period + 1, '1d', 'close')
    b_prices = history_bars('000002.XSHE', 6, '1d', 'close')
    volumes = history_bars('000002.XSHE', context.period + 1, '1d', 'volume')
    score = {}
    for stock in prices.columns:
        p = prices[stock]
        v = volumes[stock]
        temp = 0
        for i in list(range(1, context.period)):
            if p[i] > p[i - 1]:
                if v[i] > v[i - 1]:
                    temp = temp + 2
                else:
                    temp = temp + 1
            else:
                if v[i] < v[i - 1]:
                    temp = temp - 1
                else:
                    temp = temp - 2
        score[stock] = temp
    s = pd.Series(score, name='scores')
    s.sort(ascending=False)
    context.to_buy = s.index[0:context.number]
    if b_prices[0] / b_prices[4] <= 0.92:
        context.to_buy = []


def position(context, bar_dict):
    stocks = set(context.to_buy)
    holdings = set(get_holdings(context))
    to_buy = stocks - holdings
    holdings = set(get_holdings(context))
    to_sell = holdings - stocks
    for stock in to_sell:
        if bar_dict[stock].is_trading:
            order_target_percent(stock, 0)
    to_buy = get_trading_stocks(to_buy, context, bar_dict)
    cash = context.portfolio.cash
    average_value = 0
    if len(to_buy) > 0:
        average_value = 0.98 * cash / len(to_buy)
    for stock in to_buy:
        if bar_dict[stock].is_trading:
            order_value(stock, average_value)
    context.marketval = context.portfolio.market_value


def get_trading_stocks(to_buy, context, bar_dict):
    trading_stocks = []
    for stock in to_buy:
        if bar_dict[stock].is_trading:
            trading_stocks.append(stock)
    return trading_stocks


def get_holdings(context):
    positions = context.portfolio.positions

    holdings = []
    for position in positions:
        if positions[position].quantity > 0:
            holdings.append(position)
    return holdings


def stoploss(context, bar_dict):
    if context.portfolio.market_value < context.marketval * 0.95:
        for stock in context.portfolio.positions:
            if bar_dict[stock].is_trading:
                order_target_value(stock, 0)