# -*- coding: utf-8 -*-

import pymongo

class WechatpubPipeline(object):
    def __init__(self, mongo_ip, mongo_port, mongo_db):
        self.mongo_ip = mongo_ip
        self.mongo_port = mongo_port
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(mongo_ip = crawler.settings.get('MONGO_IP'), mongo_port = crawler.settings.get('MONGO_PORT'), mongo_db = crawler.settings.get('MONGO_DB'))

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_ip, self.mongo_port)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if spider.name == 'pubinfospider':
            collection_name = 'pubinfo_set'
            self.db[collection_name].insert(dict(item))
            return item
        elif spider.name == 'postspider':
            collection_name = 'post_set'
            self.db[collection_name].insert(dict(item))
            return item
        else:
            return None
