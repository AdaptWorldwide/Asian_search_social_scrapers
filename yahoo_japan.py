import datetime
import requests
from bs4 import BeautifulSoup
from random import choice, randint
from urllib.parse import urlparse
from time import sleep

base_url = 'https://search.yahoo.co.jp/search?p='

keywords_to_try = []
failed_keywords = []

UserAgentList = ['Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
                 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36']

def RandomUserAgent():
    UserAgent = choice(UserAgentList)
    UserAgent = {'User-Agent':UserAgent}
    return UserAgent

def make_request(keyword):
    keyword = keyword.strip()
    url = '{}{}'.format(base_url,keyword.replace(' ','+'))
    try:
        r = requests.get(url,headers=RandomUserAgent())
        return r
    except:
        failed_keywords.append(keyword)
        return None

def make_soup(response,keyword):
    if response.status_code != 200:
        failed_keywords.append(keyword)
        return None
    else:
        soup = BeautifulSoup(response.text,'lxml')
    return soup

def extract_results(soup):
    if soup != None:
        result_divs = soup.find_all('div', attrs={'class': 'hd'})
        result_urls = []
        for div in result_divs:
            result = div.find('a',href=True)
            result = result['href']
            result_urls.append(result)
    if len(result_urls) > 0:
        return result_urls
    else:
        return None

def domain_parse(string):
    try:
        parsed = urlparse(string)
        parsed = parsed.netloc
        return parsed
    except:
        return string

def print_results(keyword,results):
    i = 0
    while i < len(results):
        with open('output.csv','a',encoding='utf-8') as results_file:
            results_file.write('"{}","{}","{}","{}"\n'.format(keyword,results[i],domain_parse(results[i]),i+1))
        i += 1

def load_keywords(textfile):
    with open(textfile,'r',encoding='utf-8') as infile:
        for line in infile:
            line = line.strip()
            if line not in keywords_to_try:
                keywords_to_try.append(line)



def main():
    load_keywords('test.txt')
    for keyword in keywords_to_try:
        r = make_request(keyword)
        soup = make_soup(r, keyword)
        results = extract_results(soup)
        print_results(keyword, results)
        sleep(randint(20, 40))
    for keyword in failed_keywords:
        r = make_request(keyword)
        soup = make_soup(r, keyword)
        results = extract_results(soup)
        print_results(keyword, results)
        sleep(randint(20, 40))


main()
