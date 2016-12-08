from bs4 import BeautifulSoup
import requests
from random import choice
from random import randint
from time import sleep

#Globals
BaseURL = 'http://search.daum.net/search?w=blog&nil_search=btn&DA=NTB&enc=utf8&q='

UserAgentList = ['Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
                 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36']

def RandomUserAgent():
    UserAgent = choice(UserAgentList)
    UserAgent = {'User-Agent':UserAgent}
    return UserAgent


def GetResults(keyword):
    keyword = keyword.strip()
    keyword = keyword.replace(' ','+')
    r = requests.get('{}{}'.format(BaseURL,keyword),headers=RandomUserAgent())
    return r.text

def GetSoup(html):
    soup = BeautifulSoup(html,'html.parser')
    return soup

def GetLinks(soup):
    resultBoxes = soup.findAll('div',attrs={'class':'cont_inner'})
    Results = []
    for resultBox in resultBoxes:
        Result = resultBox.find('a',href=True)
        Result = Result['href']
        if not 'http://keyword.daumdn.com' in Result:
            Results.append(Result)
    return Results

def GetTitles(soup):
    titleResults = soup.findAll('div',attrs={'wrap_tit'})
    Titles = []
    for title in titleResults:
        title = title.text
        title = title.strip()
        Titles.append(title)
    return Titles

def PrettyPrint(keyword,titles,results):
    r = len(results)
    i = 0
    while i < r:
        with open('OtherFormat.csv','a',encoding='utf-8') as pretty:
            pretty.write('"{}","{}","{}","{}"\n'.format(keyword,i+1,results[i],titles[i]))
        i += 1

def PrintToCSV(results,keyword):
    results = '","'.join(results)
    KeyResults = '"{}",{}"\n'.format(keyword,results)
    with open('DaumBlog.txt','a',encoding='utf-8') as DaumResults:
        DaumResults.write(KeyResults)

def main():
    for keyword in open('keywords.txt','r',encoding='utf-8'):
        keyword = keyword.strip()
        a = GetResults(keyword)
        b = GetSoup(a)
        c = GetLinks(b)
        d = GetTitles(b)
        PrettyPrint(keyword,d,c)
        sleep(randint(20,40))

main()
