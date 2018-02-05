import pandas_datareader.data as web
import datetime
import pandas as pd



if __name__ == '__main__':

    # Please set the exchange rate today before run
    exchange_rate = 0.8846

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
        H_price_row = web.get_data_yahoo(H_code).tail(1)
        H_price_row['H_code'] = H_code
        print(H_price_row)
        H_price = H_price.append(H_price_row)
    H_price.drop(['Open', 'High', 'Low', 'Volume', 'Adj Close'], inplace=True, axis=1, errors='ignore')
    H_price.rename(columns={'Close': 'H_price_HKD'}, inplace=True)
    H_price['H_price_RMB'] = H_price['H_price_HKD'].map(
        lambda x: x * exchange_rate)
    print(H_price)
    H_price.to_csv('/Users/yanghui/Documents/yahoo/H_price.csv')

    # inquiry A stock prices
    A_price = pd.DataFrame([])
    for A_code in A_H_stock_df.A_code:
        A_price_row = web.get_data_yahoo(A_code).tail(1)
        A_price_row['A_code'] = A_code
        print(A_price_row)
        A_price = A_price.append(A_price_row)
    A_price.drop(['Open', 'High', 'Low', 'Volume', 'Adj Close'], inplace=True, axis=1, errors='ignore')
    A_price.rename(columns={'Close': 'A_price'}, inplace=True)
    print(A_price)
    A_price.to_csv('/Users/yanghui/Documents/yahoo/A_price.csv')

    # join the A+H prices
    A_H_price_compare_result = pd.merge(A_H_stock_df,H_price,how='left',on=['H_code'])
    A_H_price_compare_result = pd.merge(A_H_price_compare_result,A_price,how='left',on=['A_code'])
    A_H_price_compare_result['A股溢价率'] = 100 * (A_H_price_compare_result['A_price'] -
                                               A_H_price_compare_result['H_price_RMB']) \
                                        / A_H_price_compare_result['H_price_RMB']
    print(A_H_price_compare_result)
    A_H_price_compare_result.to_csv('/Users/yanghui/Documents/yahoo/A_H_price_compare_result.csv',encoding='GBK')
