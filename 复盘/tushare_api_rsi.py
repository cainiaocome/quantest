# encoding: UTF-8
import pandas as pd
import talib
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
            print('Now calculating RSI for stock: ' + str(stock))
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
