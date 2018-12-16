# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Site99114Item(scrapy.Item):
    # 公司名
    companyName = scrapy.Field()
    # 连接
    link = scrapy.Field()
    # 公司联系人
    companyContact = scrapy.Field()
    # 经营模式
    businessMode = scrapy.Field()
    # 主营业务
    majorBusiness = scrapy.Field()
    # 所在地区
    area = scrapy.Field()
    # 电话
    telephone = scrapy.Field()
    # email
    email = scrapy.Field()
    # 地址
    address = scrapy.Field()
    # qq
    qq = scrapy.Field()
    # mobile
    mobile = scrapy.Field()
    # fax
    fax = scrapy.Field()
