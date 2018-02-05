from my_strategy.tushare_download.mysqlapi import MySQLApi

if __name__ == '__main__':
    """
    tushare_download data downloader to prepare the local data environment.
    requirement:
    MYSQL database installation is required in localhost
    trade_cal is downloaded from datayes (通联数据）
    so a free account of datayes is required to have your own token.
    """

    api = MySQLApi()

    ######################################
    # download the stock fundamental information
    ######################################
    #api.download_stock_basics() #download ok
    #api.download_trade_cal()  #download ok

    # TODO completed with 2016-02 duplicated, the data is not clean also from tushare_download, some records are duplicated
    #api.download_report_data(year_from=2016)


    #api.download_profit_data(year_from=2013) #TODO downloaded  but with duplicated records
    #api.download_operation_data(year_from=2013)  # completed
    #api.download_growth_data(year_from=2014) # completed
    #api.download_debtpaying_data(year_from=2013) # completed
    #api.download_cashflow_data(year_from=2013)

    ######################################
    # download the daily stock price
    ######################################
    api.download_stock_D1()
    api.download_stock_D1_qfq()
    #api.download_st_classified_CSV()
    #api.download_stock_basics_csv()
    #api.download_news()
    #api.download_index()
    #api.download_daily_tick(start='2016-06-01', end='2016-12-01')

    ######################################
    # download the ticker data
    # TODO: stock ticker will support later, the data is too huge.
    ######################################
    #api.download_stock_M1(start='2014-01-09',end='2014-01-09')
    #api.download_industry_classified()

    ######################################
    # MYSQLAPI will log the warnings during the download
    # and printed in the end of the downloader.
    ######################################
    #if api.warning_list is not None :
    #   print(api.warning_list)
