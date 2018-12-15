#from matplotlib_ch import set_ch
import pandas as pd
import sys,os
from datetime import *
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import talib



if __name__ == '__main__':
    #set_ch()
    path = sys.path[0]
    today_ISO = datetime.today().date().isoformat()

    start_date = '2016-01-01'
    #end_date = today_ISO
    end_date = '2016-12-31'
    #stock = 'sh.600306'

    all_stock = pd.read_csv(path + "/all_stock.csv")
    all_stock.drop_duplicates(subset=['code'], keep='first', inplace=True)

    profit_data = pd.read_csv(path + "/profit_data.csv")
    profit_data = profit_data[profit_data.code == stock]
    profit_data.sort_values(by='statDate', ascending=True, inplace=True)


    font_small = FontProperties(fname='/Library/Fonts/Songti.ttc',size=10)
    font_medium = FontProperties(fname='/Library/Fonts/Songti.ttc',size=12)
    font_large=FontProperties(fname='/Library/Fonts/Songti.ttc', size=14)
    font_xlarge=FontProperties(fname='/Library/Fonts/Songti.ttc', size=16)

    plt.style.use('ggplot')
    fig, axes = plt.subplots(nrows=4, ncols=1, figsize=(10, 18))
    fig.suptitle(stock + '历史分析',fontproperties=font_xlarge)

    axes[0].set_title(u'历史 roeAvg', fontproperties=font_large)
    axes[0].grid(color='white', which='both', linestyle='-', linewidth=0.4)
    axes[0].set_ylabel('roeAvg',fontproperties=font_medium)
    axes[0].plot(profit_data['statDate'], profit_data['roeAvg'], 'red', linewidth=1)
    #axes[0, 0].set_xlim([0, 100])
    xlabels = axes[0].get_xticklabels()
    for xlabel in xlabels:
        xlabel.set_rotation(45)
        xlabel.set_fontproperties(font_small)
    ylabels = axes[0].get_yticklabels()
    for ylabel in ylabels:
        ylabel.set_fontproperties(font_small)

    axes[1].set_title(u'epsTTM',fontproperties=font_large)
    axes[1].grid(color='white', which='both', linestyle='-', linewidth=0.4)
    axes[1].set_ylabel('epsTTM',fontproperties=font_medium)
    axes[1].plot(profit_data['statDate'], profit_data['epsTTM'], 'blue', linewidth=1)
    #axes[1, 0].set_xlim([0, 100])
    xlabels = axes[1].get_xticklabels()
    for xlabel in xlabels:
        xlabel.set_rotation(45)
        xlabel.set_fontproperties(font_small)
    ylabels = axes[1].get_yticklabels()
    for ylabel in ylabels:
        ylabel.set_fontproperties(font_small)

    axes[2].set_title(u'gpMargin',fontproperties=font_large)
    axes[2].grid(color='white', which='both', linestyle='-', linewidth=0.4)
    axes[2].set_ylabel('gpMargin',fontproperties=font_medium)
    axes[2].plot(profit_data['statDate'], profit_data['gpMargin'], 'green', linewidth=1)
    #axes[1, 0].set_xlim([0, 100])
    xlabels = axes[2].get_xticklabels()
    for xlabel in xlabels:
        xlabel.set_rotation(45)
        xlabel.set_fontproperties(font_small)
    ylabels = axes[2].get_yticklabels()
    for ylabel in ylabels:
        ylabel.set_fontproperties(font_small)

    axes[3].set_title(u'npMargin',fontproperties=font_large)
    axes[3].grid(color='white', which='both', linestyle='-', linewidth=0.4)
    axes[3].set_ylabel('npMargin',fontproperties=font_medium)
    axes[3].plot(profit_data['statDate'], profit_data['npMargin'], 'green', linewidth=1)
    #axes[1, 0].set_xlim([0, 100])
    xlabels = axes[3].get_xticklabels()
    for xlabel in xlabels:
        xlabel.set_rotation(45)
        xlabel.set_fontproperties(font_small)
    ylabels = axes[3].get_yticklabels()
    for ylabel in ylabels:
        ylabel.set_fontproperties(font_small)


    #fig.tight_layout()
    plt.show()


