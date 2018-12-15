# -*- coding: utf-8 -*-
import os
import threading
from datetime import datetime, date
from time import sleep

import dateutil.relativedelta
import pandas as pd

from logger import Logger
from tushare_api import tushare_api
from tushare_api_rsi import TushareApiRsi

###################################################
# main stream - 
####################################################
# is_trading_day ->
# -> thread_01 -> thread_17 -> thread_18 -> thread_20 -> thread_21 -> thread_22
#                                               ^                        ^
#                                               |                        |
# -> thread_05 -> thread_06 -> thread_07---------                        |
#                                                                        |
# -> thread_16 -----------------------------------------------------------
####################################################
# none critical thread after @thread_22
# thread_02/thread_03/thread_04
# thread_19
###################################################


def is_trading_day(date):
    """

    """
    path = '/Users/yanghui/Documents/quantest/data_Shared/baoStock/'
    trading_days = pd.read_csv(path + "trade_dates.csv")
    if trading_days[(trading_days.calendar_date == date) & (trading_days.is_trading_day == 1)].empty:
        return False
    else:
        return True

def last_trading_day(date):
    """

    """
    path = '/Users/yanghui/Documents/quantest/data_Shared/baoStock/'
    trading_days = pd.read_csv(path + "trade_dates.csv")
    trading_days = trading_days[(trading_days.calendar_date <= date)  \
                                & (trading_days.is_trading_day == 1)]
    trading_days.sort_values(by='calendar_date', ascending=False, inplace=True)
    
    if not trading_days.empty:
        return trading_days.head(1).iloc[0,0]
    else:
        log.logger.info('cannot find the last trading date!')
        return date


#Critical thread - download_today_all
def thread_01(thread_01_event):
    log.logger.info('thread_01 start...')
    thread_complete = False
    api = tushare_api()
    end = today_ISO
    while not thread_complete:
        try:
            api.download_today_all(end=end)
        except Exception:
            log.logger.info('download_today_all failed...')

        working_folder = '/Users/yanghui/Documents/quantest/data_shared/tuShare/'
        filename = 'today_all'
        today_all = pd.read_excel(io=working_folder  + filename + '.xlsx')
        if today_all.iloc[0,15] >= today_ISO: # check the date_download
            thread_complete = True
        else:
            thread_complete = False
        sleep(60)

    thread_01_event.set()
    log.logger.info('thread_01 completed!')
    return

def thread_02(thread_02_event,thread_22_event):
    thread_22_event.wait()
    log.logger.info('thread_02 start...')
    thread_complete = False
    api = tushare_api()
    end = today_ISO
    while not thread_complete:
        try:
            api.download_industry_classified(end=end)
            thread_complete = True
        except Exception:
            log.logger.info('download_industry_classified failed...')
        sleep(600)

    thread_02_event.set()
    log.logger.info('thread_02 completed!')
    return

def thread_03(thread_03_event,thread_02_event):
    thread_02_event.wait()
    log.logger.info('thread_03 start...')
    thread_complete = False
    api = tushare_api()
    end = today_ISO
    while not thread_complete:
        try:
            api.download_concept_classified(end=end)
            thread_complete = True
        except Exception:
            log.logger.info('download_concept_classified failed...')

        sleep(600)
    
    thread_03_event.set()
    log.logger.info('thread_03 completed!')
    return

def thread_04(thread_04_event,thread_03_event):
    thread_03_event.wait()
    log.logger.info('thread_04 start...')
    thread_complete = False
    api = tushare_api()
    end = today_ISO
    while not thread_complete:
        try:
            api.download_area_classified(end=end)
            thread_complete = True
        except Exception:
            log.logger.info('download_area_classified failed...')
        sleep(600)

    thread_04_event.set()
    log.logger.info('thread_04 completed!')
    return

# critical thread - download_stock_basics
def thread_05(thread_05_event,thread_01_event):
    thread_01_event.wait()
    log.logger.info('thread_05 start...')
    thread_complete = False
    api = tushare_api()
    end = today_ISO
    while not thread_complete:
        try:
            api.download_stock_basics(end=end)
        except Exception:
            log.logger.info('download_stock_basics failed...')

        working_folder = '/Users/yanghui/Documents/quantest/data_shared/tuShare/'
        filename = 'stock_basics'
        stock_basics = pd.read_excel(io=working_folder  + filename + '.xlsx')
        if stock_basics.iloc[0,23] >= today_ISO: # check the date_download
            thread_complete = True
        else:
            thread_complete = False
        sleep(60)

    thread_05_event.set()
    log.logger.info('thread_05 completed!')
    return

def thread_06(thread_06_event, thread_05_event):
    thread_05_event.wait()
    log.logger.info('thread_06 start...')
    thread_complete = False
    api = tushare_api()
    while not thread_complete:
        try:
            api.download_stock_fundamentals(year=2017,end=2018)
            thread_complete = True
        except Exception:
            log.logger.info('download_stock_fundamentals failed...')
        sleep(60)

    thread_06_event.set()
    log.logger.info('thread_06 completed!')
    return

def thread_07(thread_07_event, thread_06_event):
    thread_06_event.wait()
    log.logger.info('thread_07 start...')
    thread_complete = False
    api = tushare_api()
    while not thread_complete:
        try:
            api.format_stock_fundamentals(year=2010,end=2018)
            api.merge_stock_fundamentals(year=2010,end=2018)
            thread_complete = True
        except Exception:
            log.logger.info('format_merge_fundamentals failed...')

    thread_07_event.set()
    log.logger.info('thread_07 completed!')
    return

def thread_16(thread_16_event, thread_07_event):
    thread_07_event.wait()
    log.logger.info('thread_16 start...')
    thread_complete = False
    api = tushare_api()
    end = today_ISO
    while not thread_complete:
        try:
            api.downloadIndex(end=end)
        except Exception:
            log.logger.info('downloadIndex failed...')

        working_folder = '/Users/yanghui/Documents/quantest/data_shared/tuShare/'
        filename = 'index_000001'
        index_000001 = pd.read_excel(io=working_folder  + filename + '.xlsx')
        filename = 'index_399001'
        index_399001 = pd.read_excel(io=working_folder  + filename + '.xlsx')
        filename = 'index_399006'
        index_399006 = pd.read_excel(io=working_folder  + filename + '.xlsx')

        # check the date_download
        if (index_000001.iloc[0,0].date().isoformat() >= today_ISO)    \
            and (index_399001.iloc[0,0].date().isoformat() >= today_ISO)   \
            and (index_399006.iloc[0,0].date().isoformat() >= today_ISO):
            thread_complete = True
        else:
            thread_complete = False
        sleep(60)

    thread_16_event.set()
    log.logger.info('thread_16 completed!')
    return

#critical thread - download_hist_data
def thread_17(thread_17_event, thread_16_event):
    #print(thread_01_event.is_set())
    thread_16_event.wait()
    log.logger.info('thread_17 start...')
    thread_complete = False
    api = tushare_api()
    start = (date.today() - dateutil.relativedelta.relativedelta(days=30)).isoformat()
    end = today_ISO

    while not thread_complete:
        try:
            api.download_hist_data(start=start, end=end)
        except Exception:
            log.logger.info('download_hist_data failed...')

        working_folder = '/Users/yanghui/Documents/quantest/data_shared/tuShare/'
        filename = 'hist_data'
        hist_data = pd.read_excel(io=working_folder  + filename + '.xlsx')
        if hist_data.iloc[0,0] >= today_ISO: # check the date field
            thread_complete = True
        else:
            thread_complete = False
        
        sleep(60)

    thread_17_event.set()
    log.logger.info('thread_17 completed!')
    return

def thread_18(thread_18_event, thread_01_event, thread_17_event):
    thread_01_event.wait()
    thread_17_event.wait()
    log.logger.info('thread_18 start...')
    thread_complete = False
    api = tushare_api()
    start = (date.today() - dateutil.relativedelta.relativedelta(days=30)).isoformat()
    end = today_ISO

    while not thread_complete:
        try:
            api.calculate_today_all_with_percentage(start=start, end=end)
            thread_complete = True
        except Exception:
            log.logger.info('calculate_today_all_with_percentage failed...')
        sleep(60)

    thread_18_event.set()
    log.logger.info('thread_18 completed!')
    return

def thread_19(thread_19_event, thread_01_event, thread_17_event):
    thread_01_event.wait()
    thread_17_event.wait()
    log.logger.info('thread_19 start...')
    thread_complete = False
    api = tushare_api()
    start = (date.today() - dateutil.relativedelta.relativedelta(days=30)).isoformat()
    end = today_ISO

    while not thread_complete:
        try:
            api.calculate_today_all_without_percentage(start=start, end=end)
            thread_complete = True
        except Exception:
            log.logger.info('calculate_today_all_without_percentage failed...')
        sleep(60)

    thread_19_event.set()
    log.logger.info('thread_19 completed!')
    return

# waiting for thread_07, need more testing, 暂时拿掉07的dependency
#def thread_20(thread_20_event, thread_18_event, thread_05_event, thread_07_event):
def thread_20(thread_20_event, thread_18_event, thread_07_event):
    thread_18_event.wait()
    #thread_05_event.wait()
    thread_07_event.wait()
    log.logger.info('thread_20 start...')
    thread_complete = False
    api = tushare_api()
    while not thread_complete:
        try:
            api.calculate_roe_pb()
            thread_complete = True
        except Exception:
            log.logger.info('calculate_roe_pb failed...')
        sleep(60)

    thread_20_event.set()
    log.logger.info('thread_20 completed!')
    return

def thread_21(thread_21_event, thread_20_event, thread_17_event):
    thread_20_event.wait()
    thread_17_event.wait()
    log.logger.info('thread_21 start...')
    thread_complete = False
    while not thread_complete:
        try:
            TushareApiRsi().calculate_rsi()
            thread_complete = True
        except Exception:
            log.logger.info('calculate_rsi failed...')
        sleep(60)

    thread_21_event.set()
    log.logger.info('thread_21 completed!')
    return

def thread_22(thread_22_event, thread_21_event, thread_17_event, thread_16_event):
    thread_21_event.wait()
    thread_17_event.wait()
    log.logger.info('thread_22 start...')
    thread_complete = False
    while not thread_complete:
        try:
            TushareApiRsi().calculateHindenburgOmen(end=today_ISO)
            thread_complete = True
        except Exception:
            log.logger.info('calculateHindenburgOmen failed...')
        sleep(60)

    thread_22_event.set()
    log.logger.info('thread_22 completed!')
    return


if __name__ == '__main__':

    log = Logger(level='debug')
    log.logger.info('tushare_auto_downloader_v2.1 start...')
    today_ISO = datetime.today().date().isoformat()
    if not is_trading_day(date=today_ISO):
        today_ISO = last_trading_day(date=today_ISO)
    
    thread_01_event = threading.Event()
    thread_02_event = threading.Event()
    thread_03_event = threading.Event()
    thread_04_event = threading.Event()
    thread_05_event = threading.Event()
    thread_06_event = threading.Event()
    thread_07_event = threading.Event()
    thread_08_event = threading.Event()
    thread_09_event = threading.Event()
    thread_10_event = threading.Event()
    thread_11_event = threading.Event()
    thread_12_event = threading.Event()
    thread_13_event = threading.Event()
    thread_14_event = threading.Event()
    thread_15_event = threading.Event()
    thread_16_event = threading.Event()
    thread_17_event = threading.Event()
    thread_18_event = threading.Event()
    thread_19_event = threading.Event()
    thread_20_event = threading.Event()
    thread_21_event = threading.Event()
    thread_22_event = threading.Event()



    #if is_trading_day(date=today_ISO):
    threads = []

    # thread_01
    threads.append(threading.Thread(target=thread_01, args=(thread_01_event,)))
    ################################
    # non-critical thread
    ################################   
    # thread_02
    threads.append(threading.Thread(target=thread_02, args=(thread_02_event,thread_22_event,)))
    ################################
    # non-critical thread
    ################################   
    # thread_03
    threads.append(threading.Thread(target=thread_03, args=(thread_03_event,thread_02_event,)))
    ################################
    # non-critical thread
    ################################   
    # thread_04
    threads.append(threading.Thread(target=thread_04, args=(thread_04_event,thread_03_event,)))
    # thread_05
    threads.append(threading.Thread(target=thread_05, args=(thread_05_event,thread_01_event,)))
    # thread_06
    threads.append(threading.Thread(target=thread_06, args=(thread_06_event,thread_05_event,)))
    # thread_07
    threads.append(threading.Thread(target=thread_07, args=(thread_07_event,thread_06_event,)))
    '''
    # thread_08
    threads.append(threading.Thread(target=thread_08, args=(thread_08_event,)))
    # thread_09
    threads.append(threading.Thread(target=thread_09, args=(thread_09_event,)))
    # thread_10
    threads.append(threading.Thread(target=thread_10, args=(thread_10_event,)))
    # thread_11
    threads.append(threading.Thread(target=thread_11, args=(thread_11_event,)))
    # thread_12
    threads.append(threading.Thread(target=thread_12, args=(thread_12_event,)))
    # thread_13
    threads.append(threading.Thread(target=thread_13, args=(thread_13_event,)))
    # thread_14
    threads.append(threading.Thread(target=thread_14, args=(thread_14_event,)))
    # thread_15
    threads.append(threading.Thread(target=thread_15, args=(thread_15_event,)))
    '''
    # thread_16
    threads.append(threading.Thread(target=thread_16, args=(thread_16_event,thread_07_event,)))
    # thread_17
    threads.append(threading.Thread(target=thread_17, args=(thread_17_event,thread_16_event,)))
    # thread_18
    threads.append(threading.Thread(target=thread_18, args=(thread_18_event,thread_01_event,thread_17_event,)))
    # thread_19
    threads.append(threading.Thread(target=thread_19, args=(thread_19_event,thread_01_event,thread_17_event,)))
    # thread_20
    threads.append(threading.Thread(target=thread_20, args=(thread_20_event,thread_18_event,thread_07_event,)))
    # thread_21
    threads.append(threading.Thread(target=thread_21, args=(thread_21_event,thread_20_event,thread_17_event,)))
    # thread_22
    threads.append(threading.Thread(target=thread_22, args=(thread_22_event,thread_21_event,thread_17_event,thread_16_event,)))
    
    for t in threads:
        t.setDaemon(True)
        t.start()

    #等待所有thread结束
    for t in threads:
        t.join()
    log.logger.info('tushare_auto_downloader_v2.1 end...')

    """
        tushare_download data downloader to prepare the local data environment.
        flow:
                +--------------------------------------------------------+
                |                                                        | 
                v                                                        |
        +-------------------+                                           +-----------+
        | is_trading_day    | ----------------------------------------->| quit()    |
        |  (main thread)    |                                           +-----------+
        +-------------------+                                           
            True |
                |
                |
                |
                |
                |   >= @16:30   +---------------------+        +---------------+
                | ------------- | download_today_all  | <----> |  sleep(60)    |
                |  (thread 01)  +---------------------+        +---------------+   
                |
                |
                |   >= @16:30   +-------------------------------+        +---------------+
                | ------------- | download_industry_classified  | <----> |  sleep(60)    |
                |  (thread 02)  +-------------------------------+        +---------------+   
                |
                |
                |   >= @16:30   +-------------------------------+        +---------------+
                | ------------- | download_concept_classified   | <----> |  sleep(60)    |
                |  (thread 03)  +-------------------------------+        +---------------+   
                |
                |
                |   >= @16:30   +-------------------------------+        +---------------+
                | ------------- | download_area_classified      | <----> |  sleep(60)    |
                |  (thread 04)  +-------------------------------+        +---------------+   
                |
                |
                |   >= @16:30   +-------------------------------+        +---------------+
                | ------------- | download_stock_basics         | <----> |  sleep(60)    |
                |  (thread 05)  +-------------------------------+        +---------------+   
                |
                |
                |   >= @16:30   +-------------------------------+        +---------------+
                | ------------- | download_stock_fundamentals   | <----> |  sleep(60)    |
                |  (thread 06)  +-------------------------------+        +---------------+   
                |
                |                @download_stock_fundamentals
                |   >= @16:30   +-------------------------------+        +---------------+
                | ------------- | format_merge_fundamentals     | <----> |  sleep(60)    |
                |  (thread 07)  +-------------------------------+        +---------------+   
                |
                |
                |   >= @16:30   +-------------------------------+        +---------------+
                | ------------- | download_share_profit_data    | <----> |  sleep(60)    |
                |  (thread 08)  +-------------------------------+        +---------------+   
                |
                |
                |   >= @16:30   +-------------------------------+        +---------------+
                | ------------- | download_forecast_data        | <----> |  sleep(60)    |
                |  (thread 09)  +-------------------------------+        +---------------+   
                |
                |
                |   >= @16:30   +-------------------------------+        +---------------+
                | ------------- | download_xsg_data             | <----> |  sleep(60)    |
                |  (thread 10)  +-------------------------------+        +---------------+   
                |
                |
                |   >= @16:30   +-------------------------------+        +---------------+
                | ------------- | download_fund_holdings        | <----> |  sleep(60)    |
                |  (thread 11)  +-------------------------------+        +---------------+   
                |
                |
                |   >= @16:30   +-------------------------------+        +---------------+
                | ------------- | download_new_stocks           | <----> |  sleep(60)    |
                |  (thread 12)  +-------------------------------+        +---------------+   
                |
                |
                |   >= @16:30   +-------------------------------+        +---------------+
                | ------------- | download_ST_classified        | <----> |  sleep(60)    |
                |  (thread 13)  +-------------------------------+        +---------------+   
                |
                |
                |   >= @16:30   +-------------------------------+        +---------------+
                | ------------- | download_stock_W1_qfq         | <----> |  sleep(60)    |
                |  (thread 14)  +-------------------------------+        +---------------+   
                |
                |
                |   >= @16:30   +-------------------------------+        +---------------+
                | ------------- | download_stock_D1_qfq         | <----> |  sleep(60)    |
                |  (thread 15)  +-------------------------------+        +---------------+   
                |
                |
                |   >= @16:30   +-------------------------------+        +---------------+
                | ------------- | downloadIndex                 | <----> |  sleep(60)    |
                |  (thread 16)  +-------------------------------+        +---------------+   
                |
                |                @download_today_all
                |   >= @16:30   +-------------------------------+        +---------------+
                | ------------- | download_hist_data            | <----> |  sleep(60)    |
                |  (thread 17)  +-------------------------------+        +---------------+   
                |
                |                @downloadIndex
                |   >= @16:30   +--------------------------------------+        +---------------+
                | ------------- | calculate_today_all_with_percentage  | <----> |  sleep(60)    |
                |  (thread 18)  +--------------------------------------+        +---------------+   
                |
                |
                |
                |                @downloadIndex
                |   >= @16:30   +-----------------------------------------+        +---------------+
                | ------------- | calculate_today_all_without_percentage  | <----> |  sleep(60)    |
                |  (thread 19)  +-----------------------------------------+        +---------------+   
                |
                |                @downloadIndex
                |   >= @16:30   +-------------------------------+        +---------------+
                | ------------- | calculate_roe_pb              | <----> |  sleep(60)    |
                |  (thread 20)  +-------------------------------+        +---------------+   
                |
                |
                |
                |                @downloadIndex
                |   >= @16:30   +-------------------------------+        +---------------+
                | ------------- | calculate_rsi                 | <----> |  sleep(60)    |
                |  (thread 21)  +-------------------------------+        +---------------+   
                |
                |
                |                @downloadIndex
                |   >= @16:30   +-------------------------------+        +---------------+
                | ------------- | calculateHindenburgOmen       | <----> |  sleep(60)    |
                |  (thread 22)  +-------------------------------+        +---------------+   
                |
                |
                |
                |
                |
                |
                |
                |
                |
                |
                |

        """
