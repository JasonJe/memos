import scrapy
import json
import urllib
import re

from urllib.parse import quote
from pymongo import MongoClient

from wechatpub.items import WechatpubItem, PostinfoItem

class PubinfoSpider(scrapy.Spider):
    name = 'pubinfospider'
    allowed_domains = ['sogou.com']

    keyword = input('Input your query keyword:')
    # keyword = 'python'
    start_url = 'http://weixin.sogou.com/weixin?type=2&s_from=input&query=%s&ie=utf8&_sug_=n&_sug_type_='%(quote(keyword))

    start_urls = [start_url]

    def start_requests(self):
        for url in self.start_urls:
            print('---------- Request From %s ----------'%url)
            yield scrapy.http.Request(url, self.parse)

    def parse(self, response):
        print('[FEED BACK: %s]'%response.meta)
        postinfolist = response.xpath('//*[@id="main"]/div/ul[@class="news-list"]/li/div')
        if postinfolist != []:
            for postinfo in postinfolist:
                print('-------------')
                if postinfo.xpath('h3/a/text()').extract_first() is None:
                    continue
                postinfoitem = PostinfoItem()
                title = postinfo.xpath('h3/a/em/text()').extract_first() + postinfo.xpath('h3/a/text()').extract_first()
                href = postinfo.xpath('h3/a/@href').extract_first()
                author = ''.join(postinfo.xpath('div[@class="s-p"]/a/text()').extract())
                pubaccount = postinfo.xpath('div[@class="s-p"]/a/@href').extract_first()
                timemark = ''.join(postinfo.xpath('div[@class="s-p"]/span/text()').extract())
                print(href)

                postinfoitem['title'] = title
                postinfoitem['href'] = href
                postinfoitem['author'] = author
                postinfoitem['pubaccount'] = pubaccount
                postinfoitem['timemark'] = timemark

                yield postinfoitem

            pagenext = response.xpath('//*[@id="sogou_next"]/@href')
            if pagenext:
                url = 'http://weixin.sogou.com/weixin' + pagenext.extract_first()
                yield scrapy.Request(url, callback = self.parse)
