# encoding: UTF-8
from time import strftime, localtime
import pandas as pd
from datetime import *
import tushare as ts

class tushare_api(object):
    today = datetime.today()
    today_year = datetime.today().year
    quarter_list = [1, 2, 3, 4]
    year = 2013
    working_folder = '/Users/huiyang/Documents/'

    warning_list = pd.DataFrame(columns=['return code',
                                         'description',
                                         'additional info 1'
                                        ]
                               )

    # ----------------------------------------------------------------------
    # directly download - Market data
    # ----------------------------------------------------------------------



    def download_today_all(self):
        """

        """

        print('downloading the today_all info...')
        total = 0
        stock_data = ts.get_today_all()
        if stock_data is not None:
            print('Now downloading today_all, total records:' + str(len(stock_data)))
            filename = 'today_all'
            stock_data.to_excel(self.working_folder + 'SPSS modeler/复盘/' + filename + '.xlsx', encoding='GBK')
        else:
            warning_code = pd.DataFrame(
                {'return code': ['for all stocks'], 'description': ['today_all download failed']})
            self.warning_list = self.warning_list.append(warning_code)

    def downloadIndex(self, start='2017-01-01', end=today):
        """
        download the index for today
        """
        print('downloading the index for today...')
        index_000001 = ts.get_h_data('000001', index=True, start=start, end=end)  #上证综指
        index_399001 = ts.get_h_data('399001', index=True, start=start, end=end)  #深圳成指
        index_399006 = ts.get_h_data('399006', index=True, start=start, end=end)  #创业板指
        if not index_000001.empty:
            filename = 'index_000001'
            index_000001.to_excel(self.working_folder + 'SPSS modeler/复盘/' + filename + '.xlsx', encoding='GBK')
        if not index_399001.empty:
            filename = 'index_399001'
            index_399001.to_excel(self.working_folder + 'SPSS modeler/复盘/' + filename + '.xlsx', encoding='GBK')
        if not index_399006.empty:
            filename = 'index_399006'
            index_399006.to_excel(self.working_folder + 'SPSS modeler/复盘/' + filename + '.xlsx', encoding='GBK')
        return

    def download_hist_data(self, start='2015-01-05', end='2015-01-09'):

        print('downloading the hist_data info to csv...')
        filename = 'today_all'
        today_all = pd.read_excel(io=self.working_folder + 'SPSS modeler/复盘/' + filename + '.xlsx')
        stock_list = sorted(list(today_all.code))
        total = 0
        stock_data_all = pd.DataFrame([])
        for stock in stock_list:
            stock = str(stock).zfill(6)
            stock_data_row = ts.get_hist_data(code=stock, pause=1, start=start, end=end)
            if stock_data_row is not None:
                #print('Now downloading stock: ' + stock + ', Total records:' + str(len(stock_data_row)))
                total = total + len(stock_data_row)
                stock_data_row['code'] = float(stock)
                stock_data_all = stock_data_all.append(stock_data_row)
        filename = 'hist_data'
        stock_data_all.to_excel(self.working_folder + 'SPSS modeler/复盘/' + filename + '.xlsx', encoding='GBK')
        print('download_hist_data successful ' + str(total))

    def calculate_today_all_with_percentage(self, start='2015-01-05', end='2015-01-09'):

        print('Calculating today_all_with_percentage')
        filename = 'today_all'
        today_all = pd.read_excel(io=self.working_folder + 'SPSS modeler/复盘/' + filename + '.xlsx')
        today_all['code'] = today_all['code'].map(lambda x: str(x).zfill(6))
        filename = 'hist_data'
        hist_data = pd.read_excel(io=self.working_folder + 'SPSS modeler/复盘/' + filename + '.xlsx')
        hist_data['code'] = hist_data['code'].map(lambda x: str(x).zfill(6))
        hist_data.sort_values(by='date', ascending=False, inplace=True)
        today_all.set_index(keys=['code'], inplace=True, drop=False)
        hist_data = hist_data[hist_data.date != end]
        for stock in today_all.index:
            #print('Now calculating for stock: ' + str(stock))
            today_all.loc[stock, 'yday_percentage'] = 0
            today_all.loc[stock, '2days_percentage'] = 0
            today_all.loc[stock, '3days_percentage'] = 0
            today_all.loc[stock, '4days_percentage'] = 0
            today_all.loc[stock, '5days_percentage'] = 0
            today_all.loc[stock, '10days_percentage'] = 0
            today_all.loc[stock, 'yday_volume'] = 0
            today_all.loc[stock, '2days_volume'] = 0
            today_all.loc[stock, '3days_volume'] = 0
            today_all.loc[stock, '4days_volume'] = 0
            today_all.loc[stock, '5days_volume'] = 0
            today_all.loc[stock, '10days_volume'] = 0
            today_all.loc[stock, 'yday_turnover'] = 0
            today_all.loc[stock, '2days_turnover'] = 0
            today_all.loc[stock, '3days_turnover'] = 0
            today_all.loc[stock, '4days_turnover'] = 0
            today_all.loc[stock, '5days_turnover'] = 0
            today_all.loc[stock, '10days_turnover'] = 0
            if today_all.loc[stock, 'open'] > 0 :
                today_all.loc[stock, 'today_amplitude (%)'] = 100 * abs(
                    today_all.loc[stock, 'high'] - today_all.loc[stock, 'low']) / today_all.loc[stock, 'open']

            # 前一日涨幅
            hist = hist_data[hist_data.code == stock].head(1)
            if len(hist) > 0:
                today_all.loc[stock, 'yday_percentage'] = hist.head(1).iloc[0, 7]
                today_all.loc[stock, 'yday_volume'] = hist.head(1).iloc[0, 5]
                today_all.loc[stock, 'yday_turnover'] = hist.head(1).iloc[0, 14]
            # 2日涨幅
            hist = hist_data[hist_data.code == stock].head(3)
            if len(hist) > 0:
                start_price = hist.tail(1).iloc[0, 3]
                end_price = hist.head(1).iloc[0, 3]
                percentage = 100 * (end_price - start_price) / start_price
                today_all.loc[stock, '2days_percentage'] = percentage
                hist = hist_data[hist_data.code == stock].head(2)
                hist = hist.groupby(['code'], as_index=False).sum()
                today_all.loc[stock, '2days_volume'] = hist.iloc[0, 5]
                today_all.loc[stock, '2days_turnover'] = hist.iloc[0, 14]
            # 3日涨幅
            hist = hist_data[hist_data.code == stock].head(4)
            if len(hist) > 0:
                start_price = hist.tail(1).iloc[0, 3]
                end_price = hist.head(1).iloc[0, 3]
                percentage = 100 * (end_price - start_price) / start_price
                today_all.loc[stock, '3days_percentage'] = percentage
                hist = hist_data[hist_data.code == stock].head(3)
                hist = hist.groupby(['code'], as_index=False).sum()
                today_all.loc[stock, '3days_volume'] = hist.iloc[0, 5]
                today_all.loc[stock, '3days_turnover'] = hist.iloc[0, 14]
            # 4日涨幅
            hist = hist_data[hist_data.code == stock].head(5)
            if len(hist) > 0:
                start_price = hist.tail(1).iloc[0, 3]
                end_price = hist.head(1).iloc[0, 3]
                percentage = 100 * (end_price - start_price) / start_price
                today_all.loc[stock, '4days_percentage'] = percentage
                hist = hist_data[hist_data.code == stock].head(4)
                hist = hist.groupby(['code'], as_index=False).sum()
                today_all.loc[stock, '4days_volume'] = hist.iloc[0, 5]
                today_all.loc[stock, '4days_turnover'] = hist.iloc[0, 14]
            # 5日涨幅
            hist = hist_data[hist_data.code == stock].head(6)
            if len(hist) > 0:
                start_price = hist.tail(1).iloc[0, 3]
                end_price = hist.head(1).iloc[0, 3]
                percentage = 100 * (end_price - start_price) / start_price
                today_all.loc[stock, '5days_percentage'] = percentage
                hist = hist_data[hist_data.code == stock].head(5)
                hist = hist.groupby(['code'], as_index=False).sum()
                today_all.loc[stock, '5days_volume'] = hist.iloc[0, 5]
                today_all.loc[stock, '5days_turnover'] = hist.iloc[0, 14]
            # 10日涨幅
            hist = hist_data[hist_data.code == stock].head(11)
            if len(hist) > 0:
                start_price = hist.tail(1).iloc[0, 3]
                end_price = hist.head(1).iloc[0, 3]
                percentage = 100 * (end_price - start_price) / start_price
                today_all.loc[stock, '10days_percentage'] = percentage
                hist = hist_data[hist_data.code == stock].head(10)
                hist = hist.groupby(['code'], as_index=False).sum()
                today_all.loc[stock, '10days_volume'] = hist.iloc[0, 5]
                today_all.loc[stock, '10days_turnover'] = hist.iloc[0, 14]
        filename = 'today_all_with_percentage'
        today_all.to_excel(self.working_folder + 'SPSS modeler/复盘/' + filename + '.xlsx', encoding='GBK')
        print('today_all_with_percentage successful ')
        return
    
    def calculate_today_all_without_percentage(self, start='2015-01-05', end='2015-01-09'):

        print('Start calculate_today_all_without_percentage')
        filename = 'today_all'
        today_all = pd.read_excel(io=self.working_folder + 'SPSS modeler/复盘/' + filename + '.xlsx')
        today_all['code'] = today_all['code'].map(lambda x: str(x).zfill(6))
        filename = 'hist_data'
        hist_data = pd.read_excel(io=self.working_folder + 'SPSS modeler/复盘/' + filename + '.xlsx')
        hist_data['code'] = hist_data['code'].map(lambda x: str(x).zfill(6))
        hist_data.sort_values(by='date', ascending=False, inplace=True)
        today_all.set_index(keys=['code'], inplace=True, drop=False)
        for stock in today_all.index:
            #print('Now calculating for stock: ' + str(stock))
            today_all.loc[stock, 'yday_percentage'] = 0
            today_all.loc[stock, '2days_percentage'] = 0
            today_all.loc[stock, '3days_percentage'] = 0
            today_all.loc[stock, '4days_percentage'] = 0
            today_all.loc[stock, '5days_percentage'] = 0
            today_all.loc[stock, '10days_percentage'] = 0
            today_all.loc[stock, 'yday_volume'] = 0
            today_all.loc[stock, '2days_volume'] = 0
            today_all.loc[stock, '3days_volume'] = 0
            today_all.loc[stock, '4days_volume'] = 0
            today_all.loc[stock, '5days_volume'] = 0
            today_all.loc[stock, '10days_volume'] = 0
            today_all.loc[stock, 'yday_turnover'] = 0
            today_all.loc[stock, '2days_turnover'] = 0
            today_all.loc[stock, '3days_turnover'] = 0
            today_all.loc[stock, '4days_turnover'] = 0
            today_all.loc[stock, '5days_turnover'] = 0
            today_all.loc[stock, '10days_turnover'] = 0
            if today_all.loc[stock, 'open'] > 0 :
                today_all.loc[stock, 'today_amplitude (%)'] = 100 * abs(
                    today_all.loc[stock, 'high'] - today_all.loc[stock, 'low']) / today_all.loc[stock, 'open']
            # 前一日涨幅
            hist = hist_data[hist_data.code == stock].head(1)
            if len(hist) > 0:
                today_all.loc[stock, 'yday_percentage'] = hist.head(1).iloc[0, 7]
                today_all.loc[stock, 'yday_volume'] = hist.head(1).iloc[0, 5]
                today_all.loc[stock, 'yday_turnover'] = hist.head(1).iloc[0, 14]
            # 2日涨幅
            hist = hist_data[hist_data.code == stock].head(3)
            if len(hist) > 0:
                start_price = hist.tail(1).iloc[0, 3]
                end_price = hist.head(1).iloc[0, 3]
                percentage = 100 * (end_price - start_price) / start_price
                today_all.loc[stock, '2days_percentage'] = percentage
                hist = hist_data[hist_data.code == stock].head(2)
                hist = hist.groupby(['code'], as_index=False).sum()
                today_all.loc[stock, '2days_volume'] = hist.iloc[0, 5]
                today_all.loc[stock, '2days_turnover'] = hist.iloc[0, 14]
            # 3日涨幅
            hist = hist_data[hist_data.code == stock].head(4)
            if len(hist) > 0:
                start_price = hist.tail(1).iloc[0, 3]
                end_price = hist.head(1).iloc[0, 3]
                percentage = 100 * (end_price - start_price) / start_price
                today_all.loc[stock, '3days_percentage'] = percentage
                hist = hist_data[hist_data.code == stock].head(3)
                hist = hist.groupby(['code'], as_index=False).sum()
                today_all.loc[stock, '3days_volume'] = hist.iloc[0, 5]
                today_all.loc[stock, '3days_turnover'] = hist.iloc[0, 14]
            # 4日涨幅
            hist = hist_data[hist_data.code == stock].head(5)
            if len(hist) > 0:
                start_price = hist.tail(1).iloc[0, 3]
                end_price = hist.head(1).iloc[0, 3]
                percentage = 100 * (end_price - start_price) / start_price
                today_all.loc[stock, '4days_percentage'] = percentage
                hist = hist_data[hist_data.code == stock].head(4)
                hist = hist.groupby(['code'], as_index=False).sum()
                today_all.loc[stock, '4days_volume'] = hist.iloc[0, 5]
                today_all.loc[stock, '4days_turnover'] = hist.iloc[0, 14]
            # 5日涨幅
            hist = hist_data[hist_data.code == stock].head(6)
            if len(hist) > 0:
                start_price = hist.tail(1).iloc[0, 3]
                end_price = hist.head(1).iloc[0, 3]
                percentage = 100 * (end_price - start_price) / start_price
                today_all.loc[stock, '5days_percentage'] = percentage
                hist = hist_data[hist_data.code == stock].head(5)
                hist = hist.groupby(['code'], as_index=False).sum()
                today_all.loc[stock, '5days_volume'] = hist.iloc[0, 5]
                today_all.loc[stock, '5days_turnover'] = hist.iloc[0, 14]
            # 10日涨幅
            hist = hist_data[hist_data.code == stock].head(11)
            if len(hist) > 0:
                start_price = hist.tail(1).iloc[0, 3]
                end_price = hist.head(1).iloc[0, 3]
                percentage = 100 * (end_price - start_price) / start_price
                today_all.loc[stock, '10days_percentage'] = percentage
                hist = hist_data[hist_data.code == stock].head(10)
                hist = hist.groupby(['code'], as_index=False).sum()
                today_all.loc[stock, '10days_volume'] = hist.iloc[0, 5]
                today_all.loc[stock, '10days_turnover'] = hist.iloc[0, 14]
            # clean the percentage for today
            today_all.loc[stock, 'changepercent'] = 'NA'

        filename = 'today_all_without_percentage'
        today_all.to_excel(self.working_folder + 'SPSS modeler/复盘/' + filename + '.xlsx', encoding='GBK')
        print('calculate_today_all_without_percentage successful ')

    def calculate_roe_pb(self):
        print('calculate_roe_pb...')

        # read today_all
        filename = 'today_all_with_percentage'
        filepath = self.working_folder + 'SPSS modeler/复盘/'
        today_all = pd.read_excel(filepath + filename + '.xlsx')

        # read stock_basics
        filename = 'stock_basics'
        filepath = self.working_folder + 'SPSS modeler/复盘/'
        stock_basics = pd.read_excel(filepath + filename + '.xlsx')

        # merge today_all with stock_basics
        today_all.drop(['name', 'pb'], inplace=True, axis=1, errors='ignore')
        today_all = pd.merge(today_all, stock_basics, how='right', left_on=['code'], right_on=['code'])
        today_all['code'] = today_all['code'].map(lambda x: str(x).zfill(6))
        today_all.drop_duplicates(subset=['code'], keep='first', inplace=True)
        today_all.set_index(keys=['code'], inplace=True, drop=False)

        # 读取年报季报信息
        filename = 'stock_fundamentals_all'
        filepath = self.working_folder + 'tushare/StockFundamentals_merge/'
        report_data = pd.read_excel(filepath + filename + '.xlsx')
        report_data['code'] = report_data['code'].map(lambda x: str(x).zfill(6))

        today_all['roe_mean'] = None
        today_all['roe/pb'] = None
        today_all['yday_volume/10days_average_volume'] = None

        for stk in today_all.index:
            #print(strftime("%Y-%m-%d %H:%M:%S", localtime()) + ' - Now calculating: ' + str(stk))
            report_data_code = report_data[report_data.code == stk]
            if len(report_data_code) > 0:
                report_data_code.sort_values(by='report_date', inplace=True)
                report_data_code = report_data_code.tail(3)
                # print(report_data_code)
                roe_mean = report_data_code['roe'].mean(axis=0)
                # print(roe_mean)
                today_all.loc[stk, 'roe_mean'] = roe_mean
                pb = today_all.loc[stk, 'pb']
                if pb > 0:
                    today_all.loc[stk, 'roe/pb'] = roe_mean / pb
                volume = today_all.loc[stk, '10days_volume']
                if volume > 0:
                    today_all.loc[stk, 'yday_volume/10days_average_volume'] = (10 * today_all.loc[
                        stk, 'yday_volume']) / (today_all.loc[stk, '10days_volume'])

        today_all.sort_values(by=['industry', 'roe/pb'], inplace=True)
        filename = 'today_all_roe_pb'
        filepath = self.working_folder + 'SPSS modeler/复盘/'
        today_all.to_excel(filepath + filename + '.xlsx', encoding='GBK')

    def download_industry_classified(self):
        """
        返回值说明：

        code：股票代码
        name：股票名称
        c_name：行业名称
        """

        print('downloading the industry_classified info...')
        total = 0
        industry_classified = ts.get_industry_classified()
        if industry_classified is not None:
            print('Now downloading industry_classified, total records:' + str(len(industry_classified)))
            filename = 'industry_classified'
            industry_classified.to_excel(self.working_folder + 'SPSS modeler/复盘/' + filename + '.xlsx', encoding='GBK')
        else:
            warning_code = pd.DataFrame(
                {'return code': ['for all stocks'], 'description': ['industry_classified download failed']})
            self.warning_list = self.warning_list.append(warning_code)

    def download_concept_classified(self):
        """
        返回值说明：

        code：股票代码
        name：股票名称
        c_name：概念名称
        """

        print('downloading the concept_classified info...')
        total = 0
        concept_classified = ts.get_concept_classified()
        if concept_classified is not None:
            print('Now downloading concept_classified, total records:' + str(len(concept_classified)))
            filename = 'concept_classified'
            concept_classified.to_excel(self.working_folder + 'SPSS modeler/复盘/' + filename + '.xlsx', encoding='GBK')
        else:
            warning_code = pd.DataFrame(
                {'return code': ['for all stocks'], 'description': ['concept_classified download failed']})
            self.warning_list = self.warning_list.append(warning_code)

    def download_area_classified(self):
        """
        返回值说明：

        code：股票代码
        name：股票名称
        area：地域名称
        """

        print('downloading the area_classified info...')
        total = 0
        area_classified = ts.get_area_classified()
        if area_classified is not None:
            print('Now downloading area_classified, total records:' + str(len(area_classified)))
            filename = 'area_classified'
            area_classified.to_excel(self.working_folder + 'SPSS modeler/复盘/' + filename + '.xlsx', encoding='GBK')
        else:
            warning_code = pd.DataFrame(
                {'return code': ['for all stocks'], 'description': ['concept_classified download failed']})
            self.warning_list = self.warning_list.append(warning_code)

    def download_stock_basics(self):
        """
        """
        print('downloading the stock_basics info...')
        total = 0
        stock_basics = ts.get_stock_basics()
        if stock_basics is not None:
            print('Now downloading stock_basics, total records:' + str(len(stock_basics)))
            filename = 'stock_basics'
            stock_basics.to_excel(self.working_folder + 'SPSS modeler/复盘/' + filename + '.xlsx', encoding='GBK')
        else:
            warning_code = pd.DataFrame(
                {'return code': ['for all stocks'], 'description': ['stock_basics download failed']})
            self.warning_list = self.warning_list.append(warning_code)

    def download_report_data(self, year=2017, quarter=3):
        """
        """
        print('downloading the report_data info...')

        try:
            data_2017_1 = ts.get_report_data(2017, 1)
            print('Now downloading report_data_2017_1, total records:' + str(len(data_2017_1)))
            filename = 'report_data_2017_1'
            data_2017_1.to_excel(self.working_folder + 'SPSS modeler/复盘/' + filename + '.xlsx', encoding='GBK')
        except:
            print('download report_data_2017_1 failed')

        try:
            data_2017_2 = ts.get_report_data(2017, 2)
            print('Now downloading report_data_2017_2, total records:' + str(len(data_2017_2)))
            filename = 'report_data_2017_2'
            data_2017_2.to_excel(self.working_folder + 'SPSS modeler/复盘/' + filename + '.xlsx', encoding='GBK')
        except:
            print('download report_data_2017_2 failed')

        try:
            data_2017_3 = ts.get_report_data(2017, 3)
            print('Now downloading report_data_2017_3, total records:' + str(len(data_2017_3)))
            filename = 'report_data_2017_3'
            data_2017_3.to_excel(self.working_folder + 'SPSS modeler/复盘/' + filename + '.xlsx', encoding='GBK')
        except:
            print('download report_data_2017_3 failed')

        
        try:
            data_2017_4 = ts.get_report_data(2017, 4)
            print('Now downloading report_data_2017_4, total records:' + str(len(data_2017_4)))
            filename = 'report_data_2017_4'
            data_2017_4.to_excel(self.working_folder + 'SPSS modeler/复盘/' + filename + '.xlsx', encoding='GBK')
        except:
            print('download report_data_2017_4 failed')
        

        data = data_2017_3.append(data_2017_2).append(data_2017_1)

        data.drop_duplicates(subset=['code'], keep='first', inplace=True)
        filename = 'report_data'
        data.to_excel(self.working_folder + 'SPSS modeler/复盘/' + filename + '.xlsx', encoding='GBK')

    def download_profit_data(self, year=2017, quarter=3):
        """
        """
        print('downloading the profit_data info...')

        try:
            data_2017_1 = ts.get_profit_data(2017, 1)
            print('Now downloading profit_data_2017_1, total records:' + str(len(data_2017_1)))
            filename = 'profit_data_2017_1'
            data_2017_1.to_excel(self.working_folder + 'SPSS modeler/复盘/' + filename + '.xlsx', encoding='GBK')
        except:
            print('download profit_data_2017_1 failed')

        try:
            data_2017_2 = ts.get_profit_data(2017, 2)
            print('Now downloading profit_data_2017_2, total records:' + str(len(data_2017_2)))
            filename = 'profit_data_2017_2'
            data_2017_2.to_excel(self.working_folder + 'SPSS modeler/复盘/' + filename + '.xlsx', encoding='GBK')
        except:
            print('download profit_data_2017_2 failed')

        try:
            data_2017_3 = ts.get_profit_data(2017, 3)
            print('Now downloading profit_data_2017_3, total records:' + str(len(data_2017_3)))
            filename = 'profit_data_2017_3'
            data_2017_3.to_excel(self.working_folder + 'SPSS modeler/复盘/' + filename + '.xlsx', encoding='GBK')
        except:
            print('download profit_data_2017_3 failed')

        try:
            data_2017_4 = ts.get_profit_data(2017, 4)
            print('Now downloading profit_data_2017_4, total records:' + str(len(data_2017_4)))
            filename = 'profit_data_2017_4'
            data_2017_4.to_excel(self.working_folder + 'SPSS modeler/复盘/' + filename + '.xlsx', encoding='GBK')
        except:
            print('download profit_data_2017_4 failed')

        data = data_2017_3.append(data_2017_2).append(data_2017_1)
        data.drop_duplicates(subset=['code'], keep='first', inplace=True)
        filename = 'profit_data'
        data.to_excel(self.working_folder + 'SPSS modeler/复盘/' + filename + '.xlsx', encoding='GBK')

    def download_operation_data(self, year=2017, quarter=3):
        """
        """
        print('downloading the operation_data info...')
        try:
            data_2017_1 = ts.get_operation_data(2017, 1)
            print('Now downloading operation_data_2017_1, total records:' + str(len(data_2017_1)))
            filename = 'operation_data_2017_1'
            data_2017_1.to_excel(self.working_folder + 'SPSS modeler/复盘/' + filename + '.xlsx', encoding='GBK')
        except:
            print('download operation_data_2017_1 failed')

        try:
            data_2017_2 = ts.get_operation_data(2017, 2)
            print('Now downloading operation_data_2017_2, total records:' + str(len(data_2017_2)))
            filename = 'operation_data_2017_2'
            data_2017_2.to_excel(self.working_folder + 'SPSS modeler/复盘/' + filename + '.xlsx', encoding='GBK')
        except:
            print('download operation_data_2017_2 failed')

        try:
            data_2017_3 = ts.get_operation_data(2017, 3)
            print('Now downloading operation_data_2017_3, total records:' + str(len(data_2017_3)))
            filename = 'operation_data_2017_3'
            data_2017_3.to_excel(self.working_folder + 'SPSS modeler/复盘/' + filename + '.xlsx', encoding='GBK')
        except:
            print('download operation_data_2017_3 failed')

        try:
            data_2017_4 = ts.get_operation_data(2017, 4)
            print('Now downloading operation_data_2017_4, total records:' + str(len(data_2017_4)))
            filename = 'operation_data_2017_4'
            data_2017_4.to_excel(self.working_folder + 'SPSS modeler/复盘/' + filename + '.xlsx', encoding='GBK')
        except:
            print('download operation_data_2017_4 failed')

        data = data_2017_3.append(data_2017_2).append(data_2017_1)
        data.drop_duplicates(subset=['code'], keep='first', inplace=True)
        filename = 'operation_data'
        data.to_excel(self.working_folder + 'SPSS modeler/复盘/' + filename + '.xlsx', encoding='GBK')

    def download_growth_data(self, year=2017, quarter=3):
        """
        """
        print('downloading the growth_data info...')
        try:
            data_2017_1 = ts.get_growth_data(2017, 1)
            print('Now downloading growth_data_2017_1, total records:' + str(len(data_2017_1)))
            filename = 'growth_data_2017_1'
            data_2017_1.to_excel(self.working_folder + 'SPSS modeler/复盘/' + filename + '.xlsx', encoding='GBK')
        except:
            print('download growth_data_2017_1 failed')

        try:
            data_2017_2 = ts.get_growth_data(2017, 2)
            print('Now downloading growth_data_2017_2, total records:' + str(len(data_2017_2)))
            filename = 'growth_data_2017_2'
            data_2017_2.to_excel(self.working_folder + 'SPSS modeler/复盘/' + filename + '.xlsx', encoding='GBK')
        except:
            print('download growth_data_2017_2 failed')

        try:
            data_2017_3 = ts.get_growth_data(2017, 3)
            print('Now downloading growth_data_2016_3, total records:' + str(len(data_2017_3)))
            filename = 'growth_data_2017_3'
            data_2017_3.to_excel(self.working_folder + 'SPSS modeler/复盘/' + filename + '.xlsx', encoding='GBK')
        except:
            print('download growth_data_2017_3 failed')

        try:
            data_2017_4 = ts.get_growth_data(2017, 4)
            print('Now downloading growth_data_2017_4, total records:' + str(len(data_2017_4)))
            filename = 'growth_data_2017_4'
            data_2017_4.to_excel(self.working_folder + 'SPSS modeler/复盘/' + filename + '.xlsx', encoding='GBK')
        except:
            print('download growth_data_2017_4 failed')

        data = data_2017_3.append(data_2017_2).append(data_2017_1)
        data.drop_duplicates(subset=['code'], keep='first', inplace=True)
        filename = 'growth_data'
        data.to_excel(self.working_folder + 'SPSS modeler/复盘/' + filename + '.xlsx', encoding='GBK')

    def download_debtpaying_data(self, year=2017, quarter=3):
        """
        """
        print('downloading the debtpaying_data info...')
        try:
            data_2017_1 = ts.get_debtpaying_data(2017, 1)
            print('Now downloading debtpaying_data_2017_1, total records:' + str(len(data_2017_1)))
            filename = 'debtpaying_data_2017_1'
            data_2017_1.to_excel(self.working_folder + 'SPSS modeler/复盘/' + filename + '.xlsx', encoding='GBK')
        except:
            print('download debtpaying_data_2017_1 failed')

        try:
            data_2017_2 = ts.get_debtpaying_data(2017, 2)
            print('Now downloading debtpaying_data_2017_2, total records:' + str(len(data_2017_2)))
            filename = 'debtpaying_data_2017_2'
            data_2017_2.to_excel(self.working_folder + 'SPSS modeler/复盘/' + filename + '.xlsx', encoding='GBK')
        except:
            print('download debtpaying_data_2017_2 failed')

        try:
            data_2017_3 = ts.get_debtpaying_data(2017, 3)
            print('Now downloading debtpaying_data_2017_3, total records:' + str(len(data_2017_3)))
            filename = 'debtpaying_data_2017_3'
            data_2017_3.to_excel(self.working_folder + 'SPSS modeler/复盘/' + filename + '.xlsx', encoding='GBK')
        except:
            print('download debtpaying_data_2017_3 failed')

        try:
            data_2017_4 = ts.get_debtpaying_data(2017, 4)
            print('Now downloading debtpaying_data_2017_4, total records:' + str(len(data_2017_4)))
            filename = 'debtpaying_data_2017_4'
            data_2017_4.to_excel(self.working_folder + 'SPSS modeler/复盘/' + filename + '.xlsx', encoding='GBK')
        except:
            print('download debtpaying_data_2017_4 failed')


        data = data_2017_3.append(data_2017_2).append(data_2017_1)
        data.drop_duplicates(subset=['code'], keep='first', inplace=True)
        filename = 'debtpaying_data'
        data.to_excel(self.working_folder + 'SPSS modeler/复盘/' + filename + '.xlsx', encoding='GBK')

    def download_cashflow_data(self, year=2016, quarter=3):
        """
        """
        print('downloading the cashflow_data info...')
        try:
            data_2017_1 = ts.get_cashflow_data(2017, 1)
            print('Now downloading cashflow_data_2017_1, total records:' + str(len(data_2017_1)))
            filename = 'cashflow_data_2017_1'
            data_2017_1.to_excel(self.working_folder + 'SPSS modeler/复盘/' + filename + '.xlsx', encoding='GBK')
        except:
            print('download cashflow_data_2017_1 failed')

        try:
            data_2017_2 = ts.get_cashflow_data(2017, 2)
            print('Now downloading cashflow_data_2017_2, total records:' + str(len(data_2017_2)))
            filename = 'cashflow_data_2017_2'
            data_2017_2.to_excel(self.working_folder + 'SPSS modeler/复盘/' + filename + '.xlsx', encoding='GBK')
        except:
            print('download cashflow_data_2017_2 failed')

        try:
            data_2017_3 = ts.get_cashflow_data(2017, 3)
            print('Now downloading cashflow_data_2017_3, total records:' + str(len(data_2017_3)))
            filename = 'cashflow_data_2017_3'
            data_2017_3.to_excel(self.working_folder + 'SPSS modeler/复盘/' + filename + '.xlsx', encoding='GBK')
        except:
            print('download cashflow_data_2017_3 failed')

        try:
            data_2017_4 = ts.get_cashflow_data(2017, 4)
            print('Now downloading cashflow_data_2017_4, total records:' + str(len(data_2017_4)))
            filename = 'cashflow_data_2017_4'
            data_2017_4.to_excel(self.working_folder + 'SPSS modeler/复盘/' + filename + '.xlsx', encoding='GBK')
        except:
            print('download cashflow_data_2017_4 failed')

        data = data_2017_3.append(data_2017_2).append(data_2017_1)
        data.drop_duplicates(subset=['code'], keep='first', inplace=True)
        filename = 'cashflow_data'
        data.to_excel(self.working_folder + 'SPSS modeler/复盘/' + filename + '.xlsx', encoding='GBK')

    def download_share_profit_data(self, year='2017'):
        """
        """
        print('downloading the share_profit_data info...')

        try:
            share_data_2016 = ts.profit_data(year=year, top=3000)
            print('Now downloading share_data_2016, total records:' + str(len(share_data_2016)))
            filename = 'share_profit_data_2016'
            share_data_2016.to_excel(self.working_folder + 'SPSS modeler/复盘/' + filename + '.xlsx', encoding='GBK')
        except:
            print('download share_data_2016 failed')

        try:
            share_data_2017 = ts.profit_data(year=year, top=3000)
            print('Now downloading share_data_2016, total records:' + str(len(share_data_2017)))
            filename = 'share_profit_data_2017'
            share_data_2017.to_excel(self.working_folder + 'SPSS modeler/复盘/' + filename + '.xlsx', encoding='GBK')
        except:
            print('download share_data_2017 failed')



    def download_forecast_data(self, year=2017, quarter=1):
        """
        """
        print('downloading the forecast_data info...')

        try:
            data_2017_1 = ts.forecast_data(2017, 1)
            print('Now downloading forecast_data_2017_1, total records:' + str(len(data_2017_1)))
            filename = 'forecast_data_2017_1'
            data_2017_1.to_excel(self.working_folder + 'SPSS modeler/复盘/' + filename + '.xlsx', encoding='GBK')
        except:
            print('download forecast_data_2017_1 failed')

        try:
            data_2017_2 = ts.forecast_data(2017, 2)
            print('Now downloading forecast_data_2017_2, total records:' + str(len(data_2017_2)))
            filename = 'forecast_data_2017_2'
            data_2017_2.to_excel(self.working_folder + 'SPSS modeler/复盘/' + filename + '.xlsx', encoding='GBK')
        except:
            print('download forecast_data_2017_2 failed')

        try:
            data_2017_3 = ts.forecast_data(2017, 3)
            print('Now downloading forecast_data_2017_3, total records:' + str(len(data_2017_3)))
            filename = 'forecast_data_2017_3'
            data_2017_3.to_excel(self.working_folder + 'SPSS modeler/复盘/' + filename + '.xlsx', encoding='GBK')
        except:
            print('download forecast_data_2017_3 failed')

        try:
            data_2017_4 = ts.forecast_data(2017, 4)
            print('Now downloading forecast_data_2017_4, total records:' + str(len(data_2017_4)))
            filename = 'forecast_data_2017_4'
            data_2017_4.to_excel(self.working_folder + 'SPSS modeler/复盘/' + filename + '.xlsx', encoding='GBK')
        except:
            print('download forecast_data_2017_4 failed')


        data = data_2017_4.append(data_2017_3).append(data_2017_2).append(data_2017_1)
        data.drop_duplicates(subset=['code'], keep='first', inplace=True)
        filename = 'forecast_data'
        data.to_excel(self.working_folder + 'SPSS modeler/复盘/' + filename + '.xlsx', encoding='GBK')

    def download_xsg_data(self):
        """
        """
        print('downloading the xsg_data info...')

        try:
            data_2017_1 = ts.xsg_data(2017, 1)
            print('Now downloading xsg_data_2017_1, total records:' + str(len(data_2017_1)))
            filename = 'xsg_data_2017_1'
            data_2017_1.to_excel(self.working_folder + 'SPSS modeler/复盘/' + filename + '.xlsx', encoding='GBK')
        except:
            print('download xsg_data_2017_1 failed')

        try:
            data_2017_2 = ts.xsg_data(2017, 2)
            print('Now downloading xsg_data_2017_2, total records:' + str(len(data_2017_2)))
            filename = 'xsg_data_2017_2'
            data_2017_2.to_excel(self.working_folder + 'SPSS modeler/复盘/' + filename + '.xlsx', encoding='GBK')
        except:
            print('download xsg_data_2017_2 failed')


        try:
            data_2017_3 = ts.xsg_data(2017, 3)
            print('Now downloading xsg_data_2017_3, total records:' + str(len(data_2017_3)))
            filename = 'xsg_data_2017_3'
            data_2017_3.to_excel(self.working_folder + 'SPSS modeler/复盘/' + filename + '.xlsx', encoding='GBK')
        except:
            print('download xsg_data_2017_3 failed')

        try:
            data_2017_4 = ts.xsg_data(2017, 4)
            print('Now downloading xsg_data_2017_4, total records:' + str(len(data_2017_4)))
            filename = 'xsg_data_2017_4'
            data_2017_4.to_excel(self.working_folder + 'SPSS modeler/复盘/' + filename + '.xlsx', encoding='GBK')
        except:
            print('download xsg_data_2017_4 failed')

        data = data_2017_3.append(data_2017_2).append(data_2017_1)
        data.drop_duplicates(subset=['code'], keep='first', inplace=True)
        filename = 'xsg_data'
        data.to_excel(self.working_folder + 'SPSS modeler/复盘/' + filename + '.xlsx', encoding='GBK')

    def download_fund_holdings(self, year=2017, quarter=1):
        """
        """
        print('downloading the fund_holdings info...')

        try:
            data_2017_1 = ts.fund_holdings(2017, 1)
            print('Now downloading fund_holdings_2017_1, total records:' + str(len(data_2017_1)))
            filename = 'fund_holdings_2017_1'
            data_2017_1.to_excel(self.working_folder + 'SPSS modeler/复盘/' + filename + '.xlsx', encoding='GBK')
        except:
            print('download fund_holdings_2017_1 failed')

        try:
            data_2017_2 = ts.fund_holdings(2017, 2)
            print('Now downloading fund_holdings_2017_2, total records:' + str(len(data_2017_2)))
            filename = 'fund_holdings_2017_2'
            data_2017_2.to_excel(self.working_folder + 'SPSS modeler/复盘/' + filename + '.xlsx', encoding='GBK')
        except:
            print('download fund_holdings_2017_2 failed')

        try:
            data_2017_3 = ts.fund_holdings(2017, 3)
            print('Now downloading fund_holdings_2017_3, total records:' + str(len(data_2017_3)))
            filename = 'fund_holdings_2017_3'
            data_2017_3.to_excel(self.working_folder + 'SPSS modeler/复盘/' + filename + '.xlsx', encoding='GBK')
        except:
            print('download fund_holdings_2017_3 failed')

        try:
            data_2017_4 = ts.fund_holdings(2017, 4)
            print('Now downloading fund_holdings_2017_4, total records:' + str(len(data_2017_4)))
            filename = 'fund_holdings_2017_4'
            data_2017_4.to_excel(self.working_folder + 'SPSS modeler/复盘/' + filename + '.xlsx', encoding='GBK')
        except:
            print('download fund_holdings_2017_4 failed')


        data = data_2017_3.append(data_2017_2).append(data_2017_1)
        data.drop_duplicates(subset=['code'], keep='first', inplace=True)
        filename = 'fund_holdings'
        data.to_excel(self.working_folder + 'SPSS modeler/复盘/' + filename + '.xlsx', encoding='GBK')

    def download_new_stocks(self):
        """
        """
        print('downloading the new_stocks info...')
        total = 0
        new_stocks = ts.new_stocks()
        if new_stocks is not None:
            print('Now downloading new_stocks, total records:' + str(len(new_stocks)))
            filename = 'new_stocks'
            new_stocks.to_excel(self.working_folder + 'SPSS modeler/复盘/' + filename + '.xlsx', encoding='GBK')
        else:
            warning_code = pd.DataFrame(
                {'return code': ['for all stocks'], 'description': ['new_stocks download failed']})
            self.warning_list = self.warning_list.append(warning_code)

    def download_ST_classified(self):
        """
        """
        print('downloading the ST_classified info...')
        ST_classified = ts.get_st_classified()
        if ST_classified is not None:
            print('Now downloading ST_classified, total records:' + str(len(ST_classified)))
            filename = 'ST_classified'
            ST_classified.to_excel(self.working_folder + 'SPSS modeler/复盘/' + filename + '.xlsx', encoding='GBK')
        else:
            warning_code = pd.DataFrame(
                {'return code': ['for all stocks'], 'description': ['ST_classified download failed']})
            self.warning_list = self.warning_list.append(warning_code)

    def download_stock_D1(self):
        """
        下载日线数据
        """
        print('downloading the stock daily info...')
        stock_basics = ts.get_today_all()
        stock_list = sorted(list(stock_basics.code.values))
        total = 0
        file_path = self.working_folder + 'tushare/StockDaily/'
        for stock in stock_list:
            filename = stock + '.csv'
            stock_data = pd.DataFrame([])
            try:
                stock_data = pd.read_csv(file_path + filename)
                print('downloading:' + stock + ' for the lost data...before count: ' + str(len(stock_data)))
                stock_data.sort_values(by='date', ascending=False, inplace=True)
                start_date = stock_data.head(1).iloc[0, 0]
                end_date = strftime("%Y-%m-%d", localtime())
                try:
                    stock_data_latest = ts.get_k_data(stock, autype=None, start=start_date, end=end_date)
                    stock_data = stock_data.append(stock_data_latest)
                except:
                    pass
            except:
                print('downloading:' + stock + ' for the lost data...before count: ' + str(len(stock_data)))
                year = 1990
                while year <= self.today_year:
                    start_date = str(year) + '-01-01'
                    end_date = str(year) + '-12-31'
                    try:
                        stock_data_latest = ts.get_k_data(stock, autype=None, start=start_date, end=end_date)
                        stock_data = stock_data.append(stock_data_latest)
                    except:
                        pass
                    year = year + 1
            # stock_data['code'] = str(stock).zfill(6)
            # stock_data.index = stock_data.index.map(lambda x: strftime("%Y-%m-%d", x))
            if len(stock_data) > 0:
                stock_data.drop_duplicates(subset=['date'], keep='first', inplace=True)
                stock_data.sort_values(by='date', ascending=False, inplace=True)
                stock_data.set_index(keys=['date'], drop=True, inplace=True, append=False)
                stock_data.to_csv(file_path + filename)
            print('downloading:' + stock + ' for the lost data...after count: ' + str(len(stock_data)))

        print('download_stock_D1 successful ' + str(total))

    def download_stock_D1_qfq(self):
        """
        下载日线数据（前复权）
        """

        print('downloading the stock daily info...')
        stock_basics = ts.get_today_all()
        stock_list = sorted(list(stock_basics.code.values))
        print(stock_list)
        total = 0
        file_path = self.working_folder + 'tushare/StockDaily_qfq/'
        for stock in stock_list:
            filename = stock + '.csv'
            stock_data = pd.DataFrame([])
            try:
                stock_data = pd.read_csv(file_path + filename)
                print('downloading:' + stock + ' for the lost data...before count: ' + str(len(stock_data)))
                stock_data.sort_values(by='date', ascending=False, inplace=True)
                start_date = stock_data.head(1).iloc[0, 0]
                end_date = strftime("%Y-%m-%d", localtime())
                try:
                    stock_data_latest = ts.get_k_data(stock, autype='qfq', start=start_date, end=end_date)
                    stock_data = stock_data.append(stock_data_latest)
                except:
                    pass
            except:
                print('downloading-' + stock + ' for the lost data...before count: ' + str(len(stock_data)))
                year = 1990
                while year <= self.today_year:
                    start_date = str(year) + '-01-01'
                    end_date = str(year) + '-12-31'
                    try:
                        stock_data_latest = ts.get_k_data(stock, autype='qfq', start=start_date, end=end_date)
                        stock_data = stock_data.append(stock_data_latest)
                    except:
                        pass
                    year = year + 1
            # stock_data['code'] = str(stock).zfill(6)
            # stock_data.index = stock_data.index.map(lambda x: strftime("%Y-%m-%d", x))
            if len(stock_data) > 0:
                stock_data.drop_duplicates(subset=['date'], keep='first', inplace=True)
                stock_data.sort_values(by='date', ascending=False, inplace=True)
                stock_data.set_index(keys=['date'], drop=True, inplace=True, append=False)
                stock_data.to_csv(file_path + filename)
            print('downloading-' + stock + ' for the lost data...after count: ' + str(len(stock_data)))

        print('download_stock_D1_qfq successful ' + str(total))
        return

    def download_stock_W1_qfq(self):
        """
        下载周线数据（前复权）
        """

        print('downloading the stock weekly data...')
        filename = 'today_all'
        today_all = pd.read_excel(io=self.working_folder + 'SPSS modeler/复盘/' + filename + '.xlsx')
        today_all['code'] = today_all['code'].map(lambda x: str(x).zfill(6))
        stock_list = sorted(list(today_all.code))

        total = 0
        stock_data = pd.DataFrame([])
        for stock in stock_list:
            year = 2018
            while year <= self.today_year:
                start_date = str(year) + '-01-01'
                end_date = str(year) + '-12-31'
                try:
                    stock_data_latest = ts.get_k_data(stock, ktype='W', autype='qfq', start=start_date, end=end_date)
                    stock_data = stock_data.append(stock_data_latest)
                except:
                    pass
                year = year + 1
            total = total + 1
            print('downloading-' + stock + ' for the weekly data, total count: ' + str(len(stock_data)))

        filename = 'hist_data_weekly_qfq.xlsx'
        file_path = self.working_folder + 'SPSS modeler/复盘/'
        stock_data.to_excel(file_path + filename)
        print('download_stock_W1_qfq successful ' + str(total))
        return


    def download_stock_fundamentals(self, year=2000):
        """
        """
        print('downloading the download_stock_fundamentals...')

        filepath = self.working_folder + 'tushare/StockFundamentals_merge/'
        stock_basics = ts.get_stock_basics()
        filename = 'stock_basics'
        stock_basics.to_excel(filepath + filename + '.xlsx', encoding='GBK')

        while year <= 2017:
            for quarter in self.quarter_list:
                print('Now downloading for:' + str(year) + '-' + str(quarter))
                try:
                    report_data = ts.get_report_data(year, quarter)
                    filename = 'report_data'
                    report_data.to_excel(filepath + str(year) + '_' + str(quarter) + '_' + filename + '.xlsx',
                                         encoding='GBK')
                except:
                    pass

                try:
                    profit_data = ts.get_profit_data(year, quarter)
                    filename = 'profit_data'
                    profit_data.to_excel(filepath + str(year) + '_' + str(quarter) + '_' + filename + '.xlsx',
                                         encoding='GBK')
                except:
                    pass

                try:
                    operation_data = ts.get_operation_data(year, quarter)
                    filename = 'operation_data'
                    operation_data.to_excel(filepath + str(year) + '_' + str(quarter) + '_' + filename + '.xlsx',
                                            encoding='GBK')
                except:
                    pass

                try:
                    growth_data = ts.get_growth_data(year, quarter)
                    filename = 'growth_data'
                    growth_data.to_excel(filepath + str(year) + '_' + str(quarter) + '_' + filename + '.xlsx',
                                         encoding='GBK')
                except:
                    pass

                try:
                    debtpaying_data = ts.get_debtpaying_data(year, quarter)
                    filename = 'debtpaying_data'
                    debtpaying_data.to_excel(filepath + str(year) + '_' + str(quarter) + '_' + filename + '.xlsx',
                                             encoding='GBK')
                except:
                    pass

                try:
                    cashflow_data = ts.get_cashflow_data(year, quarter)
                    filename = 'cashflow_data'
                    cashflow_data.to_excel(filepath + str(year) + '_' + str(quarter) + '_' + filename + '.xlsx',
                                           encoding='GBK')
                except:
                    pass

            year = year + 1

    def format_stock_fundamentals(self, year=1990):
        """
        
        :param year: 
        :return: 
        """

        print('formatting the stock_fundamentals...')
        filepath = self.working_folder + 'tushare/StockFundamentals_merge/'

        stock_basics = ts.get_stock_basics()

        filename = 'stock_basics'
        stock_basics.to_excel(filepath + filename + '.xlsx', encoding='GBK')
        while year <= 2017:
            for quarter in self.quarter_list:
                print('Now formatting for:' + str(year) + '-' + str(quarter))
                try:
                    filename = 'report_data'
                    report_data = pd.read_excel(filepath + str(year) + '_' + str(quarter) + '_' + filename + '.xlsx')
                    if quarter == 1:
                        report_data['report_date'] = report_data['report_date'].map(
                            lambda x: str(year) + '-' + x if x >= '03-31' else str(year + 1) + '-' + x)
                    if quarter == 2:
                        report_data['report_date'] = report_data['report_date'].map(
                            lambda x: str(year) + '-' + x if x >= '06-30' else str(year + 1) + '-' + x)
                    if quarter == 3:
                        report_data['report_date'] = report_data['report_date'].map(
                            lambda x: str(year) + '-' + x if x >= '10-01' else str(year + 1) + '-' + x)
                    if quarter == 4:
                        report_data['report_date'] = report_data['report_date'].map(
                            lambda x: str(year) + '-' + x if x >= '12-01' else str(year + 1) + '-' + x)

                    report_data['code'] = report_data['code'].map(lambda x: str(x).zfill(6))
                    report_data = pd.merge(report_data, stock_basics, how='left', left_on=['code'], right_index=True)
                    report_data.drop(
                        ['name_y', 'pe', 'outstanding', 'totals', 'totalAssets', 'liquidAssets',
                         'fixedAssets', 'reserved', 'reservedPerShare', 'esp', 'bvps_y', 'pb', 'undp', 'perundp', 'rev',
                         'profit', 'gpr', 'npr', 'holders'], inplace=True, axis=1, errors='ignore')
                    report_data['timeToMarket'] = report_data['timeToMarket'].map(
                        lambda x: str(x)[0:4] + '-' + str(x)[4:6] + '-' + str(x)[6:8])
                    report_data.to_excel(filepath + str(year) + '_' + str(quarter) + '_' + filename + '_new' + '.xlsx',
                                         encoding='GBK')
                    report_data = report_data[report_data.report_date >= report_data.timeToMarket]
                    report_data.to_excel(
                        filepath + str(year) + '_' + str(quarter) + '_' + filename + '_final' + '.xlsx', encoding='GBK')
                except:
                    pass
            year = year + 1

    def merge_stock_fundamentals(self, year=1990):
        print('merging the stock_fundamentals...')
        filepath = self.working_folder + 'tushare/StockFundamentals_merge/'
        filename = 'stock_fundamentals_all'
        try:
            stock_fundamentals_all = pd.read_excel(filepath + filename + '.xlsx')
        except:
            stock_fundamentals_all = pd.DataFrame([])
        while year <= 2017:
            for quarter in self.quarter_list:
                print('Now merging for:' + str(year) + '-' + str(quarter))
                try:
                    filename = 'report_data'
                    report_data = pd.read_excel(
                        filepath + str(year) + '_' + str(quarter) + '_' + filename + '_final' + '.xlsx')
                    filename = 'profit_data'
                    profit_data = pd.read_excel(filepath + str(year) + '_' + str(quarter) + '_' + filename + '.xlsx')
                    filename = 'operation_data'
                    operation_data = pd.read_excel(filepath + str(year) + '_' + str(quarter) + '_' + filename + '.xlsx')
                    filename = 'growth_data'
                    growth_data = pd.read_excel(filepath + str(year) + '_' + str(quarter) + '_' + filename + '.xlsx')
                    filename = 'debtpaying_data'
                    debtpaying_data = pd.read_excel(
                        filepath + str(year) + '_' + str(quarter) + '_' + filename + '.xlsx')
                    filename = 'cashflow_data'
                    cashflow_data = pd.read_excel(filepath + str(year) + '_' + str(quarter) + '_' + filename + '.xlsx')

                    ###### merge fundamentals
                    report_data.drop(
                        ['eps', 'bvps', 'roe', 'net_profits'], inplace=True, axis=1, errors='ignore')
                    profit_data.drop(
                        ['name'], inplace=True, axis=1, errors='ignore')
                    operation_data.drop(
                        ['name'], inplace=True, axis=1, errors='ignore')
                    growth_data.drop(
                        ['name'], inplace=True, axis=1, errors='ignore')
                    debtpaying_data.drop(
                        ['name'], inplace=True, axis=1, errors='ignore')
                    cashflow_data.drop(
                        ['name'], inplace=True, axis=1, errors='ignore')
                    stock_fundamentals = pd.merge(report_data, profit_data, how='left', on=['code'])
                    stock_fundamentals = pd.merge(stock_fundamentals, operation_data, how='left', on=['code'])
                    stock_fundamentals = pd.merge(stock_fundamentals, growth_data, how='left', on=['code'])
                    stock_fundamentals = pd.merge(stock_fundamentals, debtpaying_data, how='left', on=['code'])
                    stock_fundamentals = pd.merge(stock_fundamentals, cashflow_data, how='left', on=['code'])
                    filename = 'stock_fundamentals'
                    stock_fundamentals.to_excel(
                        filepath + str(year) + '_' + str(quarter) + '_' + filename + '.xlsx', encoding='GBK')
                    stock_fundamentals_all = stock_fundamentals_all.append(stock_fundamentals)
                except:
                    pass
            year = year + 1
        stock_fundamentals_all.drop_duplicates(
            subset=['code', 'report_date', 'roe', 'net_profit_ratio', 'gross_profit_rate', 'net_profits', 'eps',
                    'business_income'], inplace=True)
        filename = 'stock_fundamentals_all'
        stock_fundamentals_all.to_excel(
            filepath + filename + '.xlsx', encoding='GBK')
