import random
import requests
import traceback
from bs4 import BeautifulSoup

from settings import *

from server.proxies import *
from server.user_agent import *
from db.redis_session import *
from server.pipelines import *

proxies_set = RedisSet('proxies', host = REDIS_HOST, port = REDIS_PORT, db = REDIS_DB, password = REDIS_PWD)
pageurls_queue = RedisQueue('pageurls', host = REDIS_HOST, port = REDIS_PORT, db = REDIS_DB, password = REDIS_PWD)

class Engine():
    def __init__(self, root_url, page_num):
        self.root_url = root_url
        self.page_num = page_num

    def get_urls(self, num):
        while True:
            try:
                headers = {
                    'User-Agent': random.sample(user_agent_list, 1)[0],
                    'Host': 'www.lagou.com',
                    'Connection': 'keep-alive',
                    'Content-Length': '26',
                    'Pragma': 'no-cache',
                    'Cache-Control': 'no-cache',
                    'Origin': 'https://www.lagou.com',
                    'X-Anit-Forge-Code': '0',
                    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                    'Accept': 'application/json, text/javascript, */*; q=0.01',
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-Anit-Forge-Token': 'None',
                    'Referer': 'https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput=',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Accept-Language': 'zh-CN,zh;q=0.9',
                    'Cookie': '_ga=GA1.2.2102803584.1542767027; user_trace_token=20181121102346-794ca69c-ed34-11e8-af2a-525400f775ce; LGUID=20181121102346-794ca90c-ed34-11e8-af2a-525400f775ce; index_location_city=%E6%B7%B1%E5%9C%B3; _gid=GA1.2.417210577.1545100733; JSESSIONID=ABAAABAAAFCAAEGA2594CCC871A5C6033C439A7D767B848; _gat=1; LGSID=20181218212005-a2432f21-02c7-11e9-8f5b-5254005c3644; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1542767027,1545100734,1545139206; TG-TRACK-CODE=index_search; SEARCH_ID=3062075691be4d739e276ef7ea9921c1; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1545139212; LGRID=20181218212011-a5f61409-02c7-11e9-8f5b-5254005c3644'
                }
                proxies = {
                    "http": proxies_set.get_rand()
                }
                data = {
                    'first': 'false',
                    'pn': str(num),
                    'kd': 'python'
                }
                params = {
                    'city': '深圳',
                    'needAddtionalResult': False
                }
                res = requests.post(self.root_url, params = params, data = data, headers = headers, proxies = proxies, timeout = 3)
                url_list = url_generator(res)
                [pageurls_queue.put(url) for url in url_list]
                if res.status_code == 200:
                    print('success', str(num), proxies['http'])
                    break
                else:
                    print('status failed')
                    continue
            except requests.exceptions.ProxyError:
                proxies_set.remove(proxies['http'])
                print('ProxyError. Removing proxy:', proxies['http'])
                continue
            except requests.exceptions.ConnectTimeout:
                proxies_set.remove(proxies['http'])
                print('ConnectTimeout. Removing proxy:', proxies['http'])
                continue
            except Exception as e:
                traceback.format_exc()
                continue

    def main(self):
        for num in range(self.page_num):
            self.get_urls(num + 1)

if __name__ == '__main__':
    GetIps(100).main()
    engine = Engine(SERVER_ROOT_URL, 30)
    engine.main()
