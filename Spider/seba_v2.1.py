import traceback
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
import unittest
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from logger import Logger
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import random

class WebKitFeatureStatusTest(unittest.TestCase):
    def setUp(self):
        log.logger.info('seba start...')
        
        capa = DesiredCapabilities.CHROME
        capa["pageLoadStrategy"] = "none"
        self.driver = webdriver.Chrome(desired_capabilities=capa)
       
        # 使用headless无界面浏览器模式
        #chrome_options = webdriver.ChromeOptions()
        #chrome_options.add_argument('--headless')
        #chrome_options.add_argument('--disable-gpu')

        #self.driver = webdriver.Chrome(options=chrome_options)
        #self.driver.set_page_load_timeout(10)
        self.wait = WebDriverWait(self.driver, 20)
        #self.driver.set_window_size(10,10)

    def tearDown(self):
        log.logger.info('seba end...')
        self.driver.quit()

    def test_feature_status_seba(self):
        usr_name = "esheepnetsheep"
        usr_pwd = "63961310ok"
        #print('session id: ' + self.driver.session_id)
        self.driver.get(url='http://sebashow.com/forum.php')
        sleep(5)
        windows = self.driver.window_handles
        #输入帐号密码
        self.driver.find_element_by_id('ls_username').send_keys(usr_name)
        self.driver.find_element_by_id('ls_password').send_keys(usr_pwd)
        self.driver.find_element_by_id('lsform').submit()
        sleep(2)
        self.driver.get(url='http://sebashow.com/forum-134-1.html')
        sleep(2)

        elements = self.driver.find_elements_by_partial_link_text('MP4')
        url = []
        #print (len(elements))
        for i in range(0, len(elements)):
            url.append(elements[i].get_attribute('href'))

        windows = self.driver.window_handles
        #print(windows)
        
        i = 1
        
        #for link in url:
        while i <= 10:
            random_int = random.randint(0,(len(elements) - 1))
            #self.driver.switch_to.window(self.driver.current_window_handle)
            link = url[random_int]
            self.driver.get(link)
            self.wait.until(EC.element_to_be_clickable((By.ID, 'fastpostmessage')))
            self.driver.find_element_by_id('fastpostmessage').send_keys(u'谢谢楼主分享！')                        
            self.driver.find_element_by_id('fastpostform').submit()
            i = i + 1
            sleep(20)


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
