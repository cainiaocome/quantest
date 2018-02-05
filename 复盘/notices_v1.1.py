import tushare as ts
import pandas as pd
from wxpy import *
from datetime import *
import time, os, sched


if __name__ == '__main__':
    """
    download the news notice and send to wechat

    """

    #load keyword
    filename = 'key_word'
    key_word = pd.read_excel(io='/Users/yanghui/Documents/tushare/Notices/' + filename + '.xlsx')
    #登陆wechat
    today_ISO = datetime.today().date().isoformat()
    bot = Bot()
    msg = 'Hello from wechat_bot! Happy trading! Today is: ' + today_ISO
    bot.friends().search('Yang Hui')[0].send(msg)
    bot.friends().search('欣')[0].send(msg)
    #initialize the notices_last
    filename = 'notices'
    notices_last = pd.read_excel('/Users/yanghui/Documents/tushare/Notices/' + filename + '_' + today_ISO + '.xlsx')

    while True:
        today_ISO = datetime.today().date().isoformat()
        notices = ts.get_latest_news(top=80)
        for title in notices.title:
            if len(notices_last[notices_last.title == title]) > 0:
                pass
            else:
                notices_last = notices_last.append(notices[notices.title == title])
                for word in key_word.key_word:
                    if word in title:
                        msg = title + ' - ' + notices[notices.title == title].iloc[0,3]
                        bot.friends().search('Yang Hui')[0].send(msg)
                        bot.friends().search('欣')[0].send(msg)


        #保存消息
        notices_last.sort_values(by='time', ascending=False, inplace=True)
        notices_last.to_excel('/Users/yanghui/Documents/tushare/Notices/' + filename + '_' + today_ISO + '.xlsx', encoding='GBK')
        #定时60秒
        print('wait for 60 seconds')
        time.sleep(60)

