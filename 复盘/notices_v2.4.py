import tushare as ts
import pandas as pd
from wxpy import *
from datetime import *
import time
from time import strftime, localtime


def sina_news_notification(bot):
    '''
    新浪新闻提醒
    :param: 
    :return: 
    '''
    today_ISO = datetime.today().date().isoformat()
    # initialize the notices_last
    filename = 'notices'
    try:
        notices_last = pd.read_excel('/Users/huiyang/Documents/tushare/Notices/' + filename + '_' + today_ISO + '.xlsx')
    except:
        notices_last = pd.DataFrame(columns=['classify',
                                             'title',
                                             'time',
                                             'url',
                                             'content'
                                             ])

    today_md = strftime("%m-%d 00:00", localtime())
    if len(notices_last) > 0:
        notices_last = notices_last[notices_last.time >= today_md]
    try:
        notices = ts.get_latest_news(show_content=True)
        notices = notices[notices.time >= today_md]
        for title in notices.title:
            if len(notices_last[notices_last.title == title]) <= 0:
                notices_last = notices_last.append(notices[notices.title == title])
                # load keyword
                filename = 'key_word'
                key_word = pd.read_excel(io='/Users/huiyang/Documents/tushare/Notices/' + filename + '.xlsx')
                for word in key_word.key_word:
                    if word in title:
                        msg = title + ' - ' + notices[notices.title == title].iloc[0, 3]
                        if key_word[key_word.key_word == word].iloc[0, 1] == 'Y':
                            bot.friends().search('Yang Hui')[0].send(msg)
                        if key_word[key_word.key_word == word].iloc[0, 2] == 'Y':
                            bot.friends().search('欣')[0].send(msg)
    except:
        print(strftime("%Y-%m-%d %H:%M:%S", localtime()) + '-Warning: tushare server maybe down! try again later.')

    # 保存消息
    notices_last.sort_values(by='time', ascending=False, inplace=True)
    filename = 'notices'
    notices_last.to_excel('/Users/huiyang/Documents/tushare/Notices/' + filename + '_' + today_ISO + '.xlsx',
                          encoding='GBK')
    return


def M0_notification(bot):
    '''
    M0 占比分析消息推送
    :return: 
    '''
    M0_sched_Timer = '15:30'
    today_ISO = datetime.today().date().isoformat()
    now = strftime("%H:%M", localtime())
    M0_row = pd.DataFrame(columns=['date',
                                   'M0',
                                   'index_volume_total',
                                   'M0_percentage'
                                   ], index=["0"])
    filename = '成交量M0占比'
    try:
        M0_last = pd.read_excel('/Users/huiyang/Documents/sina/' + filename + '.xlsx')
    except:
        M0_last = pd.DataFrame(columns=['date',
                                        'M0',
                                        'index_volume_total',
                                        'M0_percentage'
                                        ], index=["0"])
    M0_last_msg_sent_date = M0_last.iloc[0, 0]
    if now >= M0_sched_Timer and M0_last_msg_sent_date != today_ISO:
        try:
            index_sh = ts.get_h_data('000001', index=True, start=today_ISO, end=today_ISO)
            index_sz = ts.get_h_data('399001', index=True, start=today_ISO, end=today_ISO)
            # index_sh = ts.get_h_data('000001', index=True, start='2017-04-27', end=today_ISO)
            # index_sz = ts.get_h_data('399001', index=True, start='2017-04-27', end=today_ISO)
            if len(index_sh) > 0 and len(index_sz) > 0:
                M0_index_amount = (index_sh.iloc[0, 5] + index_sz.iloc[0, 5]) / 100000000
                M0_index_volume = (index_sh.iloc[0, 4] + index_sz.iloc[0, 4]) / 100000000
                filename = '货币供应量_宏观数据_新浪财经'
                M0_sina = pd.read_excel('/Users/huiyang/Documents/sina/' + edirafilename + '.xlsx')
                ##################################
                M0 = M0_sina.iloc[0, 5]
                M0_percentage = 100 * M0_index_amount / M0

                msg = today_ISO + ' - \n' + \
                      '两市总成交额：' + str(round(M0_index_amount, 2)) + '（亿）\n' + \
                      '两市总成交量：' + str(round(M0_index_volume, 2)) + '（亿）\n' + \
                      'M0：' + str(M0) + '（亿）\n' + \
                      '两市总成交额占M0：' + str(round(M0_percentage, 2)) + '%'
                bot.friends().search('Yang Hui')[0].send(msg)
                bot.friends().search('欣')[0].send(msg)

                M0_row.iloc[0, 0] = today_ISO
                M0_row.iloc[0, 1] = M0
                M0_row.iloc[0, 2] = M0_index_amount
                M0_row.iloc[0, 3] = M0_percentage

                M0_last = M0_last.append(M0_row)
                M0_last.sort_values(by='date', ascending=False, inplace=True)
                filename = '成交量M0占比'
                M0_last.to_excel(
                    '/Users/huiyang/Documents/sina/' + filename + '.xlsx',
                    encoding='GBK')
            else:
                print(strftime("%Y-%m-%d %H:%M:%S",
                               localtime()) + '-Warning: index not available today')
        except:
            #print(strftime("%Y-%m-%d %H:%M:%S",
            #               localtime()) + '-Warning: get index failed, index not available today')
            pass
    return


def M1_notification(bot):
    '''
    M1 占比分析消息推送
    :return:
    '''
    M1_sched_Timer = '15:30'
    today_ISO = datetime.today().date().isoformat()
    now = strftime("%H:%M", localtime())
    M1_row = pd.DataFrame(columns=['date',
                                   'M1',
                                   'index_volume_total',
                                   'M1_percentage'
                                   ], index=["0"])
    filename = '成交量M1占比'
    try:
        M1_last = pd.read_excel('/Users/huiyang/Documents/sina/' + filename + '.xlsx')
    except:
        M1_last = pd.DataFrame(columns=['date',
                                        'M1',
                                        'index_volume_total',
                                        'M1_percentage'
                                        ], index=["0"])
    M1_last_msg_sent_date = M1_last.iloc[0, 0]
    if now >= M1_sched_Timer and M1_last_msg_sent_date != today_ISO:
        try:
            index_sh = ts.get_h_data('000001', index=True, start=today_ISO, end=today_ISO)
            index_sz = ts.get_h_data('399001', index=True, start=today_ISO, end=today_ISO)
            # index_sh = ts.get_h_data('000001', index=True, start='2017-04-27', end=today_ISO)
            # index_sz = ts.get_h_data('399001', index=True, start='2017-04-27', end=today_ISO)
            if len(index_sh) > 0 and len(index_sz) > 0:
                M1_index_amount = (index_sh.iloc[0, 5] + index_sz.iloc[0, 5]) / 100000000
                M1_index_volume = (index_sh.iloc[0, 4] + index_sz.iloc[0, 4]) / 100000000
                filename = '货币供应量_宏观数据_新浪财经'
                M1_sina = pd.read_excel('/Users/huiyang/Documents/sina/' + filename + '.xlsx')
                ##################################
                M0 = M1_sina.iloc[0, 5]
                M0_percentage = 100 * M1_index_amount / M0
                M1 = M1_sina.iloc[0, 3]
                M1_percentage = 100 * M1_index_amount / M1

                msg = today_ISO + ' - \n' + \
                      '两市总成交额：' + str(round(M1_index_amount, 3)) + '（亿）\n' + \
                      '两市总成交量：' + str(round(M1_index_volume, 3)) + '（亿）\n' + \
                      'M0：' + str(M0) + '（亿）\n' + \
                      'M1：' + str(M1) + '（亿）\n' + \
                      '两市总成交额占M0：' + str(round(M0_percentage, 3)) + '% \n' \
                      '两市总成交额占M1：' + str(round(M1_percentage, 3)) + '%'
                bot.friends().search('Yang Hui')[0].send(msg)
                bot.friends().search('欣')[0].send(msg)

                M1_row.iloc[0, 0] = today_ISO
                M1_row.iloc[0, 1] = M1
                M1_row.iloc[0, 2] = M1_index_amount
                M1_row.iloc[0, 3] = M1_percentage

                M1_last = M1_last.append(M1_row)
                M1_last.sort_values(by='date', ascending=False, inplace=True)
                filename = '成交量M1占比'
                M1_last.to_excel(
                    '/Users/huiyang/Documents/sina/' + filename + '.xlsx',
                    encoding='GBK')
            else:
                print(strftime("%Y-%m-%d %H:%M:%S",
                               localtime()) + '-Warning: index not available today')
        except:
            #print(strftime("%Y-%m-%d %H:%M:%S",
            #               localtime()) + '-Warning: get index failed, index not available today')
            pass
    return

def open_limit_notification(bot, dqst_sent):
    '''
    大千生态股价发送状态
    :return: 
    '''
    ##################################################################
    ### 大千生态股价提醒
    ##################################################################
    if not dqst_sent:
        try:
            today_all = ts.get_today_all()
            dqst = today_all[today_all.code == '603955']
            curr_time = strftime("%H:%M:%S", localtime())
            # check the percentage is <=9.8 and volume > 0 and current time is market opened.
            if dqst.iloc[0, 2] <= 9.8 and dqst.iloc[0, 8] > 0 and curr_time > '09:30:00':
                dqst_sent = True
                msg = '大千生态开板了！'
                bot.friends().search('Yang Hui')[0].send(msg)
                bot.friends().search('欣')[0].send(msg)
        except:
            pass
    return dqst_sent


if __name__ == '__main__':
    """
    send to wechat for different kind of notifications

    """

    # 登陆wechat
    bot = Bot()
    # msg = 'Hello from wechat_bot! Happy trading! Today is: ' + today_ISO
    # bot.friends().search('Yang Hui')[0].send(msg)
    # bot.friends().search('欣')[0].send(msg)

    while True:
        ##############################################################################################################
        #try:
        #    sina_news_notification(bot)
        #except:
        #    print(strftime("%Y-%m-%d %H:%M:%S", localtime()) + '-Warning: sina_news_notification failed!')
        ##############################################################################################################
        #try:
        #    M0_notification(bot)
        #except:
        #    print(strftime("%Y-%m-%d %H:%M:%S", localtime()) + '-Warning: M0_notification failed!')
        try:
            M1_notification(bot)
        except:
            print(strftime("%Y-%m-%d %H:%M:%S", localtime()) + '-Warning: M1_notification failed!')

        ##############################################################################################################
        #try:
        #    dqst_sent = open_limit_notification(bot, dqst_sent)
        #except:
        #    print(strftime("%Y-%m-%d %H:%M:%S", localtime()) + '-Warning: open_limit_notification failed!')
        ##############################################################################################################
        # 60秒重试
        time.sleep(60)