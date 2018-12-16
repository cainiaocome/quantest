import scrapy
from site_99114.items import Site99114Item

class QuotesSpider(scrapy.Spider):
    name = "site_99114"

    def start_requests(self):
        page = 1
        urls = []
        while page <= 255:
            url = 'http://shop.99114.com/list/area/101111107_%s' % page
            urls.append(url)
            #print(url)
            page = page + 1

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        #page = response.url.split("_")[-1]
        #filename = 'jinhua-page-%s.html' % page
        #with open(filename, 'wb') as f:
        #    f.write(response.body)
        #self.log('Saved file %s' % filename)
        
        urls = response.xpath('//*[@id="footerTop"]/ul/li/a/@href').extract()
        #print(urls)
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_detail)
        
    def parse_detail(self, response):
        #print(response.url)
        item = Site99114Item()
        item['companyName'] = 'NA'
        companyName = response.xpath('//*[@id="module_193165"]/div/div/div[4]/div/ul/li[2]/div/text()').extract()
        if len(companyName) > 0:
            item['companyName'] = companyName[0].replace('\n', '').replace('\t', '').replace('\r', '')

        item['link'] = response.url

        item['companyContact'] = 'NA'
        companyContact = response.xpath('//*[@id="module_193165"]/div/div/div[4]/div/ul/li[1]/div/p/span/text()').extract()
        if len(companyContact) > 0:
            item['companyContact'] = companyContact[0]

        item['businessMode'] = 'NA'
        businessMode = response.xpath('//*[@id="module_221762"]/div[1]/div/div/div[2]/div[2]/p[2]/span[2]/text()').extract()
        if len(businessMode) > 0:
            item['businessMode'] = businessMode[0]

        item['majorBusiness'] = 'NA'     
        majorBusiness = response.xpath('//*[@id="module_221762"]/div[1]/div/div/div[2]/div[2]/p[3]/span[2]/text()').extract()
        if len(majorBusiness) > 0:
            item['majorBusiness'] = majorBusiness[0]
        
        item['area'] = 'NA'
        area = response.xpath('//*[@id="module_221762"]/div[1]/div/div/div[2]/div[2]/p[4]/span[2]/text()').extract()
        if len(area) > 0:
            item['area'] = area[0]

        item['telephone'] = 'NA'
        item['email'] = 'NA'
        item['fax'] = 'NA'
        label = response.xpath('//*[@id="module_193165"]/div/div/div[4]/div/ul/li[3]/div[1]/div[1]/ul/li[*]/span/text()').extract()
        if len(label) > 0:
            i = 0
            while i < len(label):
                if label[i] == '电\xa0\xa0话：':
                    item['telephone'] = label[i+1].replace('\n', '').replace('\t', '').replace('\r', '')
                if label[i] == '邮\xa0\xa0箱：':
                    item['email'] = label[i+1].replace('\n', '').replace('\t', '').replace('\r', '').replace(' ', '')
                if label[i] == '传\xa0\xa0真：':
                    item['fax'] = label[i+1].replace('\n', '').replace('\t', '').replace('\r', '')
                i = i + 1

        item['address'] = response.xpath('//*[@id="detialAddr"]/text()').extract()[0].replace('\n', '').replace('\t', '').replace('\r', '')
        

        item['mobile'] = 'NA'
        item['qq'] = 'NA'
        label = response.xpath('//*[@id="module_193165"]/div/div/div[4]/div/ul/li[1]/div/p[*]/span/text()').extract()
        if len(label) > 0:
            i = 0
            while i < len(label):
                if label[i] == '手\xa0机：':
                    item['mobile'] = label[i+1].replace('\n', '').replace('\t', '').replace('\r', '')
                if label[i] == '联系我：':
                    qq = response.xpath('//*[@id="module_193165"]/div/div/div[4]/div/ul/li[1]/div/p[%d]/a/@title' %(i+1)).extract()

                i = i + 1
        yield item
