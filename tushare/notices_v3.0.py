import tushare as ts
import pandas as pd
#from wxpy import *
from datetime import *
import time
from time import strftime, localtime
import sys,os
import threading
import smtplib
from email.mime.text import MIMEText
from email.header import Header

def sendEmail(mail_subject, mail_text,):
    # 第三方 SMTP 服务
    mail_host="smtp.qq.com"  #设置服务器
    mail_user="59272179@qq.com"    #用户名
    mail_pass="63961310(ok)"   #口令 
    sender = '59272179@qq.com'
    receivers = ['59272179@qq.com', '226045968@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    
    message = MIMEText(mail_text, 'plain', 'utf-8')
    message['From'] = Header("张超", 'utf-8')
    message['To'] =  Header("yanghui", 'utf-8')
    
    subject = mail_subject
    message['Subject'] = Header(subject, 'utf-8')
    
    try:
        smtpObj = smtplib.SMTP() 
        smtpObj.connect(mail_host, 587)    # 25 为 SMTP 端口号
        smtpObj.starttls()
        smtpObj.ehlo()
        smtpObj.login(mail_user,mail_pass)  
        smtpObj.sendmail(sender, receivers, message.as_string())
        smtpObj.close()
        print ('邮件发送成功： ' + mail_subject)
    except:
        print ('邮件发送失败： ' + mail_subject)
    return


def M1_notification():
    '''
    消息推送：M0/M1占比分析
    :return: null
    '''
    print(strftime("%Y-%m-%d %H:%M:%S", localtime()) + ' - Start M1_notification thread ')
    path = sys.path[0] + '/notification_monitoring_files/'
    
    while True:
        now = strftime("%H:%M", localtime())
        today_ISO = datetime.today().date().isoformat()
        ## holiday calendar
        holiday_calendar = ['2018-04-05', '2018-04-06', '2018-04-30', \
                            '2018-05-01', '2018-06-18', '2018-09-24', \
                            '2018-10-01', '2018-10-02', '2018-10-03', '2018-10-04', '2018-10-05']
        if datetime.today().weekday() >= 5 or (today_ISO in holiday_calendar):
            holiday = True
        else:
            holiday = False

        if (now > '15:30') and (not holiday):
            # check if today's notification has sent?
            filename = '成交量M1占比'
            try:
                M1_last = pd.read_excel(path + filename + '.xlsx')
            except:
                M1_last = pd.DataFrame(columns=['date',
                                        'M1',
                                        'index_volume_total',
                                        'M1_percentage'
                                        ], index=["0"])
            M1_last_msg_sent_date = M1_last.iloc[0, 0]
        
            #消息推送
            if M1_last_msg_sent_date != today_ISO:
                try:
                    index_sh = ts.get_h_data('000001', index=True, start=today_ISO, end=today_ISO)
                    index_sz = ts.get_h_data('399001', index=True, start=today_ISO, end=today_ISO)
                    if (not index_sh.empty) and (not index_sz.empty):
                        #M0/M1占比分析
                        M1_index_amount = (index_sh.iloc[0, 5] + index_sz.iloc[0, 5]) / 100000000
                        M1_index_volume = (index_sh.iloc[0, 4] + index_sz.iloc[0, 4]) / 100000000
                        filename = '货币供应量_宏观数据_新浪财经'
                        M1_sina = pd.read_excel(path + filename + '.xlsx')
                        ##################################
                        M0 = M1_sina.iloc[0, 5]
                        M0_percentage = 100 * M1_index_amount / M0
                        M1 = M1_sina.iloc[0, 3]
                        M1_percentage = 100 * M1_index_amount / M1

                        M1_row = pd.DataFrame(columns=['date',
                                'M1',
                                'index_volume_total',
                                'M1_percentage'
                                ], index=["0"])

                        M1_row.iloc[0, 0] = today_ISO
                        M1_row.iloc[0, 1] = M1
                        M1_row.iloc[0, 2] = M1_index_amount
                        M1_row.iloc[0, 3] = M1_percentage

                        M1_last = M1_last.append(M1_row)
                        M1_last.sort_values(by='date', ascending=False, inplace=True)
                        filename = '成交量M1占比'
                        M1_last.to_excel(path + filename + '.xlsx',
                                    encoding='GBK')
                    
                        msg =   '==========================' + '\n' + \
                            today_ISO + ' - \n' + \
                            '==========================' + '\n' + \
                            '两市总成交额：' + str(round(M1_index_amount, 3)) + '（亿）\n' + \
                            '两市总成交量：' + str(round(M1_index_volume, 3)) + '（亿）\n' + \
                            'M0：' + str(M0) + '（亿）\n' + \
                            'M1：' + str(M1) + '（亿）\n' + \
                            '两市总成交额占M0：' + str(round(M0_percentage, 3)) + '% \n' + \
                            '两市总成交额占M1：' + str(round(M1_percentage, 3)) + '% \n' + \
                            '=========================='

                        #发送邮件
                        mail_subject = '两市成交 ' + today_ISO
                        mail_text = msg
                        sendEmail(mail_subject=mail_subject, mail_text=mail_text)
                        #发送微信
                        #bot.friends().search('Yang Hui')[0].send(msg)
                        #bot.friends().search('欣')[0].send(msg)  
                except:
                    pass
        time.sleep(600)
    print(strftime("%Y-%m-%d %H:%M:%S", localtime()) + ' - End M1_notification thread ')
    return

def hindenburgOmenNotification():
    '''
    消息推送：兴登堡凶兆
    :return: null
    '''
    print(strftime("%Y-%m-%d %H:%M:%S", localtime()) + ' - Start hindenburgOmenNotification thread ')
    #generic variables initialization
    path = sys.path[0] + '/notification_monitoring_files/'
    while True:
        now = strftime("%H:%M", localtime())
        today_ISO = datetime.today().date().isoformat()
        ## holiday calendar
        holiday_calendar = ['2018-04-05', '2018-04-06', '2018-04-30', \
                            '2018-05-01', '2018-06-18', '2018-09-24', \
                            '2018-10-01', '2018-10-02', '2018-10-03', '2018-10-04', '2018-10-05']
        if datetime.today().weekday() >= 5 or (today_ISO in holiday_calendar):
            holiday = True
        else:
            holiday = False

        if (now > '18:00') and (not holiday):
            filename = 'hindenburg_omen'
            hindenburg_omen = pd.read_excel(path + filename + '.xlsx')
            #消息推送
            if (hindenburg_omen.iloc[0, 0] == today_ISO) & (hindenburg_omen.iloc[0, 4] == 'N'):
                msg =   '==========================' + '\n' + \
                        today_ISO + ' - \n' + \
                        '==========================' + '\n' + \
                        'hindenburg_omen_000001：' + str(round(hindenburg_omen.iloc[0, 1], 2)) + '\n' + \
                        'hindenburg_omen_399001：' + str(round(hindenburg_omen.iloc[0, 2], 2)) + '\n' + \
                        'hindenburg_omen_399006：' + str(round(hindenburg_omen.iloc[0, 3], 2)) + '\n' + \
                        '=========================='
                hindenburg_omen.iloc[0, 4] = 'Y'
                filename = 'hindenburg_omen'
                hindenburg_omen.to_excel(path + filename + '.xlsx',
                    encoding='GBK')
                #发送消息
                mail_subject = 'hindenburg_omen ' + today_ISO
                mail_text = msg
                sendEmail(mail_subject=mail_subject, mail_text=mail_text)
                #bot.friends().search('Yang Hui')[0].send(msg)
                #bot.friends().search('欣')[0].send(msg)
        time.sleep(600)  
    print(strftime("%Y-%m-%d %H:%M:%S", localtime()) + ' - End hindenburgOmenNotification thread ')
    return

def stoplossNotification():
    '''
    消息推送：持仓股票提醒
    :return: null
    '''
    print(strftime("%Y-%m-%d %H:%M:%S", localtime()) + ' - Start stoplossNotification thread ')
    #generic variables initialization
    working_folder = '/Users/yanghui/Documents/'
    
    while True:
        now = strftime("%H:%M", localtime())
        today_ISO = datetime.today().date().isoformat()
        ## 2018 holiday calendar
        holiday_calendar = ['2018-04-05', '2018-04-06', '2018-04-30', \
                            '2018-05-01', '2018-06-18', '2018-09-24', \
                            '2018-10-01', '2018-10-02', '2018-10-03', '2018-10-04', '2018-10-05']
        if datetime.today().weekday() >= 5 or (today_ISO in holiday_calendar):
            holiday = True
        else:
            holiday = False

        #now = '14:30' # for testing purpose, need to remove before use
        if (not holiday) and (now >= '09:30') and (now <= '15:05') :
            filename = 'portfolio'
            portfolio = pd.read_excel(io=working_folder + \
                'quantest/risk_management/' + filename + '.xlsx')
            portfolio.index = portfolio.index.map(lambda x: str(x).zfill(6))
            portfolio_closed = portfolio[portfolio.price_close > 0]
            portfolio_open = portfolio[portfolio.isnull().price_close]
            try:
                today_all = ts.get_today_all()
                today_all['code'] = today_all['code'].map(lambda x: str(x).zfill(6))
                for code in portfolio_open.index:
                    today_all_stock = today_all[(today_all.code == code)]
                    if (today_all_stock.iloc[0,3] <= portfolio_open.loc[code, 'price_stoploss']) and (portfolio_open.loc[code, 'notification_sent'] != 'Y'):
                        #消息推送
                        msg =   '==========================' + '\n' + \
                                today_ISO + ' ' + now + ' - \n' + \
                                '==========================' + '\n' + \
                                '提醒：' + portfolio_open.loc[code, 'name'] + '-跌破止损价' + str(portfolio_open.loc[code, 'price_stoploss']) + '\n' + \
                                '=========================='
                        portfolio_open.loc[code, 'notification_sent'] = 'Y'
                        #发送消息
                        #bot.friends().search('Yang Hui')[0].send(msg)
                        #bot.friends().search('欣')[0].send(msg)
                        
                        #save file
                        portfolio = portfolio_closed.append(portfolio_open)
                        filename = 'portfolio'
                        portfolio.to_excel(working_folder + 'quantest/risk_management/' + filename + '.xlsx', encoding='GBK')
            except:
                pass
        time.sleep(300)  
    print(strftime("%Y-%m-%d %H:%M:%S", localtime()) + ' - End stoplossNotification thread ')
    return

if __name__ == '__main__':
    """
    send to wechat for different kind of notifications

    """
    # 登陆wechat
    #bot = Bot()
    # msg = 'Hello from wechat_bot! Happy trading! Today is: ' + today_ISO
    # bot.friends().search('Yang Hui')[0].send(msg)
    # bot.friends().search('欣')[0].send(msg)
    threads = []
    t1 = threading.Thread(target=M1_notification)
    threads.append(t1)
    t2 = threading.Thread(target=hindenburgOmenNotification)
    threads.append(t2)
    #t3 = threading.Thread(target=stoplossNotification, args=(bot,))
    #threads.append(t3)

    for t in threads:
        t.setDaemon(True)
        t.start()
    
    #等待所有thread结束
    for t in threads:
        t.join()
    print('Exiting Main Thread!')