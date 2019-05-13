import random
import requests
import asyncio
import traceback
import functools
from concurrent import futures

from server.proxies import *
from server.user_agent import *
from client.pipelines import *

proxies_set = RedisSet('proxies', host = REDIS_HOST, port = REDIS_PORT, db = REDIS_DB, password = REDIS_PWD)
pageurls_queue = RedisQueue('pageurls', host = REDIS_HOST, port = REDIS_PORT, db = REDIS_DB, password = REDIS_PWD)

executor = futures.ThreadPoolExecutor(max_workers = 10)

async def get_content(url, header, proxies):
    loop = asyncio.get_event_loop()
    try:
        response = await loop.run_in_executor(executor, functools.partial(requests.get, url = url, headers = header, proxies = proxies, timeout = 30))
        if response.status_code == 200:
            if analyze_content(response.text):
                print('Success crawl page: {}, {}, {}'.format(url, header, proxies))
            else:
                proxies_set.remove(list(proxies.values())[0])
                print('Analyze error. Removing proxy:', list(proxies.values())[0])
                pageurls_queue.put(url)
                print('Add page url to queue again.')
        else:
            proxies_set.remove(list(proxies.values())[0])
            print('Response error. Removing proxy:', list(proxies.values())[0])
            pageurls_queue.put(url)
            print('Add page url to queue again.')
    except Exception as e:
        proxies_set.remove(list(proxies.values())[0])
        traceback.print_exc()
        print('Removing proxy:', list(proxies.values())[0])
        pageurls_queue.put(url)
        print('Add page url to queue again.')
