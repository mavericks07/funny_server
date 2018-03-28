import re
import redis
import requests
from bs4 import BeautifulSoup
from lxml.html import etree
from pymongo import MongoClient

conn = MongoClient('127.0.0.1', 27017)
db = conn.funny
joke_set = db.joke

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/56.0.2924.87 Safari/537.36',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,',
           'Accept-Encoding': 'gzip, deflate',
           'Accept-Language': 'zh-CN,zh;q=0.9'
           }

r = redis.Redis(host='127.0.0.1', port=6379, db=1)


def spider1():
    """
    开心一刻网爬虫
    """
    url = 'http://www.jokeji.cn'
    resp = requests.get(url=url, headers=headers)
    resp.encoding = 'GB2312'
    soup = BeautifulSoup(resp.text, 'lxml')
    soup = soup.find("div", {"class": "joketype l_left"})

    def get_item(item_url):
        if r.sismember('down', item_url):
            print(f'已经抓取过:{item_url}')
            return 0
        item_resp = requests.get(item_url, headers=headers)
        item_resp.encoding = 'GB2312'
        item_soup = BeautifulSoup(item_resp.text, 'lxml')
        item_soup = item_soup.find('span', {"id": "text110"})
        item_soup = item_soup.select('p')
        if not item_soup:
            return 0
        for item in item_soup:
            content = item.text[2:]
            if len(content) > 20:
                print(content)
                joke_set.insert({"content": item.text[2:]})
                joke_set.insert({"from": item_url})
                r.sadd('down', item_url)
            else:
                r.sadd('fail', item_url)

    def get_list(list_url):
        list_resp = requests.get(list_url, headers=headers)
        list_resp.encoding = 'GB2312'
        list_soup = BeautifulSoup(list_resp.text, 'lxml')
        list_soup = list_soup.find('div', {"class": "list_title"})
        return list_soup.select('li > b > a[href]')

    def get_page_nums(list_url):
        list_resp = requests.get(list_url, headers=headers)
        list_resp.encoding = 'GB2312'
        list_soup = BeautifulSoup(list_resp.text, 'lxml')
        list_soup = list_soup.find('div', {"class": "next_page"})
        last_url = list_soup.find_all("a")[-1].get('href')
        page_nums_groups = re.search(r'.*_(\d*).*', last_url).groups()
        if not page_nums_groups:
            return 0
        page_nums = int(page_nums_groups[0])

        return page_nums

    def handle_list(list_url):
        page_nums = get_page_nums(list_url)
        for num in range(1, page_nums+1):
            print(num)
            list_url = re.sub(r'_\d*', f'_{num}', list_url)
            joke_list = get_list(list_url)
            for item in joke_list:
                new_item_url = url + item.get('href')
                get_item(new_item_url)

    for each in soup.select('li > a[href]'):
        new_list_url = url + each.get('href')
        handle_list(new_list_url)


spider1()

