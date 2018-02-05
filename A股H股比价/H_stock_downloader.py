import pandas_datareader.data as web
import datetime
import pandas as pd



if __name__ == '__main__':
    # loading stock list
    filepath = '/Users/yanghui/Documents/yahoo/A股H股代码对照表.csv'
    A_H_stock_df = pd.read_csv(filepath)
    A_H_stock_df['A_code2'] = A_H_stock_df['A_code'].map(
        lambda x: x[0:6] + '.SS' if x[7:11] == 'XSHG' else x[0:6] + '.SZ')
    A_H_stock_df.drop(['A_code'], inplace=True, axis=1, errors='ignore')
    A_H_stock_df.rename(columns={'A_code2': 'A_code'}, inplace=True)
    print(A_H_stock_df)


    # inquiry H stock prices
    H_price = pd.DataFrame([])
    for H_code in A_H_stock_df.H_code:
        H_price = web.get_data_yahoo(H_code)
        H_price['H_code'] = H_code
        filename = H_code
        print(H_code)
        filepath = '/Users/yanghui/Documents/yahoo/H_History/' + filename + '.csv'
        H_price.to_csv(filepath)


