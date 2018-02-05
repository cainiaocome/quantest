from time import strftime, localtime

import itertools

import math
import talib
from rqalpha.api import *
import pandas as pd


class strategy_api(object):
    """
    ===================================
    策略开发API：
    ===================================
    '''第1部、选择标的'''
    #1.1 数据载入
    #1.2 基本面选股
    '''第2部、入场策略'''
    #2.1 大盘环境问题
        #？？？？
    #2.2 个股选择问题，最后还要过滤非跌停、上市天数、非停牌的标的（过滤st？）
        #2.2.1 备选中标的站上5日线
        #2.2.2 备选中标的站上10日线
        #2.2.2 所谓金叉，今天短均线大于长均线，上一个bar反之
        #整合各个子条件的交集
        #过滤上市时间、是否涨停、是否停牌等条件
    '''第3部、持仓组合的微调策略'''
    # 平均市值做微调
    '''第4部、出场策略'''
    '''第5部、闲置资金效率最大化'''
    '''第6部、风险控制'''
    '''第7部、备用组件'''
    #7.1 将his的非标DF进行转换，licco说现在不用转换了，我还是保留了：）
    #7.2 计算n日概率随机交易的概率收益率
    #7.3 多list获得并集
    #7.4 标的上市时间距离参照时间的自然日数量
    #7.5 判断当前标在可交易区间内（非涨跌停）
    """
    # -----------------------------------------------------------------------------------------------------------------#
    # 参数配置
    # -----------------------------------------------------------------------------------------------------------------#
    # 调仓频率，单位：日
    # parm_run_frequency = 'Daily'
    # if parm_run_frequency == 'Weekly':
    #    scheduler.run_weekly(stock_selection(context=context),tradingday=1, time_rule='before_trading')
    #    scheduler.run_weekly(switch_portfolio,tradingday=1, time_rule=market_open(minute=1))

    # 配置调仓时间（24小时分钟制）
    parm_adjust_position_hour = 14
    parm_adjust_position_minute = 50

    # 配置选股参数
    # 备选股票数目
    parm_pick_stk_count = 100
    # 买入股票数目
    parm_buyStkCount = 5

    # 是否根据PE选股
    parm_pick_by_pe = False
    # 如果根据PE选股，则配置最大和最小PE值
    if parm_pick_by_pe:
        parm_max_pe = 200
        parm_min_pe = 0

    # 是否根据EPS选股
    parm_pick_by_eps = False
    # 配置选股最小EPS值
    if parm_pick_by_eps:
        parm_min_eps = 0

    # 配置是否过滤创业板股票
    parm_filter_gem = True
    # 配置是否过滤黑名单股票，回测建议关闭，模拟运行时开启
    parm_blackList = []

    # 是否对股票评分
    parm_is_rank_stock = False
    if parm_is_rank_stock:
        # 参与评分的股票数目
        parm_rank_stock_count = 20

    # -----------------------------------------------------------------------------------------------------------------#
    # 数据初始化准备
    # -----------------------------------------------------------------------------------------------------------------#
    is_stock_basics_loaded = False
    is_stock_daily_loaded = False
    is_stock_daily_qfq_loaded = False
    stock_basics = pd.DataFrame([])
    stock_daily = pd.DataFrame([])
    stock_daily_qfq = pd.DataFrame([])
    position_maxvalue = pd.DataFrame()

    def load_stock_basics(self):
        """
        载入两市所有股票的基本面信息
        """
        if not self.is_stock_basics_loaded:
            print(strftime("%Y-%m-%d %H:%M:%S", localtime()) + ' Start to load_stock_basics...')
            file_path = '/Users/yanghui/Documents/SPSS modeler/复盘/'
            filename = 'stock_basics.xlsx'
            self.stock_basics = pd.read_excel(file_path + filename, encoding='GBK')
            self.stock_basics['code'] = self.stock_basics['code'].map(
                lambda x: str(x).zfill(6))
            self.stock_basics['order_book_id'] = self.stock_basics['code'].map(
                lambda x: str(x).zfill(6) + '.XSHG' if str(x).zfill(6) >= '600000' else str(x).zfill(6) + '.XSHE')
            self.is_stock_basics_loaded = True
            print(strftime("%Y-%m-%d %H:%M:%S", localtime()) + ' Successfully load_stock_basics!')
        return

    def load_stock_daily(self):
        """
        载入未复权的股价历史记录
        """
        if not self.is_stock_daily_loaded:
            print(strftime("%Y-%m-%d %H:%M:%S", localtime()) + ' Start to load_stock_daily...')
            stock_daily_all = pd.DataFrame([])
            self.load_stock_basics()
            stock_list = sorted(list(self.stock_basics.code))
            for stock in stock_list:
                try:
                    file_name = str(stock) + '.csv'
                    file_path = '/Users/yanghui/Documents/tushare/StockDaily/'
                    stock_daily = pd.read_csv(file_path + file_name)
                    stock_daily = stock_daily[(stock_daily.date >= '2017-01-01') &
                                              (stock_daily.date <= strftime("%Y-%m-%d", localtime()))]
                    stock_daily_all = stock_daily_all.append(stock_daily)
                    stock_daily_all['order_book_id'] = stock_daily_all['code'].map(
                        lambda x: str(int(x)).zfill(6) + '.XSHG' if str(int(x)).zfill(6) >= '600000' else str(
                            int(x)).zfill(
                            6) + '.XSHE')
                except:
                    print(strftime("%Y-%m-%d %H:%M:%S", localtime()) + ' load_stock_daily failed for stock: ' + str(
                        stock))
            self.stock_daily = stock_daily_all
            self.is_stock_daily_loaded = True
            print(strftime("%Y-%m-%d %H:%M:%S", localtime()) + ' Successfully load_stock_daily!')
        return

    def load_stock_daily_qfq(self):
        """
        载入前复权的股价历史记录
        """
        if not self.is_stock_daily_qfq_loaded:
            print(strftime("%Y-%m-%d %H:%M:%S", localtime()) + ' Start to load_stock_daily_qfq...')
            stock_daily_all = pd.DataFrame([])
            self.load_stock_basics()
            stock_list = sorted(list(self.stock_basics.code))
            for stock in stock_list:
                try:
                    file_name = str(stock) + '.csv'
                    file_path = '/Users/yanghui/Documents/tushare/StockDaily_qfq/'
                    stock_daily = pd.read_csv(file_path + file_name)
                    stock_daily = stock_daily[(stock_daily.date >= '2017-01-01') &
                                              (stock_daily.date <= strftime("%Y-%m-%d", localtime()))]
                    stock_daily_all = stock_daily_all.append(stock_daily)
                    stock_daily_all['order_book_id'] = stock_daily_all['code'].map(
                        lambda x: str(int(x)).zfill(6) + '.XSHG' if str(int(x)).zfill(6) >= '600000' else str(
                            int(x)).zfill(
                            6) + '.XSHE')
                except:
                    print(strftime("%Y-%m-%d %H:%M:%S", localtime()) + ' load_stock_daily_qfq failed for stock: ' + str(
                        stock))
            self.stock_daily_qfq = stock_daily_all
            self.is_stock_daily_qfq_loaded = True
            print(strftime("%Y-%m-%d %H:%M:%S", localtime()) + ' Successfully load_stock_daily_qfq!')
        return

    '''第1部、选择标的'''
    '''
    def choose_target(self, context):
        # 最小市值的100只标的
        df = get_fundamentals(
            query(fundamentals.eod_derivative_indicator.market_cap)
                .order_by(fundamentals.eod_derivative_indicator.market_cap.asc())
                .limit(context.choosenum)
        )
        context.stocks = [stock for stock in df][:100]
        return context.stocks
    '''

    '''第2部、入场策略'''

    def for_buy(self, context, bar_dict):
        to_buy = []
        for stock in context.universe:
            con1 = self.sma_cross(stock) == 'gold_cross'
            con2 = bar_dict[stock].is_trading
            con3 = self.is_limit_up(stock, bar_dict)
            #if con1 & con2 & (not con3):
            if con2 & (not con3):
                to_buy.append(stock)
        return to_buy

    # 2.1 大盘环境问题
    # 可增加外部数据

    # 2.2 个股选择问题，最后还要过滤非跌停、上市天数、非停牌的标的（st未过滤）

    # 2.2.2 所谓金叉(Golden Cross)，今天短均线大于长均线，上一个bar反之
    def sma_cross(self, stk):
        # 长短均线
        SHORTPERIOD = 5
        LONGPERIOD = 10
        cross = ' '
        prices = history_bars(stk, LONGPERIOD + 1, '1d', 'close')
        # 使用talib计算长短两根均线，均线以array的格式表达
        short_avg = talib.SMA(prices, SHORTPERIOD)
        long_avg = talib.SMA(prices, LONGPERIOD)
        # 死叉：如果短均线从上往下跌破长均线，也就是在目前的bar短线平均值低于长线平均值，而上一个bar的短线平均值高于长线平均值
        if short_avg[-1] - long_avg[-1] < 0 and short_avg[-2] - long_avg[-2] > 0:
            cross = 'dead_cross'
        # 金叉：如果短均线从下往上突破长均线，为入场信号
        if short_avg[-1] - long_avg[-1] > 0 and short_avg[-2] - long_avg[-2] < 0:
            cross = 'gold_cross'
        return cross

    def stock_selection(self, context):
        """
        '''第1部、选择标的'''
        选股函数
        """
        # 获取前一个交易日
        prev_calendar_date = get_previous_trading_date(context.now.date()).strftime("%Y-%m-%d")

        # 筛选价格小于5元的股票, 使用不复权价格
        self.load_stock_daily()
        # stock_daily_all = self.stock_daily[(self.stock_daily.date == prev_calendar_date) &
        #                                          (self.stock_daily.open < 5)
        #                                          ]
        stock_daily_all = self.stock_daily[(self.stock_daily.date == prev_calendar_date)]

        self.load_stock_daily_qfq()
        stock_daily_all_qfq = self.stock_daily_qfq[
            (self.stock_daily_qfq.date == prev_calendar_date)]
        # merge股票基本面信息以获得各个股票的总股本
        stock_daily_all = pd.merge(left=stock_daily_all, right=self.stock_basics, left_on=['order_book_id'],
                                   right_on=['order_book_id'], how='left')
        # merge前复权价格，并计算市值
        stock_daily_all = pd.merge(left=stock_daily_all, right=stock_daily_all_qfq, left_on=['order_book_id'],
                                   right_on=['order_book_id'], how='left', suffixes=('', '_qfq'))
        stock_daily_all['market_cap'] = stock_daily_all['totals'] * stock_daily_all['close_qfq']

        #筛选市值小于50亿的公司
        stock_daily_all = stock_daily_all[stock_daily_all.market_cap <= 50]

        # 以股票市值排序
        stock_daily_all = stock_daily_all.sort_values(by='market_cap', ascending=True)
        print(stock_daily_all)



        # 过滤st股票、过滤不能交易的股票、过滤上市小于30天的股票
        stock_list = list(stock_daily_all.order_book_id)
        for stk in stock_list:
            # 过滤st股票
            if is_st_stock(stk):
                stock_list.remove(stk)
            # 过滤不能交易的股票
            elif is_suspended(stk):
                stock_list.remove(stk)
            # 过滤上市小于30天的股票
            elif self.ipo_days(stk, context.now) <= 60:
                stock_list.remove(stk)
            # 过滤黑名单
            elif stk in self.parm_blackList:
                stock_list.remove(stk)

        # 更新股票池
        # update_universe(stock_list[0:self.parm_buyStkCount])
        update_universe(stock_list)
        return

    '''第3部、持仓组合的微调策略'''

    # 平均市值做微调
    def portfolio_rebalance(self, context, bar_dict):
        # mvalues = context.portfolio.market_value
        # avalues = context.portfolio.portfolio_value
        # per = mvalues / avalues
        hlist = []
        for stock in context.portfolio.positions:
            hlist.append([stock, bar_dict[stock].last * context.portfolio.positions[stock].quantity])

        if hlist:
            hlist = sorted(hlist, key=lambda x: x[1], reverse=True)
            temp = 0
            for li in hlist:
                temp += li[1]
            for li in hlist:
                if bar_dict[li[0]].is_trading:
                    order_target_value(li[0], temp / len(hlist))
        return

    def switch_portfolio(self, context, bar_dict):
        """
        根据股票列表换仓
        """
        sell_list = self.for_sell(context, bar_dict)
        # 卖出股票
        for stk in sell_list:
            order_target_percent(stk, 0)
        # 买入新股
        buy_list = self.for_buy(context, bar_dict)[0:self.parm_buyStkCount]
        for stk in buy_list:
            if len(context.portfolio.positions) < self.parm_buyStkCount:
                order_target_percent(stk, 1.0 / self.parm_buyStkCount)
        return

    '''第4部、出场策略'''

    # 死叉，并且可交易，没跌停
    def for_sell(self, context, bar_dict):
        to_sell = []
        for stock in context.portfolio.positions:
            #con1 = self.sma_cross(stock) == 'dead_cross'
            con1 = self.stop_loss_floor(context, stock)
            con2 = bar_dict[stock].is_trading
            con3 = self.is_limit_down(stock, bar_dict)
            if con1 & con2 & (not con3):
                to_sell.append(stock)
        return to_sell

    '''
    阶梯止损
    M= 初始止损比例
    X= 阶梯长度  
    Y= 阶梯变化率 （阶梯每改变一次， 止损线上涨的幅度）

    止损线改变次数=floor[log(周期内最高股价/买入价)/log(1+ X%)]
    止损价= M * [1+Y%] ^ 止损线改变次数

    if 现价< 止损价： 
    直接跌破止损价， 卖出止损。
    else：
    继续持有
    '''
    def stop_loss_floor(self, context, stock):
        #self.position_maxvalue = pd.DataFrame()
        initSLM = 0.9  # 初始止损比例 M
        step = 0.10  # 间隔 X
        increment = 0.09  # 止损增量  Y

        if stock not in self.position_maxvalue.columns:
            temp = pd.DataFrame({stock: [context.portfolio.positions[stock].bought_value, initSLM]})
            self.position_maxvalue = pd.concat([self.position_maxvalue, temp], axis=1, join='inner')
        print(self.position_maxvalue)

        market_value = context.portfolio.positions[stock].market_value  # 该股市场价值 单位（RMB）
        bought_value = context.portfolio.positions[stock].bought_value  # 该股初始价值 单位（RMB）
        stockdic = self.position_maxvalue[stock]
        maxvalue = stockdic[0]

        del self.position_maxvalue[stock]
        currSL = initSLM * (1 + increment) ** math.floor(
            (math.log(maxvalue / bought_value) / math.log(1 + step)))  # 阶梯止损算法

        temp = pd.DataFrame({str(stock): [max(maxvalue, market_value), currSL]})
        self.position_maxvalue = pd.concat([self.position_maxvalue, temp], axis=1, join='inner')  # 更新dataframe。

        print(str(stock) + '的成本为：' + str(bought_value) + ', 最高价值为：' + str(maxvalue) + '现价值为：' + str(market_value))
        print(str(stock) + '的现 止损价位为: ' + str(currSL))
        # logger.info ( type(market_value))
        # logger.info(type(ontext.maxvalue[stock].values)))
        if market_value < bought_value * currSL:
            return True
        else:
            return False



    '''第5部、闲置资金效率最大化'''

    def for_cash(self, context, bar_dict):
        cash = context.portfolio.cash
        # order_target_value('511880.XSHG',cash) 注释掉因为滑点太大，可以买一个货基，或者逆回购
        return

    '''第6部、风险控制'''

    def alert_risk(self, context, bar_dict):
        # 这里如果给出策略，要强制执行，注意在handle优先级高于所有
        pass

    '''第7部、备用组件'''

    # 7.1 将his的非标DF进行转换，licco说现在不用转换了，我还是保留了：）
    def trans(self, df):
        temp = pd.DataFrame()
        for col in df.index:
            temp[col] = df.T[col]
        return temp.T

    # 7.2 计算n日概率随机交易的概率收益率
    def rts_sj(self, df, n, m):
        dfp_pct = df.pct_change()

        def the_list(df, n, m):
            temp = []
            for i in range(n, n + m):
                temp.append(df.iloc[-i, :] + 1)
            return temp

        def from_list(self, num):
            result = []
            for i in range(1, num + 1):
                result.extend(list(itertools.combinations(self, i)))
            return result

        def rts_n(tu):
            sum0 = []
            for i in tu:
                temp = 1
                for z in i:
                    temp = temp * z
                temp = temp ** (1 / len(i))
                sum0.append(temp)
            sum1 = 0
            for i in sum0:
                sum1 = sum1 + i - 1
            return sum1 / len(sum0)

        return rts_n(from_list(the_list(dfp_pct, n, m), m))

    # 7.3 多list获得并集
    def jj_list(self, tar_list):
        temp = tar_list[0]
        for i in tar_list:
            temp = list(set(temp).intersection(set(i)))
        return temp

    # 7.4 标的上市时间距离参照时间的自然日数量
    def ipo_days(self, stock, today):
        market_date = instruments(stock).listed_date.replace(tzinfo=None)
        today = today.replace(tzinfo=None)
        return (today - market_date).days

    # 7.5 判断当前标在可交易区间内（非涨跌停）
    def is_limit_up(self, stock, bar_dict):
        yesterday = history_bars(stock, 1, '1d', 'close')[0]
        limit_up = round(1.10 * yesterday, 2)
        if bar_dict[stock].last >= limit_up:
            return True
        else:
            return False

    def is_limit_down(self, stock, bar_dict):
        yesterday = history_bars(stock, 1, '1d', 'close')[0]
        limit_down = round(0.90 * yesterday, 2)
        if bar_dict[stock].last <= limit_down:
            return True
        else:
            return False
