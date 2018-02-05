"""

版本：v2.0
日期：2017.04.11
作者：Yang Hui
"""
from time import strftime

from rqalpha.core.strategy_context import RunInfo
from rqalpha.api import *

'''
============
关于本策略：
============
这个策略比较适合平衡市
策略逻辑： 选出市值最小市值股票，去除ST股票，成交量大于3000万，前一交易日涨跌幅在-5% - 9.9%之间，加入股票池并买入5只。
卖出条件：
不在选股范围的股票

'''

# 在这个方法中编写任何的初始化逻辑。context对象将会在你的算法策略的任何方法之间做传递。
def init(context):
    import os
    import sys
    strategy_file_path = '/Users/yanghui/PycharmProjects/quantest/my_strategy/'
    sys.path.append(os.path.realpath(os.path.dirname(strategy_file_path)))
    #context.run_info()
    from strategy_api import strategy_api
    context.api = strategy_api()

# before_trading此函数会在每天交易开始前被调用，当天只会被调用一次
def before_trading(context):
    #context.s1 = '000001.XSHG'
    #context.api.ipo_days(context.s1, context.now)
    context.api.stock_selection(context=context)

# 你选择的证券的数据更新将会触发此段逻辑，例如日或分钟历史数据切片或者是实时数据切片更新
def handle_bar(context, bar_dict):
    context.api.switch_portfolio(context=context, bar_dict=bar_dict)


"""
2017.04.11

v2.0
v2.0 初始版本，更多初始化参数配置，把常用功能打包成 local API
"""
