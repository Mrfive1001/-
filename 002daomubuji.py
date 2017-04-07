# -*-coding:gbk-*-
# python2.7
import requests
from bs4 import BeautifulSoup
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

f = open('read.txt', 'w+')
base_url = 'http://www.lread.net/read/70/'
url = 'http://www.lread.net/read/70/48150.html'

response = requests.get(url)
response.encoding = 'GBK'
html = response.text

soup = BeautifulSoup(html, 'html.parser')
next = soup.find('a',string =u'下一章')
if next:
    next = base_url + next['href']
content = soup.find('div',attrs={'class': 'content'})
if content:
    title = soup.find('div',attrs={'class': 'bookname'}).find('h1')
    title = title.get_text()
    tags = content.find_all(True)
    for tag in tags:
        tag.clear()
    content = content.get_text()
    content = content.replace(u'\xa0'*4, '\n')
    f.write(title)
    f.write(content)

f.close()


