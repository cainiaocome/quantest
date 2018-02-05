import tushare as ts

if __name__ == '__main__':
    sh_index = ts.get_hist_data('sh')
    filename = 'sh_index'
    sh_index.to_excel('/Users/yanghui/Desktop/策略资料/' + filename + '.xlsx', encoding='GBK')

