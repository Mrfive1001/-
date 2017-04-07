#python2.7
import requests
from bs4 import BeautifulSoup
DOWNLOAD_URL = 'http://movie.douban.com/top250/'


def find_all_pages(start_html):
    soup = BeautifulSoup(start_html, "html.parser")
    pages = soup.find('div', attrs={'class': 'paginator'})
    pages = pages.find_all('a')
    pages.pop(-1)
    pages_after = []
    for page in pages:
        string_after = DOWNLOAD_URL + page['href']
        pages_after.append(string_after)
    pages_after.insert(0,DOWNLOAD_URL)
    return pages_after


def get_html(url):
    data = requests.get(url).content
    return data


def parse_txt(html):
    soup = BeautifulSoup(html, "html.parser")
    movie_list = soup.find('ol', attrs={'class': 'grid_view'})
    movie_name_list = movie_list.find_all('li')
    for name in movie_name_list:
        movie = name.find('div',attrs = {'class': 'hd'})
        movie_name = movie.find('span',attrs = {'class','title'}).string
        movie_url = movie.find('a')['href']
        print movie_name, movie_url


def one_page(url):
    html = get_html(url)
    parse_txt(html)


def main():
    html = get_html(DOWNLOAD_URL)
    all_pages = find_all_pages(html)
    for all_page in all_pages:
        one_page(all_page)


if __name__ == '__main__':
    main()
