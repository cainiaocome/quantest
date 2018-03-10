#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
from datetime import *
from time import strftime, localtime, sleep
import pandas as pd

from tushare_api import tushare_api
from tushare_api_rsi import TushareApiRsi


if __name__ == '__main__':
    """
    tushare_download data downloader to prepare the local data environment.
    """
    today_ISO = datetime.today().date().isoformat()
    api = tushare_api()
    start = '2018-02-01'
    end = today_ISO
    # schedule = sched.scheduler(time.time, time.sleep)
    sched_Timer = '16:30'
    working_folder = '/Users/huiyang/Documents/'


    while True:
        now = strftime("%H:%M", localtime())

        # run below download steps in a perticular time only.
        if now == sched_Timer:
            ######################################
            # download today's stock price
            ######################################
            try:
                api.download_today_all()
                #api.downloadIndex(end=end)
                #api.download_hist_data(start=start, end=end)
                #api.calculate_today_all_with_percentage(start=start, end=end)
                #api.calculate_today_all_without_percentage(start=start, end=end)
            except:
                print('download_today_all failed!')
            try:
                api.download_industry_classified()
            except:
                print('download_industry_classified failed!')
            try:
                api.download_concept_classified()
            except:
                print('download_concept_classified failed!')
            try:
                api.download_area_classified()
            except:
                print('download_area_classified failed!')
            ######################################
            # download the stock fundamental information
            ######################################
            try:
                api.download_stock_basics()
            except:
                print('download_stock_basics failed!')
            try:
                api.download_report_data()
            except:
                print('download_report_data failed!')
            try:
                api.download_profit_data()
            except:
                print('download_profit_data failed!')
            try:
                api.download_operation_data()
            except:
                print('download_operation_data failed!')
            try:
                api.download_growth_data()
            except:
                print('download_growth_data failed!')
            try:
                api.download_debtpaying_data()
            except:
                print('download_debtpaying_data failed!')
            try:
                api.download_cashflow_data()
            except:
                print('download_cashflow_data failed!')
            try:
                api.download_stock_fundamentals(year=2017)
            except:
                print('download_stock_fundamentals failed!')
            try:
                api.format_stock_fundamentals(year=2017)
            except:
                print('format_stock_fundamentals failed!')
            try:
                api.merge_stock_fundamentals(year=2017)
            except:
                print('merge_stock_fundamentals failed!')
            #try:
            #    api.calculate_roe_pb()
            #except:
            #    print('calculate_roe_pb failed!')
            #try:
            #    TushareApiRsi().calculate_rsi()
            #    TushareApiRsi().calculateHindenburgOmen()
            #except:
            #    print('calculate_rsi failed!')
            ######################################
            # download the 投资参考数据
            ######################################
            try:
                api.download_share_profit_data(year='2016')
            except:
                print('download_share_profit_data failed!')
            try:
                api.download_forecast_data()
            except:
                print('download_forecast_data failed!')
            try:
                api.download_xsg_data()
            except:
                print('download_xsg_data failed!')
            try:
                api.download_fund_holdings()
            except:
                print('download_fund_holdings failed!')
            try:
                api.download_new_stocks()
            except:
                print('download_new_stocks failed!')
            try:
                api.download_ST_classified()
            except:
                print('download_ST_classified failed!')
            ######################################
            # refresh tushare daily stock data
            ######################################
            try:
                api.download_stock_D1()
                api.download_stock_D1_qfq()
            except:
                print('download_stock_D1 failed!')
            ######################################
            # update rqalpha data bundle
            ######################################
            try:
                os.system('rqalpha update_bundle')
            except:
                print('rqalpha update_bundle failed')
 
        # check file and run below download steps if today's file is not downloaded yet.
        if now >= sched_Timer:
            ##################################
            # check index file, 
            # if today's file is not downloaded yet. 
            # start the download
            ##################################
            filename = 'index_000001'
            index_000001 = pd.read_excel(io=working_folder + \
                    'SPSS modeler/复盘/' + filename + '.xlsx')
            filename = 'index_399001'
            index_399001 = pd.read_excel(io=working_folder + \
                    'SPSS modeler/复盘/' + filename + '.xlsx')
            filename = 'index_399006'
            index_399006 = pd.read_excel(io=working_folder + \
                    'SPSS modeler/复盘/' + filename + '.xlsx')

            if (index_000001.iloc[0, 0].isoformat() < today_ISO)    \
                or (index_399001.iloc[0, 0].isoformat() < today_ISO) \
                or (index_399006.iloc[0, 0].isoformat() < today_ISO):
                    try:
                        api.downloadIndex(end=end)
                    except:
                        print('downloadIndex failed')
            
            ##################################
            # check hist_data file, 
            # if today's file is not downloaded yet. 
            # start the download
            ##################################
            filename = 'hist_data'
            hist_data = pd.read_excel(io=working_folder + \
                    'SPSS modeler/复盘/' + filename + '.xlsx')
            if (hist_data.iloc[0, 0] < today_ISO):
                    try:
                        api.download_hist_data(start=start, end=end)
                    except:
                        print('download_hist_data failed')
            
            ##################################
            # check hist_data file, 
            # if hist_data file is available for today,   
            # start the calculation for today
            ##################################
            filename = 'hist_data'
            hist_data = pd.read_excel(io=working_folder + \
                    'SPSS modeler/复盘/' + filename + '.xlsx')
            filename = 'index_000001'
            index_000001 = pd.read_excel(io=working_folder + \
                    'SPSS modeler/复盘/' + filename + '.xlsx')
            filename = 'index_399001'
            index_399001 = pd.read_excel(io=working_folder + \
                    'SPSS modeler/复盘/' + filename + '.xlsx')
            filename = 'index_399006'
            index_399006 = pd.read_excel(io=working_folder + \
                    'SPSS modeler/复盘/' + filename + '.xlsx')
            if (index_000001.iloc[0, 0].isoformat() >= today_ISO)    \
                and (index_399001.iloc[0, 0].isoformat() >= today_ISO) \
                and (index_399006.iloc[0, 0].isoformat() >= today_ISO) \
                and (hist_data.iloc[0, 0] >= today_ISO):
                    try:
                        api.calculate_today_all_with_percentage(start=start, end=end)
                        api.calculate_today_all_without_percentage(start=start, end=end)
                        api.calculate_roe_pb()
                        TushareApiRsi().calculate_rsi()
                        TushareApiRsi().calculateHindenburgOmen()
                    except:
                        print('download_hist_data failed')

        ## sleep for 1 mins
        sleep(60)







