import traceback
from bs4 import BeautifulSoup

from settings import *
from db.redis_session import *

jobdatas = RedisSet('jobdatas', host = REDIS_HOST, port = REDIS_PORT, db = REDIS_DB, password = REDIS_PWD)

def analyze_content(html_text):
    try:
        soup = BeautifulSoup(html_text, 'html5lib')

        job_names = soup.find_all(name = 'div', attrs = {"class": "job-name"})[0]
        name = job_names.attrs['title']
        company = job_names.find(name = 'div', attrs = {"class": "company"}).text

        job_requests = soup.find_all(name = 'dd', attrs = {"class": "job_request"})[0]
        request = "".join([i.text for i in job_requests.find_all(name = 'span')])

        job_detail = soup.select('#job_detail')[0]
        job_advantage = job_detail.select('.job-advantage p')[0].text

        job_description = [i.text for i in job_detail.select('.job_bt div p')]

        job_address = job_detail.select('.work_addr')[0].text.replace('\n', '').replace(' ', '').replace('查看地图', '')

        job_url = soup.find(name = 'link', attrs = {"rel": "canonical"}).attrs['href']

        job_data = {
            'name': name,
            'company': company,
            'request': request,
            'advantage': job_advantage,
            'description': job_description,
            'address': job_address,
            'url': job_url
        }

        jobdatas.add(job_data)
        return True
    except Exception as e:
        traceback.print_exc()
        return False
