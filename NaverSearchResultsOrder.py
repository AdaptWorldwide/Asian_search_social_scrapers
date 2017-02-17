import requests
from bs4 import BeautifulSoup
from time import sleep
from random import randint,choice

failed_keywords = []
keywords = []

desktop_agents = ['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14',
                 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
                 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
                 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0']

def random_desktop_agent():
    agent = choice(desktop_agents)
    return {'User-Agent': agent}

def keyword_list(list):
    with open(list,'r',encoding='utf-8') as in_file:
        for line in in_file:
            line = line.strip()
            keywords.append(line)

def random_sleep(low,high):
    sleep(randint(low,high))

def make_request(keyword):
    url = 'https://search.naver.com/search.naver?where=nexearch&query={}&sm=top_hty&fbm=1&ie=utf8'.format(keyword.replace(' ','+'))
    try:
        r = requests.get(url,headers=random_desktop_agent())
        return r
    except:
        failed_keywords.append(keyword)
        return None

def get_h2s(keyword,response):
    soup = BeautifulSoup(response.text, 'lxml')
    to_return = []
    section_heads = soup.find_all('div', attrs={'class': 'section_head'})
    count = 1
    for section in section_heads:
        h2 = section.find('h2')
        h2 = h2.get_text()
        output_line = '"{}","{}","{}"\n'.format(keyword,count,h2)
        to_return.append(output_line)
        count += 1
    return to_return

def write_to_csv(list_of_lines):
    for line in list_of_lines:
        with open('KoreanOutput.csv','a',encoding='utf-8') as out_file:
            out_file.write(line)

def main():
    keyword_list('example.txt')
    for key in keywords:
        print(key)
        response = make_request(key)
        print(response)
        if response.status_code != 200:
            failed_keywords.append(key)
            print('Failed: ', key)
        else:
            try:
                output_list = get_h2s(key,response)
                write_to_csv(output_list)
            except:
                failed_keywords.append(key)
                print('Failed: ', key)
        random_sleep(30,60)
    for key in failed_keywords:
        response = make_request(key)
        if response == None:
            failed_keywords.append(key)
        else:
            try:
                output_list = get_h2s(key,response)
                write_to_csv(output_list)
            except:
                failed_keywords.append(key)
        random_sleep(30,60)

main()
