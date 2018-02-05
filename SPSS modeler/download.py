import tushare as ts

if __name__ == '__main__':
    df = ts.get_hist_data('600810',start='2015-01-05',end='2017-03-13')
    df.to_excel('/Users/yanghui/Documents/SPSS modeler/600810/600810.xlsx', encoding='GBK')
