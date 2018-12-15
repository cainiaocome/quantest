import requests
import lxml
from bs4 import BeautifulSoup
import xlwt
import queue
import


class TianYanCha(object):
    def __init__(self):
        self.search_url = 'https://www.tianyancha.com/search?key={}&checkFrom=searchBox'
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding':    'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Connection': 'keep-alive',
            'Host': 'www.tianyancha.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
        }
        self.search_queue = queue.Queue()
        self.cids = set()
        self.redis_r = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)      

    #列表数据
    def load_search_data(self, text):
        soup = BeautifulSoup(text, 'lxml')
        companys = soup.find_all('a', class_='name select-none')
        for company in companys:
            company_id =company['href'].split('/')[-1]
            print("%s 成功" % company_id)
            print('开始下载详情页！======')
            self.load_detail_data(company_id)
            print('详情页成功======')

    #详细数据
    def load_detail_data(self, company_id):
        detail_url = 'https://www.tianyancha.com/company/{}'.format(company_id)
        detail_text = self.get_html(detail_url)
        soup = BeautifulSoup(detail_text, 'lxml')
        name = soup.find('h1', class_="f18 mt0 mb0 in-block vertival-middle sec-c2").text if soup.find('h1', class_="f18 mt0 mb0 in-block vertival-middle sec-c2") else company_id
        #获取详细数据
        get_all_info(soup, company_id, name)
        print("%s 详细数据成功" % company_id)

    def get_html(self, url):
        while True:
            try:
                proxy = get_proxy()#获取代理IP
                #time.sleep(1 + random())
                print('代理IP:'+str(proxy))
                resp = requests.get(url, headers=self.headers, timeout=20, proxies=proxy)
                if resp.status_code == requests.codes.ok:
                    if '请输入验证码' not in resp.text:
                        return resp.text
                    else:
                        print('{}被封了！'.format(proxy))
                elif '融资历史' in resp.text:
                    return resp.text
                else:
                    print('错误的代码编号：{}, url:{}'.format(resp.status_code, url))
            except Exception as e:
                print('url :{},错误：{}'.format(url, e))

    #分页爬数据
    def load_page_data(self,url,word):
        #第一页数据
        print('开始搜索页数据======')
        text = self.get_html(url)
        self.load_search_data(text)

        print('完成搜索数据======')
        #获取分页数据（2-5页）
        print('开始分页数据======')

        soup = BeautifulSoup(text, 'lxml')
        #total = int(soup.find('div', class_='total').lists_text.replace('共', '').replace('页', '')) if soup.find('div', class_='total') else 1
        for index in range(2, 6):
            print('page:https://www.tianyancha.com/search/p{}?key={}'.format(index, word))
            page_url='https://www.tianyancha.com/search/p{}?key={}'.format(index, word)
            text = self.get_html(page_url)
            self.load_search_data(text)
        print('完毕分页数据======')
