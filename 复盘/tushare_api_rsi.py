# encoding: UTF-8
import pandas as pd
import talib
import numpy as np  
import math  
from datetime import *
import tushare as ts
import sys,os
#from astropy.units import Ybarn  


###############
################

class TushareApiRsi():
    """
    API for RSI calculation
    """
    working_folder = '/Users/huiyang/Documents/'
    def calculate_rsi(self):
        """
        API for RSI calculation
        """
        print('start calculate the rsi...')
        # read file - today_all_roe_pb
        filename = 'today_all_roe_pb'
        today_all_roe_pb = pd.read_excel(io=self.working_folder + \
         'SPSS modeler/复盘/' + filename + '.xlsx')
        today_all_roe_pb['code'] = today_all_roe_pb['code'].map(lambda x: str(x).zfill(6))
        today_all_roe_pb.set_index(keys=['code'], inplace=True, drop=False)

        # read file - hist_data with at least 14 biz days
        filename = 'hist_data'
        hist_data = pd.read_excel(io=self.working_folder + 'SPSS modeler/复盘/' + filename + '.xlsx')
        hist_data['code'] = hist_data['code'].map(lambda x: str(x).zfill(6))
        hist_data.sort_values(by='date', ascending=True, inplace=True)

        # get last n days of prices.
        total = 0
        for stock in today_all_roe_pb.index:
            # Calculate rsi
            total = total + 1
            hist_data_stock = hist_data[hist_data.code == stock]
            # Calculate rsi for 14 biz days
            timeperiod = 14
            field_name = 'rsi_' + str(timeperiod) + 'days'
            today_all_roe_pb.loc[stock, field_name] = 50
            if not hist_data_stock.empty:
                close = hist_data_stock['close'].values
                stock_rsi = talib.RSI(close, timeperiod)[-1]
                today_all_roe_pb.loc[stock, field_name] = stock_rsi

            # Calculate rsi for 10 biz days
            timeperiod = 10
            field_name = 'rsi_' + str(timeperiod) + 'days'
            today_all_roe_pb.loc[stock, field_name] = 50
            if not hist_data_stock.empty:
                close = hist_data_stock['close'].values
                stock_rsi = talib.RSI(close, timeperiod)[-1]
                today_all_roe_pb.loc[stock, field_name] = stock_rsi

            # Calculate rsi for 5 biz days
            timeperiod = 5
            field_name = 'rsi_' + str(timeperiod) + 'days'
            today_all_roe_pb.loc[stock, field_name] = 50
            if not hist_data_stock.empty:
                close = hist_data_stock['close'].values
                stock_rsi = talib.RSI(close, timeperiod)[-1]
                today_all_roe_pb.loc[stock, field_name] = stock_rsi

        # save result
        today_all_roe_pb.sort_values(by=['rsi_5days','rsi_10days','rsi_14days'], ascending=False, inplace=True)
        filename = 'today_all_roe_pb_rsi'
        today_all_roe_pb.to_excel(self.working_folder + \
        'SPSS modeler/复盘/' + filename + '.xlsx', encoding='GBK')
        print('calculate the rsi successful ' + str(total))
        return

    def computeCorrelation(self, X, Y):  
        xBar = np.mean(X)  
        yBar = np.mean(Y) 
        SSR = 0  
        varX = 0  
        varY = 0  
        for i in range(0 , len(X)):  
            diffXXBar = X[i] - xBar  
            diffYYBar = Y[i] - yBar  
            SSR += (diffXXBar * diffYYBar) 
            varX += diffXXBar**2  
            varY += diffYYBar**2  
        SST = math.sqrt(varX * varY)  
        return SSR / SST  

    def calculateHindenburgOmen(self, start='2018-01-01', timeperiod=30):
        print('start calculate the Hindenburg Omen...')
        today_ISO = datetime.today().date().isoformat()
        # read file - today_all_roe_pb_rsi
        filename = 'today_all_roe_pb_rsi'
        today_all_roe_pb = pd.read_excel(io=self.working_folder + \
         'SPSS modeler/复盘/' + filename + '.xlsx')
        today_all_roe_pb['code'] = today_all_roe_pb['code'].map(lambda x: str(x).zfill(6))
        today_all_roe_pb.set_index(keys=['code'], inplace=True, drop=False)

        # read file - hist_data with at least 30 biz days
        filename = 'hist_data'
        hist_data = pd.read_excel(io=self.working_folder + 'SPSS modeler/复盘/' + filename + '.xlsx')
        hist_data['code'] = hist_data['code'].map(lambda x: str(x).zfill(6))
        hist_data.sort_values(by='date', ascending=False, inplace=True)

        # read index
        filename = 'index_000001'
        index_000001 = pd.read_excel(io=self.working_folder + \
         'SPSS modeler/复盘/' + filename + '.xlsx')
        index_000001.set_index(keys=['date'], inplace=True, drop=True)
        filename = 'index_399001'
        index_399001 = pd.read_excel(io=self.working_folder + \
         'SPSS modeler/复盘/' + filename + '.xlsx')
        index_399001.set_index(keys=['date'], inplace=True, drop=True)
        filename = 'index_399006'
        index_399006 = pd.read_excel(io=self.working_folder + \
         'SPSS modeler/复盘/' + filename + '.xlsx')
        index_399006.set_index(keys=['date'], inplace=True, drop=True)

        # get last n days of prices.
        total = 0
        for stock in today_all_roe_pb.index:
            # Calculate R_square
            #print('Now calculating R_square for stock: ' + str(stock))
            total = total + 1
            hist_data_stock = hist_data[hist_data.code == stock].head(timeperiod)
            hist_data_stock.set_index(keys=['date'], inplace=True, drop=False)

            # Calculate R_square for 30 biz days
            field_name = 'R_square_' + str(timeperiod) + 'days'
            if stock >= '600001':
                index_000001_stock = pd.merge(index_000001, hist_data_stock, how='left', left_index=True, right_index=True, suffixes=('_x', '_y'))
                index_000001_stock = index_000001_stock[index_000001_stock.close_y.notnull()]
                if not index_000001_stock.empty:
                    closeX = index_000001_stock['close_x'].values
                    closeY = index_000001_stock['close_y'].values
                    R_square = self.computeCorrelation(closeX, closeY)
                    today_all_roe_pb.loc[stock, field_name] = R_square

            if stock >= '000001' and stock < '300000':
                index_399001_stock = pd.merge(index_399001, hist_data_stock, how='left', left_index=True, right_index=True, suffixes=('_x', '_y'))
                index_399001_stock = index_399001_stock[index_399001_stock.close_y.notnull()]
                if not index_399001_stock.empty:
                    closeX = index_399001_stock['close_x'].values
                    closeY = index_399001_stock['close_y'].values
                    R_square = self.computeCorrelation(closeX, closeY)
                    today_all_roe_pb.loc[stock, field_name] = R_square

            if stock >= '300001' and stock < '600000':
                index_399006_stock = pd.merge(index_399006, hist_data_stock, how='left', left_index=True, right_index=True, suffixes=('_x', '_y'))
                index_399006_stock = index_399006_stock[index_399006_stock.close_y.notnull()]
                if not index_399006_stock.empty:
                    closeX = index_399006_stock['close_x'].values
                    closeY = index_399006_stock['close_y'].values
                    R_square = self.computeCorrelation(closeX, closeY)
                    today_all_roe_pb.loc[stock, field_name] = R_square
            
        # save result
        filename = 'today_all_R_square'
        today_all_roe_pb.to_excel(self.working_folder + \
        'SPSS modeler/复盘/' + filename + '.xlsx', encoding='GBK')

        # backup the file everyday for future review
        filename = 'today_all_R_square' + '_' + today_ISO
        today_all_roe_pb.to_excel(self.working_folder + \
        'SPSS modeler/复盘/' + filename + '.xlsx', encoding='GBK')

        today_all_roe_pb = today_all_roe_pb[today_all_roe_pb.R_square_30days.notnull()]
        today_all_roe_pb_000001 = today_all_roe_pb[today_all_roe_pb.code >= '600001'].R_square_30days.values
        today_all_roe_pb_399001 = today_all_roe_pb[(today_all_roe_pb.code >= '000001') & (today_all_roe_pb.code < '300000')].R_square_30days.values
        today_all_roe_pb_399006 = today_all_roe_pb[(today_all_roe_pb.code >= '300001') & (today_all_roe_pb.code < '600000')].R_square_30days.values

        hindenburg_omen_000001 = np.mean(today_all_roe_pb_000001) 
        hindenburg_omen_399001 = np.mean(today_all_roe_pb_399001) 
        hindenburg_omen_399006 = np.mean(today_all_roe_pb_399006) 

        hindenburg_omen_row = pd.DataFrame(columns=['date',
                                'hindenburg_omen_000001',
                                'hindenburg_omen_399001',
                                'hindenburg_omen_399006',
                                'notification_sent'
                                ], index=["0"])

        path = sys.path[0] + '/notification_monitoring_files/'
        filename = 'hindenburg_omen'
        try:
            hindenburg_omen_last = pd.read_excel(path + filename + '.xlsx')
        except:
            hindenburg_omen_last = hindenburg_omen_row

        hindenburg_omen_row.iloc[0, 0] = today_ISO
        hindenburg_omen_row.iloc[0, 1] = hindenburg_omen_000001
        hindenburg_omen_row.iloc[0, 2] = hindenburg_omen_399001
        hindenburg_omen_row.iloc[0, 3] = hindenburg_omen_399006
        hindenburg_omen_row.iloc[0, 4] = 'N'

        hindenburg_omen_last = hindenburg_omen_last.append(hindenburg_omen_row)
        hindenburg_omen_last.drop_duplicates(subset=['date'], keep='first', inplace=True)
        hindenburg_omen_last.sort_values(by='date', ascending=False, inplace=True)
        hindenburg_omen_last.to_excel(path + filename + '.xlsx',
                    encoding='GBK')
        print('calculate the Hindenburg Omen successful ' + str(total))
        return