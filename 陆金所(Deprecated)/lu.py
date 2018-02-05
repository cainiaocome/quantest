import traceback
from time import sleep

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium import webdriver
import unittest
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC, wait  # available since 2.26.0

usr_name = "13524161953"
usr_pwd = "63961310ok"
#mobileEmulation = {'deviceName': 'Apple iPhone 6'}
#options = webdriver.ChromeOptions()
#options.add_experimental_option('mobileEmulation', mobileEmulation)
#driver = webdriver.Chrome(chrome_options=options)
driver = webdriver.Chrome()

#清除所有cookie
#driver.delete_all_cookies()
driver.get(url='https://www.lu.com')
driver.implicitly_wait(10)

print(driver.get_cookies())


ele0 = driver.find_element_by_link_text("登录").click()
sleep(30)
#WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID,"userName")))
#driver.find_element_by_id("userName").send_keys(usr_name)
driver.get(url='https://www.lup2p.com/lup2p/transfer/list/p2p')
print(driver.get_cookies())

# go to the google home page
finish = False

while not finish:
    inputElement = driver.find_elements_by_link_text('投资')
    if len(inputElement) > 0:
        print('投资')
        inputElement[0].click()
        active_window = driver.window_handles[1]
        driver.switch_to.window(active_window)
        inputElement = driver.find_elements_by_link_text('立即投资')

        #if not EC.presence_of_element_located((By.CLASS_NAME, "blockUI blockMsg blockPage")) and len(inputElement) > 0:
        if len(inputElement) > 0:
            print('立即投资')
            #if driver.find_elements_by_xpath(//price<4000.00):
            inputElement[0].click()
            inputElement = driver.find_elements_by_link_text('下一步')
            #if not EC.presence_of_element_located((By.CLASS_NAME, "blockUI blockMsg blockPage")) and len(inputElement) > 0:
            if len(inputElement) > 0:
                print('下一步')
                inputElement[0].click()
                #active_window = driver.window_handles[2]
                #driver.switch_to.window(active_window)
                inputElement = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "agreeInvest")))
                inputElement.click()
                inputElement = driver.find_elements_by_link_text('下一步')
                inputElement[0].click()
                inputElement = driver.find_elements_by_id('tradeCode')
                inputElement[0].send_keys('728079ok')
                sleep(50000)
                inputElement[0].submit()
                finish = True
            else:
                print('下一步 not found')
                #sleep(50000)
            driver.close()
            #active_window = driver.window_handles[1]
            #driver.switch_to.window(active_window)
        else:
            print('立即投资 not found')
            driver.close()
        active_window = driver.window_handles[0]
        driver.switch_to.window(active_window)
        sleep(5)
        driver.refresh()
    else:
        traceback.print_exc()
        sleep(5)
        driver.refresh()




print(driver.title)

