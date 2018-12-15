import traceback
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
import unittest
from logger import Logger

class WebKitFeatureStatusTest(unittest.TestCase):
    def setUp(self):
        log.logger.info('seba start...')
        self.driver = webdriver.Safari()

    def tearDown(self):
        log.logger.info('seba end...')
        self.driver.quit()

    def test_feature_status_seba(self):
        usr_name = "esheepnetsheep"
        usr_pwd = "63961310ok"
        print('session id: ' + self.driver.session_id)
        self.driver.get(url='http://sebashow.com/forum.php')
        sleep(5)
        windows = self.driver.window_handles
        #输入帐号密码
        self.driver.find_element_by_id('ls_username').send_keys(usr_name)
        self.driver.find_element_by_id('ls_password').send_keys(usr_pwd)
        self.driver.find_element_by_id('lsform').submit()
        sleep(10)
        self.driver.get(url='http://sebashow.com/forum-134-1.html')
        sleep(5)

        elements = self.driver.find_elements_by_partial_link_text('MP4')
        url = []
        print (len(elements))
        for i in range(0, len(elements)):
                if i <= 4:
                        url.append(elements[i].get_attribute('href'))

        windows = self.driver.window_handles
        print(windows)

        for link in url:
                self.driver.switch_to.window(self.driver.current_window_handle)
                self.driver.get(link)
                if self.driver.find_element_by_id('fastpostmessage').is_displayed:
                    self.driver.find_element_by_id('fastpostmessage').send_keys(u'谢谢楼主分享！')
                    self.driver.find_element_by_id('fastpostform').submit()
                #sleep(2)
        sleep(3600)

if __name__ == '__main__':
        log = Logger(level='debug')
        #suite = unittest.TestSuite()
        #i = 1
        #while i <= 24:
        #        suite.addTest(WebKitFeatureStatusTest("test_feature_status_seba"))
        #        i = i + 1
        #runner = unittest.TextTestRunner()
        #runner.run(suite)
        unittest.main()
