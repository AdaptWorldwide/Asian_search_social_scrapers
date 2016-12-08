from selenium import webdriver
from bs4 import BeautifulSoup
from ClientInfo import Keys
from time import sleep

AccountsToScrape = []

#Globals
driver = webdriver.Chrome()
driver.set_window_size(1366,768)

def KakaoLogin():
    driver.get('https://story.kakao.com/s/login')
    sleep(10)
    UserName = Keys.get('User')
    Password = Keys.get('Password')
    Login = driver.find_element_by_xpath('//*[@id="u_id"]')
    Login2 = driver.find_element_by_xpath('//*[@id="u_pass"]')
    LoginButton = driver.find_element_by_xpath('//*[@id="kakaoContent"]/div[2]/form/fieldset/a')
    Login.send_keys(UserName)
    Login2.send_keys(Password)
    LoginButton.click()

def KakaoGrabPage(page):
    sleep(10)
    driver.get('{}{}'.format('https://story.kakao.com/ch/',page))
    scrolls = 0
    while scrolls < 50:
        driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
        sleep(10)
        scrolls += 1
    html = driver.page_source
    return html

def GetPerformance(html):
    soup = BeautifulSoup(html,'html.parser')
    Posts = soup.find_all('div',attrs={'class':'_activity'})
    for post in Posts:
        PageName = post.find(attrs={'class':'pf_name'})
        PageName = PageName.text
        PostTitle = post.find('div',attrs={'class':'_content'})
        PostTitle = PostTitle.text
        Date = post.find('a',attrs={'class':'time'})
        Date = Date.text
        LikeCount = post.findAll(attrs={'class':'_likeCount'})
        LikeCount = LikeCount[0].text
        CommentCount = post.findAll(attrs={'class': '_commentCount'})
        CommentCount = CommentCount[0].text
        ShareCount = post.findAll(attrs={'class':'_storyShareCount'})
        ShareCount = ShareCount[0].text
        UpCount = post.findAll('a',attrs={'class':'_btnViewSympathyList'})
        UpCount = UpCount[0].text
        moreLike = post.findAll(attrs={'class':'_moreLike'})
        moreLike = moreLike[0].text
        print(PageName,PostTitle,Date,LikeCount,CommentCount,ShareCount,UpCount,moreLike)
        with open('Output.csv','a',encoding='utf-8') as OutFile:
            OutFile.write('"{}","{}","{}","{}","{}","{}","{}","{}"\n'.format(PageName,PostTitle,Date,LikeCount,CommentCount,ShareCount,UpCount,moreLike))



KakaoLogin()
a = KakaoGrabPage('kakaostory')
GetPerformance(a)
