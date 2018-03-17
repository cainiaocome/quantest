# -*- coding: utf-8 -*-
import os
from datetime import *
from time import strftime, localtime, sleep
import pandas as pd
import dateutil.relativedelta
import sys,os
import numpy as np  

def color_win_loss(val):
    """
    Takes a scalar and returns a string with
    the css property `'color: red'` for negative
    strings, black otherwise.
    """
    if val < '0':
        color = 'green'
    if val > '0':    
        color = 'red'
    return 'color: %s' % color

def highlight_columns(data):
    '''
    highlight the DataFrame
    '''
    return ['background-color: yellow' for v in data]

if __name__ == '__main__':
    """
    update portfolio to the latest status
    """
    working_folder = '/Users/huiyang/Documents/'
    today_ISO = datetime.today().date().isoformat()
    #today_ISO = '2018-03-14' #for testing purpose
    #loading files
    filename = 'portfolio'
    portfolio = pd.read_excel(sys.path[0] + '/' + filename + '.xlsx')
    portfolio.index = portfolio.index.map(lambda x: str(x).zfill(6))
    filename = 'today_all'
    today_all = pd.read_excel(io=working_folder + 'SPSS modeler/复盘/' + filename + '.xlsx')
    today_all['code'] = today_all['code'].map(lambda x: str(x).zfill(6))
    filename = 'hist_data'
    hist_data = pd.read_excel(io=working_folder + \
                'SPSS modeler/复盘/' + filename + '.xlsx')
    hist_data['code'] = hist_data['code'].map(lambda x: str(x).zfill(6))
    filename = 'hist_data_weekly_qfq'
    hist_data_weekly_qfq = pd.read_excel(io=working_folder + \
                'SPSS modeler/复盘/' + filename + '.xlsx')
    hist_data_weekly_qfq['code'] = hist_data_weekly_qfq['code'].map(lambda x: str(x).zfill(6))
    hist_data_weekly_qfq.sort_values(by='date', ascending=False, inplace=True)

    # filter those already closed, merge back after the process below
    portfolio_closed = portfolio[portfolio.price_close > 0]
    portfolio_open = portfolio[portfolio.isnull().price_close]

    # update the portfolio file
    if (hist_data.iloc[0, 0] >= today_ISO):
        for code in portfolio_open.index:
            #hist_data = hist_data[hist_data.code == code]
            hist_data_stock = hist_data[(hist_data.code == code) & (hist_data.date == today_ISO)]
            today_all_stock = today_all[(today_all.code == code)]
            
            # generate the 'weekly_ATR'
            hist_data_weekly_qfq_stock = hist_data_weekly_qfq[(hist_data_weekly_qfq.code == code)].head(5)
            hist_data_weekly_qfq_stock['weekly_ATR'] = 0
            if len(hist_data_weekly_qfq_stock) >= 2:
                i = 1
                while i + 1 <= len(hist_data_weekly_qfq_stock):
                    hist_data_weekly_qfq_stock.iloc[i, 7] = (hist_data_weekly_qfq_stock.iloc[i, 3] - hist_data_weekly_qfq_stock.iloc[i, 4])/hist_data_weekly_qfq_stock.iloc[i - 1, 2]
                    i = i + 1
            hist_data_weekly_qfq_stock = hist_data_weekly_qfq_stock[(hist_data_weekly_qfq_stock.weekly_ATR > 0)]
            weekly_ATR = hist_data_weekly_qfq_stock['weekly_ATR'].mean()

            # compose update fields - weekly_ATR
            portfolio_open.loc[code, 'weekly_ATR'] = str(round((100 * weekly_ATR), 3)) + '%'

            # compose update fields - name
            portfolio_open.loc[code, 'name'] = today_all_stock.iloc[0, 1]
                        
            # compose update fields - price_current
            if not hist_data_stock.empty:
                portfolio_open.loc[code, 'price_current'] = hist_data_stock.iloc[0, 1]

            # compose update fields - price_highest
            if not hist_data_stock.empty:
                if portfolio_open.isnull().loc[code, 'price_highest']:
                    portfolio_open.loc[code, 'price_highest'] = hist_data_stock.iloc[0, 3]
                else:
                    if hist_data_stock.iloc[0, 3] > portfolio_open.loc[code, 'price_highest']:
                        portfolio_open.loc[code, 'price_highest'] = hist_data_stock.iloc[0, 3]
            
            # compose update fields - price_stoploss
            price_stoploss = portfolio_open.loc[code, 'price_highest'] - (portfolio_open.loc[code, 'price_highest'] * weekly_ATR)
            portfolio_open.loc[code, 'price_stoploss'] = round(price_stoploss, 3)

            # compose update fields - win(%)
            if portfolio_open.isnull().loc[code, 'price_close']:
                win = (portfolio_open.loc[code, 'price_current'] - portfolio_open.loc[code, 'price_open']) * portfolio_open.loc[code, 'amount_open']
                win_percentage = 100 * (portfolio_open.loc[code, 'price_current'] - portfolio_open.loc[code, 'price_open'])/portfolio_open.loc[code, 'price_open']
            else:
                win = (portfolio_open.loc[code, 'price_close'] - portfolio_open.loc[code, 'price_open']) * portfolio_open.loc[code, 'amount_open']
                win_percentage = 100 * (portfolio_open.loc[code, 'price_close'] - portfolio_open.loc[code, 'price_open'])/portfolio_open.loc[code, 'price_open']               
            portfolio_open.loc[code, 'win'] = round(win, 3)
            portfolio_open.loc[code, 'win(%)'] = str(round(win_percentage, 3)) + '%'

            # compose update fields - last_update_date
            portfolio_open.loc[code, 'last_update_date'] = today_ISO
            
    else:
        print('hist_data is not the latest')

    #portfolio_open.style.applymap(color_win_loss, subset=['win(%)']) \
    #    .apply(highlight_columns, subset=['name', 'price_current', 'price_highest', 'win(%)', 'last_update_date'])
    #filename = 'portfolio_open'
    #portfolio.to_excel(sys.path[0] + '/' + filename + '.xlsx', engine='openpyxl')
    portfolio = portfolio_closed.append(portfolio_open)
    #print(portfolio)
    filename = 'portfolio'
    portfolio.to_excel(sys.path[0] + '/' + filename + '.xlsx', encoding='GBK')