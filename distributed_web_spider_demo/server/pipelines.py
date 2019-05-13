import requests
from pprint import pprint

def url_generator(response):
    '''
    :param response: class:`Response <Response>` object
    :return: :list:Details page URL list
    :rtype: list
    '''
    url_list = []
    for result in response.json()['content']['positionResult']['result']:
        url_list.append('https://www.lagou.com/jobs/{}.html'.format(result['positionId']))
    return url_list
