from random import choice, randint
from time import sleep

import requests
from bs4 import BeautifulSoup


class BaiduScrape(object):

    def __init__(self, keyword, pages=5):

        self.base_url = 'http://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=0&rsv_idx=1&tn=baidu&wd={}'
        self.base_url_multi = 'http://www.baidu.com/s?wd={}&pn={}&oq=andrew%20wilson'
        self.keyword = keyword
        self.pages = pages
        self.final_urls = []
        self.failed_urls = []
        self.status = None


    def __random_header(self):
        desktop_agents = [
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/54.0.2840.99 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14',
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
        ]
        return {'User-Agent': choice(desktop_agents),
                       'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}

    def __make_request(self, url):
        try:
            r = requests.get(url=url, timeout=20)
            r.raise_for_status()
        except requests.exceptions.Timeout:
            r = requests.get(url=url, timeout=60)
        except requests.exceptions.ConnectionError:
            r = requests.get(url=url, timeout=60)
        except requests.exceptions.RequestException as e:
            raise e
        return r.url, r.text, r.status_code

    def __parse_page(self, html):
        links = []
        soup = BeautifulSoup(html, 'html.parser')
        all_titles = soup.find_all('h3', attrs={'class': 't'})
        for titles in all_titles:
            link = titles.find('a',href=True)
            if link is not None:
                links.append(link['href'])
        return links

    def get_results(self):
        i = 0
        urls = []
        while i < self.pages:
            if i == 0:
                url = self.base_url.format(self.keyword)
            else:
                pn = i * 10
                url = self.base_url_multi.format(self.keyword, pn)

            url, text, status = self.__make_request(url)
            if status == 200:
                temp_urls = self.__parse_page(text)
                for ui in temp_urls:
                    urls.append(ui)
                    print(urls)
            else:
                print(status)
                sleep(360)
                print('Fail sleeping')
                url, text, status = self.__make_request(url)
                if status == 200:
                    temp_urls = self.__parse_page(text)
                    for ui in temp_urls:
                        urls.append(ui)
            sleep(randint(30,90))
            i += 1
            print('Success sleeping')
        return urls

    def get_last_urls(self, urls):
        i = 0
        for url in urls:
            try:
                f_url, text, status = self.__make_request(url)
            except:
                f_url = url
            if 's.click.taobao.com' in f_url:
                pass
            else:
                with open('csv_output.csv', 'a', encoding='utf-8') as outfile:
                    outfile.write('"{}","{}","{}"\n'.format(self.keyword, f_url, i + 1))
                sleep(randint(3, 5))
                i += 1


    def action(self):
        urls = self.get_results()
        self.get_last_urls(urls)


if __name__ == '__main__':
    B = BaiduScrape('Andrew Wilson')
    B.action()
