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
        pass

    def handle_item(item_url):
        item_resp = requests.get(item_url, headers=headers)
        item_resp.encoding = 'GB2312'
        item_soup = BeautifulSoup(item_resp.text, 'lxml')
        item_soup = item_soup.find('span', {"id": "text110"})
        for item in item_soup.select('p'):
            joke_set.insert({"content": item.text})

    def get_list(list_url):
        list_resp = requests.get(list_url, headers=headers)
        list_resp.encoding = 'GB2312'
        list_soup = BeautifulSoup(list_resp.text, 'lxml')
        list_soup = list_soup.find('div', {"class": "list_title"})
        return list_soup.select('li > b > a[href]')

    def handle_list(list_url):
        joke_list = get_list(list_url)
        for item in joke_list:
            new_item_url = url + item.get('href')
            handle_item(new_item_url)
            break

    for each in soup.select('li > a[href]'):
        new_list_url = url + each.get('href')
        handle_list(new_list_url)
        break


spider1()
