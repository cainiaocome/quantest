#-*-coding:utf-8-*-
#文件名: matplotlib_ch.py
def set_ch():
	from matplotlib import rcParams, rc
	rcParams['font.family'] = 'sans-serif'
	rcParams['font.sans-serif'] = ['SimHei'] # 指定默认字体
	#rc('font',**{'family':'DejaVu Sans','DejaVu Sans':['PingFang SC']})
	rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题