#-*-coding:utf-8-*-
#文件名: matplotlib_ch.py
#import matplotlib as plt
def set_ch():
	#from matplotlib import rcParams, rc
	from matplotlib.font_manager import FontProperties
	font=FontProperties(fname='/System/Library/Fonts/PingFang.ttc',size=10)
	#rcParams['font.family'] = 'sans-serif'
	#rcParams['font.sans-serif'] = ['SimHei'] # 指定默认字体
	#rc('font',**{'family':'DejaVu Sans','DejaVu Sans':['PingFang SC']})
	#rcParams['font.size'] = 11 # 指定默认字体
	#rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题

