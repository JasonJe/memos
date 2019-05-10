# -*- coding: utf-8 -*-

import scrapy
class WechatpubItem(scrapy.Item):
    pass

class PostinfoItem(WechatpubItem):
    title = scrapy.Field()
    href = scrapy.Field()
    author = scrapy.Field()
    pubaccount = scrapy.Field()
    timemark = scrapy.Field()

class PostItem(WechatpubItem):
    url = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    datetime = scrapy.Field()
