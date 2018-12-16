#encoding: UTF-8
from tushare import get_stock_basics, get_today_all, __version__

if __name__ == '__main__':
    """
    跌破净值分析
    """

    # 基本面数据
    basic = get_stock_basics()

    # 行情和市值数据
    hq = get_today_all()

    # 当前股价,如果停牌则设置当前价格为上一个交易日股价
    hq['trade'] = hq.apply(lambda x: x.settlement if x.trade == 0 else x.trade, axis=1)

    # 分别选取流通股本,总股本,每股公积金,每股收益
    basedata = basic[['outstanding', 'totals', 'reservedPerShare', 'esp', 'bvps']]

    # 选取股票代码,名称,当前价格,总市值,流通市值
    hqdata = hq[['code', 'name', 'trade', 'mktcap', 'nmc']]

    # 设置行情数据code为index列
    hqdata = hqdata.set_index('code')

    # 合并两个数据表
    data = basedata.merge(hqdata, left_index=True, right_index=True)

    # 将总市值和流通市值换成亿元单位
    data['mktcap'] = data['mktcap'] / 10000
    data['nmc'] = data['nmc'] / 10000

    # 净值大于股价
    res = data.bvps >= data.trade / 1.0

    # 总市值<100亿
    mktcap = data.mktcap <= 50


    # 取并集结果：
    allcrit = res & mktcap
    selected = data[allcrit]

    # 具有高送转预期股票的结果呈现：
    print(selected)
