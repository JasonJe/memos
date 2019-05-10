import scrapy
import json
import urllib
import re

from urllib.parse import quote
from pymongo import MongoClient

from wechatpub.items import WechatpubItem, PostinfoItem, PostItem

class PubinfoSpider(scrapy.Spider):

    name = 'postspider'
    allowed_domains = ['qq.com']

    conn = MongoClient('127.0.0.1', 27017)
    db = conn.WetchatSpider
    pubinfo_set = db.pubinfo_set

    start_urls = []

    for Info in pubinfo_set.find():
        start_urls.append(Info['href'])
    conn.close()

    def start_requests(self):
        for url in self.start_urls:
            print('---------- Request From %s ----------'%url)
            yield scrapy.http.Request(url, self.parse)

    def parse(self, response):
        print('[FEED BACK: %s]'%response.meta)
        content = response.xpath('//*[@id="page-content"]').extract()
        title = response.xpath('//*[@id="activity-name"]/text()').extract()
        mydatetime = response.xpath('//*[@id="post-date"]/text()').extract()

        content = ''.join(content)
        title = ''.join(title).strip()
        mydatetime = ''.join(mydatetime).strip()
        url = response.url

        postitem = PostItem()
        postitem['url'] = url
        postitem['title'] = title
        postitem['content'] = content
        postitem['datetime'] = mydatetime
        print('---------')
        print(title)
        with open('./txtfile/' + title + '.txt', 'w') as f:
            f.write(title + '\t' + mydatetime + '\n')
            f.write(content)
        yield postitem
