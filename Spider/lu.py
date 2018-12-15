import traceback
from time import sleep

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC, wait  # available since 2.26.0
from selenium.webdriver.common.keys import Keys

usr_name = "13524161953"
usr_pwd = "63961310ok"
capa = DesiredCapabilities.CHROME
capa["pageLoadStrategy"] = "none"
#mobile_emulation = {'deviceName': 'iPhone 6 Plus'}
#options = webdriver.ChromeOptions()
#options.add_experimental_option("mobileEmulation", mobile_emulation)
#driver = webdriver.Chrome(desired_capabilities=capa, options=options)
driver = webdriver.Chrome(desired_capabilities=capa)
driver.set_page_load_timeout(10)
wait = WebDriverWait(driver, 20)
driver.maximize_window()

#清除所有cookie
#driver.delete_all_cookies()
driver.get(url='https://www.lup2p.com/user/login')
#windows = driver.window_handles
#输入帐号密码
wait.until(EC.element_to_be_clickable((By.ID, 'loginForm')))
driver.find_element_by_id('userNameLogin').send_keys(usr_name)
driver.find_element_by_id('pwd').send_keys(usr_pwd)
driver.find_element_by_id('validNum').click()
#driver.find_element_by_id('loginForm').submit()
sleep(20)

finish = False
while not finish:
    driver.get(url='https://www.lup2p.com/lup2p/')
    wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'product-title')))
    elements = driver.find_elements_by_partial_link_text('慧盈')
    #url = []
    print (len(elements))
    link = elements[0].get_attribute('href')
    #for i in range(0, len(elements)):
    #    url.append(elements[i].get_attribute('href'))
    
    #status = driver.find_element_by_xpath('//*[@id="p2p-list"]/div/div[2]/ul/li[1]/ul/div[1]/a').text
    try:
        status = driver.find_element_by_xpath('//*[@id="p2p-list"]/div/div[2]/ul/li/ul/div/span').text
        if status == '已售完':
            #sleep(30)
            #driver.refresh()
            print(status)
        else:
            print(status)
    except:
        #for link in url:
        driver.get(link)
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'amountFormat')))
        balance = driver.find_element_by_class_name('amountFormat').get_attribute('data-price').replace(',', '')
        print('account balance: ' + balance)
        wait.until(EC.element_to_be_clickable((By.ID, 'investForm')))
        invest_amount = driver.find_element_by_id('raiseAmount').get_attribute('value').replace(',', '')
        print('investment amount: ' + invest_amount)
        if float(balance) >= float(invest_amount):
            inputElement = driver.find_elements_by_id('invest')
            
            inputElement[0].click()
            wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'infoNextBtn')))
            inputElement = driver.find_elements_by_class_name('infoNextBtn')
            #if not EC.presence_of_element_located((By.CLASS_NAME, "blockUI blockMsg blockPage")) and len(inputElement) > 0:
            if len(inputElement) > 0:
                print('下一步')
                inputElement[0].click()
                #active_window = driver.window_handles[2]
                #driver.switch_to.window(active_window)
                wait.until(EC.element_to_be_clickable((By.ID, "contractAgree")))
                checkbox = driver.find_element_by_xpath('//*[@id="contractAgree"]')
                sleep(4)
                #ActionChains(driver).move_to_element(checkbox).click().perform()
                checkbox.send_keys(Keys.SPACE)
                wait.until(EC.element_to_be_clickable((By.ID, "nextBtn")))
                inputElement = driver.find_elements_by_link_text('下一步')
                inputElement[0].click()
                wait.until(EC.element_to_be_clickable((By.ID, "tradeCode")))
                inputElement = driver.find_element_by_id('tradeCode')
                inputElement.send_keys('728079ok')
                wait.until(EC.element_to_be_clickable((By.ID, "inputValid")))
                inputElement = driver.find_element_by_xpath('//*[@id="inputValid"]')
                inputElement.click()
                sleep(5000)
                finish = True
        else:
            print('余额不足：' + balance + ' --> 退出！')
            finish = True
            driver.quit()
            quit()
    sleep(30)
    driver.refresh()