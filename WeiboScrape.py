from SecretClientInfo import Keys2
from random import choice
import selenium.webdriver as webdriver
from time import sleep
from bs4 import BeautifulSoup
import re


AccountsToScrape = ['example1','example2']
User = Keys2.get('User')
Pass = Keys2.get('Password')
print(User)
print(Pass)

driver = webdriver.Chrome()
driver.set_window_size(1366,768)


def RandomAgent():
    return choice(AgentList)

def WeiboLogin():
    driver.get('http://www.weibo.com/login.php')
    LoginID = driver.find_element_by_id('loginname')
    LoginID.send_keys(User)
    Password = driver.find_element_by_class_name('enter_psw')
    Password.click()
    PasswordActive = driver.find_element_by_class_name('W_input_focus')
    PasswordActive.send_keys(Pass)
    LoginButton = driver.find_element_by_class_name('login_btn')
    sleep(5)
    LoginButton.click()

def GetStatsPage1(url):
    driver.get('{}{}'.format('http://www.weibo.com/',url))
    sleep(5)
    driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
    sleep(20)
    driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
    sleep(20)
    html = driver.page_source
    with open('html.html','w',encoding='utf-8') as output:
        output.write(html)

def GetStatsPage2(url):
    driver.get('{}{}{}'.format('http://www.weibo.com/',url,'?is_search=0&visible=0&is_hot=1&is_tag=0&profile_ftype=1&page=2#feedtop'))
    sleep(5)
    driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
    sleep(20)
    driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
    sleep(20)
    html = driver.page_source
    with open('html.html', 'w', encoding='utf-8') as output:
        output.write(html)

def GetStatsPage3(url):
    driver.get('{}{}{}'.format('http://www.weibo.com/',url,'?is_search=0&visible=0&is_hot=1&is_tag=0&profile_ftype=1&page=3#feedtop'))
    sleep(5)
    driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
    sleep(20)
    driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
    sleep(20)
    html = driver.page_source
    with open('html.html', 'w', encoding='utf-8') as output:
        output.write(html)



def Extract():
    html = open('html.html', 'r', encoding='utf-8')
    soup = BeautifulSoup(html, 'lxml')

    AttrRegex = re.compile('ouid=(\d){0,10}')
    posts = soup.findAll('div', attrs={'tbinfo': AttrRegex})
    for post in posts:
        try:
            Page = post.find('div', attrs={'class': 'WB_info'})
            Page = Page.text
            Page = Page.strip()
        except:
            pass
        try:
            PostTitle = post.find('div', attrs={'class': 'WB_text'})
            PostTitle = PostTitle.text
            PostTitle = PostTitle.strip()
            # print(PostTitle)
        except:
            pass
        try:
            date = post.find('div', attrs={'class': 'WB_from'})
            date = date.text
            date = date.strip()
        except:
            pass
        try:
            ImportantData = post.find('div', attrs={'class': 'WB_feed_handle'})
            Items = ImportantData.findAll('li')
            Repost = Items[1]
            Repost = Repost.text
            Repost = Repost.strip()
            Comments = Items[2]
            Comments = Comments.text
            Comments = Comments.strip()
            Likes = Items[3]
            Likes = Likes.text
            Likes = Likes.strip()
            print(Page, PostTitle, Repost, Comments, Likes)
            with open('Ed.txt', 'a', encoding='utf-8') as file:
                CSVString = '"{}","{}","{}","{}","{}","{}"\n'.format(Page, PostTitle, date, Repost, Comments, Likes)
                file.write(CSVString)
        except:
            pass


def main():
    WeiboLogin()
    for account in AccountsToScrape:
        GetStatsPage1(account)
        Extract()
        try:
            GetStatsPage2(account)
            Extract()
        except:
            pass
        try:
            GetStatsPage3(account)
            Extract()
        except:
            pass

main()
