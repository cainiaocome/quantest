import os
import pickle

file_path = '/Users/yanghui/'
file_name = 'result.pkl'

result_dict = pickle.load(open(file_path + file_name, "rb"))   # 从输出pickle中读取数据
file_name = 'total_portfolios.xlsx'
result_dict["total_portfolios"][:].to_excel(file_path + file_name)
file_name = 'stock_positions.xlsx'
result_dict["stock_positions"][:].to_excel(file_path + file_name)
file_name = 'trades.xlsx'
result_dict["trades"][:].to_excel(file_path + file_name)
cmd = "rqalpha plot '" + file_path + file_name + "'"
os.system(cmd)