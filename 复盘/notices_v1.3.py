import tushare as ts
import pandas as pd
from wxpy import *
from datetime import *
import time, os, sched


if __name__ == '__main__':
    """
    download the news notice and send to wechat

    """

    #登陆wechat
    today_ISO = datetime.today().date().isoformat()
    bot = Bot()
    msg = 'Hello from wechat_bot! Happy trading! Today is: ' + today_ISO
    bot.friends().search('Yang Hui')[0].send(msg)
    bot.friends().search('欣')[0].send(msg)
    #initialize the notices_last
    filename = 'notices'
    try:
        notices_last = pd.read_excel('/Users/yanghui/Documents/tushare/Notices/' + filename + '_' + today_ISO + '.xlsx')
    except:
        notices_last = pd.DataFrame([])

    ##initialize 大千生态股价发送状态
    dqst_sent = False

    while True:
        ### 新浪新闻提醒
        today_ISO = datetime.today().date().isoformat()
        try:
            notices = ts.get_latest_news()
            for title in notices.title:
                if len(notices_last[notices_last.title == title]) > 0:
                    pass
                else:
                    notices_last = notices_last.append(notices[notices.title == title])
                    # load keyword
                    filename = 'key_word'
                    key_word = pd.read_excel(io='/Users/yanghui/Documents/tushare/Notices/' + filename + '.xlsx')
                    for word in key_word.key_word:
                        if word in title:
                            msg = title + ' - ' + notices[notices.title == title].iloc[0, 3]
                            bot.friends().search('Yang Hui')[0].send(msg)
                            bot.friends().search('欣')[0].send(msg)
        except:
            print('Warning: tushare server maybe down! try again later.')

        #保存消息
        notices_last.sort_values(by='time', ascending=False, inplace=True)
        filename = 'notices'
        notices_last.to_excel('/Users/yanghui/Documents/tushare/Notices/' + filename + '_' + today_ISO + '.xlsx', encoding='GBK')

        ##################################################################
        ### 大千生态股价提醒
        if not dqst_sent:
            try:
                today_all = ts.get_today_all()
                dqst = today_all[today_all.code == '603955']
                if dqst.iloc[0, 2] <= 9.8:
                    dqst_sent = True
                    msg = '大千生态开板了！'
                    bot.friends().search('Yang Hui')[0].send(msg)
                    bot.friends().search('欣')[0].send(msg)
            except:
                pass


        ##################################################################
        # 定时60秒
        print('wait for 60 seconds')
        time.sleep(60)

