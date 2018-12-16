# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import xlwt

class Site99114Pipeline(object):
    """ 
    功能：保存item数据 
    """
    def __init__(self):
        self.workbook = xlwt.Workbook(encoding='utf-8')
        self.sheet = self.workbook.add_sheet('19114.com')
        self.sheet.write(0, 0, '名称')
        self.sheet.write(0, 1, '链接')
        self.sheet.write(0, 2, '联系人')
        self.sheet.write(0, 3, '类型')
        self.sheet.write(0, 4, '地区')
        self.sheet.write(0, 5, '电话')
        self.sheet.write(0, 6, 'email')
        self.sheet.write(0, 7, '地址')
        self.sheet.write(0, 8, 'qq')
        self.sheet.write(0, 9, '手机')
        self.sheet.write(0, 10, '传真')
        self.count = 1

    def process_item(self, item, spider):
        self.sheet.write(self.count, 0, item['companyName'])
        self.sheet.write(self.count, 1, item['link'])
        self.sheet.write(self.count, 2, item['companyContact'])
        self.sheet.write(self.count, 3, item['businessMode'])
        self.sheet.write(self.count, 4, item['area'])
        self.sheet.write(self.count, 5, item['telephone'])
        self.sheet.write(self.count, 6, item['email'])
        self.sheet.write(self.count, 7, item['address'])
        self.sheet.write(self.count, 8, item['qq'])
        self.sheet.write(self.count, 9, item['mobile'])
        self.sheet.write(self.count, 10, item['fax'])

        self.count += 1
        return item

    def close_spider(self, spider):
        #print ('ExcelPipline info:  items size: %s' % self.count)
        #file_name = _generate_filename(spider, file_format='xlsx')
        #self.wb.save(file_name)
        self.workbook.save('19114.xls')
        pass