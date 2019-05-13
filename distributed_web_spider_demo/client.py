import asyncio
import traceback

from settings import *

from db.redis_session import *
from client.downloader import *
from client.proxies import *

proxies_set = RedisSet('proxies', host = REDIS_HOST, port = REDIS_PORT, db = REDIS_DB, password = REDIS_PWD)
pageurls_queue = RedisQueue('pageurls', host = REDIS_HOST, port = REDIS_PORT, db = REDIS_DB, password = REDIS_PWD)

if __name__ == '__main__':
    # GetIps(100).main()
    tasks = []
    while True:
        if pageurls_queue.qsize() == 0:
            break
        url = pageurls_queue.get_nowait()
        url = url.decode('utf-8')

        header = {
            'User-Agent': random.sample(user_agent_list, 1)[0]
        }
        proxies = {}
        if 'https' in proxies_set.get_rand():
            proxies.update({
                "https": proxies_set.get_rand() if proxies_set.size() != 0 else ''
            })
        else:
            proxies.update({
                "http": proxies_set.get_rand() if proxies_set.size() != 0 else ''
            })

        tasks.append(asyncio.ensure_future(get_content(url, header, proxies)))
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
