# -*- coding: utf-8 -*-

BOT_NAME = 'wechatpub'
LOG_LEVEL = 'INFO'

SPIDER_MODULES = ['wechatpub.spiders']
NEWSPIDER_MODULE = 'wechatpub.spiders'
HTTPERROR_ALLOWED_CODES = [500, 501, 301, 400, 404]
# RETRY_HTTP_CODES = [500, 502, 503, 504, 400, 403, 404, 408]
DOWNLOADER_MIDDLEWARES = {
   'wechatpub.middlewares.ProxMiddleware': 122,
   'wechatpub.middlewares.UserAgentMiddleware': 124,
   'wechatpub.middlewares.PhantomJSMiddleware': 126,
   'scrapy.downloadermiddleware.retry.RetryMiddleware': None,
   'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
   'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 224,
   'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
}
# DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
# HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'

# SPIDER_MIDDLEWARES = {
#     'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
# }

ROBOTSTXT_OBEY = False
CONCURRENT_REQUESTS = 32
DOWNLOAD_DELAY = 3
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
CONCURRENT_REQUESTS_PER_IP = 1
COOKIES_ENABLED = False
DOWNLOAD_TIMEOUT = 15
# REDIRECT_ENABLED = False
#TELNETCONSOLE_ENABLED = False
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}
#AUTOTHROTTLE_ENABLED = True
#AUTOTHROTTLE_START_DELAY = 5
#AUTOTHROTTLE_MAX_DELAY = 60
ITEM_PIPELINES = {
    'wechatpub.pipelines.WechatpubPipeline': 300,
}
MONGO_IP = '127.0.0.1'
MONGO_PORT = 27017
MONGO_DB = 'WetchatSpider'
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
#AUTOTHROTTLE_DEBUG = False
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
