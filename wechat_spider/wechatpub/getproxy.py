import requests
from bs4 import BeautifulSoup
import threading
import queue

class Get_ips():
    def __init__(self, page):
        self.ips = []
        self.urls = []
        for i in range(page):
            self.urls.append('http://www.xicidaili.com/nn/%s'%i)
        self.header = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36'
        }
        self.q = queue.Queue()
        self.Lock = threading.Lock()

    def get_ips(self):
        for url in self.urls:
            res = requests.get(url, headers = self.header)
            soup = BeautifulSoup(res.text, 'html5lib')
            ips = soup.find_all('tr')
            for i in range(1, len(ips)):
                ip = ips[i]
                tds = ip.find_all('td')
                ip_temp = 'http://' + tds[1].contents[0] + ':' + tds[2].contents[0]
                self.q.put(str(ip_temp))

    def review_ips(self):
        while not self.q.empty():
            ip = self.q.get()
            try:
                proxy = {'http': ip}
                res = requests.get('http://www.baidu.com', proxies = proxy, timeout = 3)
                self.Lock.acquire()
                if res.status_code == 200:
                    self.ips.append(ip)
                    print(ip)
                    self.Lock.release()
                else:
                    print('Time Out!')
                    self.Lock.release()
            except Exception:
                pass

    def main(self):
        self.get_ips()
        threads = []
        for i in range(40):
            threads.append(threading.Thread(target = self.review_ips, args = []))

        for t in threads:
            t.start()

        for t in threads:
            t.join()
        return self.ips

if __name__ == '__main__':
    from pymongo import MongoClient

    conn = MongoClient('127.0.0.1', 27017)
    db = conn.WetchatSpider
    ProxyPool_set = db.ProxyPool_set
    proxyObj = Get_ips(10)
    proxy_list = proxyObj.main()
    i = 0
    for proxy in proxy_list:
        ProxyPool_set.insert({str(i): proxy})
        i += 1
    conn.close()
