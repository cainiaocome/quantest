from tushare_api import tushare_api
from datetime import *
import os

if __name__ == '__main__':
    """
    tushare_download data downloader to prepare the local data environment.
    """
    today_ISO = datetime.today().date().isoformat()

    api = tushare_api()
    start = '2018-05-15'
    end = today_ISO
    #end = '2017-03-24'
    ######################################
    # download today's stock price
    ######################################
    #api.download_today_all()
    #api.downloadIndex(end=end)
    #api.download_hist_data(start=start, end=end)
    #try:
    #    os.system('python3 /Users/huiyang/Documents/quantest/risk_management/update_portfolio_v1.0.py')
    #except:
    #    print('update_portfolio_v1.0.py failed')
    api.calculate_today_all_with_percentage(start=start, end=end)
    api.calculate_today_all_without_percentage(start=start, end=end)
    #api.download_industry_classified()
    #api.download_concept_classified()
    #api.download_area_classified()


    ######################################
    # download the stock fundamental information
    ######################################
    #api.download_stock_basics()
    #try:
    #    api.download_report_data()
    #except:
    #    print('download_report_data failed!')
    #api.download_profit_data()
    #api.download_operation_data()
    #api.download_growth_data()
    #api.download_debtpaying_data()
    #api.download_cashflow_data()
    #api.download_stock_fundamentals(year=2017)
    #api.format_stock_fundamentals()
    #api.merge_stock_fundamentals(year=2017)
    #api.calculate_roe_pb()

    ######################################
    # download the 投资参考数据
    ######################################
    #api.download_share_profit_data(year='2016')
    #api.download_forecast_data()
    #api.download_xsg_data()
    #api.download_fund_holdings()
    #api.download_new_stocks()
    #api.download_ST_classified()

    ######################################
    # refresh daily stock data
    ######################################
    #api.download_stock_D1()
    #api.download_stock_D1_qfq()
    #api.download_stock_W1_qfq()

    ######################################
    # update rqalpha data bundle
    ######################################
    #os.system('rqalpha update_bundle')


