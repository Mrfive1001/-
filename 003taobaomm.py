# -*-coding:utf-8-*-
# python2.7
import requests
from bs4 import BeautifulSoup
import urllib
import os
# 学会下载图片并且储存到文件里面


class Spider:
    def __init__(self):
        self.site_url = 'http://mm.taobao.com/json/request_top_list.htm'

    def get_page(self, page_num):
        url = self.site_url + '?page=' + str(page_num)
        print url
        response = requests.get(url)
        html = response.text
        return html

    def get_contents(self, page_num):
        html = self.get_page(page_num)
        soup = BeautifulSoup(html, 'html.parser')
        persons = soup.find_all('div',attrs={'class': 'personal-info'})
        result = [[0 for x in range(5)] for y in range(len(persons))]
        a = []
        temp = {'url': '', 'name': '', 'picture': '', 'age': '', 'address': ''}
        for i, person in enumerate(persons):
            image = person.find('a', attrs={'class': 'lady-avatar'})
            result[i][0] = 'http:' + image['href']
            result[i][1] = 'http:' + image.find('img')['src']
            per_info = person.find('p', attrs={'class', 'top'})
            result[i][2] = per_info.find('a').get_text()  # name
            result[i][3] = per_info.find('em').get_text() # age
            result[i][4] = per_info.find('span').get_text() # add
            a[-1:] = result[-1:]
        return result

    def print_me(self, page_num):
        persons = self.get_contents(page_num)
        for person in persons:
            for key in person:
                print key,
            print '\n'

    def save_head_img(self, image_url,filename):
        response = urllib.urlopen(image_url).read()
        f = open(filename, 'wb')
        f.write(response)
        f.close()

    def build_file(self, page):
        isExist = os.path.exists(page)
        if isExist:
            return False
        else:
            os.makedirs(page)

    def page_content(self,page_num):
        contents = self.get_contents(page_num)
        file = 'page' + str(page_num)
        self.build_file(file)
        head = file + '/'
        for content in contents:
            text_name = head+ content[2] + '.txt'
            image_name = head+content[2] + '.jpg'
            self.save_head_img(content[1], image_name)
            brief = "name:" +content[2]+'\n'
            brief += 'age:' +content[3]+'\n'
            brief += 'address:' +content[4]+'\n'
            self.save_brief(brief, text_name)

    def save_brief(self,content,filename):
            f = open(filename, 'w+')
            f.write(content.encode('utf-8'))
            f.close()

spy = Spider()
spy.print_me(1)
spy.page_content(1)
r = open('page1/1.txt', 'r')
lines = r.readlines()


def list_dic(lines):
    header = {}
    for line in lines:
        line = line.replace('\t',' ')
        line = line.replace('\n','')
        temp = line.split(' ', 1)
        try:
            header[temp[0]] = temp[1]
        except IndexError:
            print temp
    return header

print list_dic(lines)
