from selenium import webdriver
from bs4 import BeautifulSoup
from random import choice
from time import sleep
from random import randint

KeyList = []
AgentList = ['Mozilla/5.0 (iPhone; CPU iPhone OS 6_1_4 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10B350 Safari/8536.25',
             'Mozilla/5.0 (iPhone; CPU iPhone OS 7_0 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Mobile/11A465 Twitter for iPhone',
             'Mozilla/5.0 (iPhone; CPU iPhone OS 7_0 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11A465 Safari/9537.53']

def StartUp():
    File = input()
    with open(File,'r',encoding='utf-8') as keywords:
        for keyword in keywords:
            keyword = keyword.strip()
            KeyList.append(keyword)

def RandomAgent():
    return choice(AgentList)

def GetResults(keyword):
    webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.customHeaders.User-Agent'] = RandomAgent()
    driver = webdriver.PhantomJS(executable_path='C:\\Users\\EdmundJMartin\\Desktop\\bin\\phantomjs')
    driver.set_window_size(357,667)
    URL = '{}{}{}'.format('http://m.sm.cn/s?q=',keyword.replace(' ','%20'),'&from=smor&safe=1&snum=0')
    driver.get(URL)
    sleep(5)
    element = driver.find_element_by_id('pager')
    element.click()
    sleep(10)
    #driver.get_screenshot_as_file('something.png')
    html = driver.page_source
    return html

def ParseHTML(html):
    soup = BeautifulSoup(html,'lxml')
    resultCards = soup.findAll('div',attrs={'class':'result'})
    RankingURLs = []
    for card in resultCards:
        result = card.find('a',href=True)
        result = result['href']
        RankingURLs.append(result)
    return RankingURLs

def WriteToCSV(Finalresuts,keyword):
    with open('output.csv','a',encoding='utf-8') as output:
        Pages = ','.join(Finalresuts)
        FormattedKeyword = '"{}"'.format(keyword)
        OutPutString = '{},{}\n'.format(FormattedKeyword,Pages)
        output.write(OutPutString)

def main():
    StartUp()
    for keyword in KeyList:
        a = GetResults(keyword)
        b = ParseHTML(a)
        WriteToCSV(b,keyword)
        sleep(randint(10,30))

main()
