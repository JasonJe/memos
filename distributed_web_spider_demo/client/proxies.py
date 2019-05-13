import requests
import asyncio
import functools
from bs4 import BeautifulSoup
from concurrent import futures

from settings import *
from db.redis_session import *

executor = futures.ThreadPoolExecutor(max_workers = 10)

proxies_set = RedisSet('proxies', host = REDIS_HOST, port = REDIS_PORT, db = REDIS_DB, password = REDIS_PWD)

class GetIps():
    def __init__(self, page):
        self.ips = []
        self.urls = []
        for i in range(page):
            self.urls.append(PROXY_CRAWL_URL + "%s"%i)
        self.header = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36'
        }

    def get_ips(self):
        for url in self.urls:
            res = requests.get(url, headers = self.header)
            soup = BeautifulSoup(res.text, 'html5lib')
            ips = soup.find_all('tr')
            for ip in ips:
                tds = ip.find_all('td')
                if len(tds) < 2:
                    continue
                ip_temp = 'http://' + tds[0].contents[0] + ':' + tds[1].contents[0]
                self.ips.append(str(ip_temp))

    async def review_ips(self, url, ip):
        loop = asyncio.get_event_loop()
        try:
            proxy = {'http': ip}
            response = await loop.run_in_executor(executor, functools.partial(requests.get, url = url, proxies = proxy, timeout = 3))
            if response.status_code == 200:
                proxies_set.add(ip)
            else:
                print('Time Out!')
        except Exception as e:
            print(e)
            pass

    def main(self):
        self.get_ips()
        url = PROXY_TEST_URL
        tasks = [asyncio.ensure_future(self.review_ips(url, ip)) for ip in self.ips]
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait(tasks))
        loop.close()
