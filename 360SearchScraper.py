import requests
from bs4 import BeautifulSoup
from random import choice
import urllib.parse as parse
from time import sleep
from random import randint

KeywordList = ['搜狐体育']
UserAgentList = ['Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
                 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36']

def RandomUserAgent():
    UserAgent = choice(UserAgentList)
    UserAgent = {'User-Agent':UserAgent}
    return UserAgent

def StartUp():
    filename = input()
    filename = filename.strip()
    with open (filename,'r',encoding='utf-8') as ChinaKeywords:
        for line in ChinaKeywords:
            KeywordList.append(line.strip())

def Request(keyword):
    requestURL = '{}{}'.format('https://www.so.com/s?q=',keyword.replace(' ','+'))
    r = requests.get(requestURL,headers=RandomUserAgent())
    soup = BeautifulSoup(r.text,'lxml')
    return soup, keyword

def GetLinks(soup,keyword):
    ListOfResults = soup.findAll('li',attrs={'class':'res-list'})
    FinalResults = []
    for Result in ListOfResults:
        Result = Result.find('a',href=True)
        Result = Result['href']
        Result = parse.unquote(Result)
        SplitResult = Result.split('=')
        Result = SplitResult[1].replace('&q','')
        Result = '"{}"'.format(Result)
        FinalResults.append(Result)
    return FinalResults, keyword

def WriteToCSV(Finalresuts,keyword):
    with open('output.csv','a',encoding='utf-8') as output:
        Pages = ','.join(Finalresuts)
        FormattedKeyword = '"{}"'.format(keyword)
        OutPutString = '{},{}\n'.format(FormattedKeyword,Pages)
        output.write(OutPutString)

def main():
    StartUp()
    for key in KeywordList:
        Keyword = key
        a,b = Request(Keyword)
        c,d = GetLinks(a,b)
        WriteToCSV(c,d)
        sleep(randint(60,120))

main()
