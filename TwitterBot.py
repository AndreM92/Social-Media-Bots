from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.common.exceptions import *

from datetime import datetime

from bs4 import BeautifulSoup
import lxml
import time
import numpy as np
import pandas as pd


driver = webdriver.Chrome('[path to your driver]\chromedriver.exe')
driver.maximize_window()
loginpage = r'https://twitter.com/i/flow/login'

# Login process
email = '[Your registered Email]'
username = '[your username]'
password = '[your password]'

def login(email,password):
    driver.get(loginpage)
    np = '/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input'
    WebDriverWait(driver,5).until(EC.presence_of_element_located(('xpath',np)))
    nameslot = driver.find_element('xpath',np)
    nameslot.click()
    nameslot.clear()
    nameslot.send_keys(email)
    time.sleep(1)
    driver.find_element('xpath','//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]/div').click()
    pp = '/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input'
    WebDriverWait(driver, 5).until(EC.presence_of_element_located(('xpath',pp)))
    pwslot = driver.find_element('xpath',pp)
    pwslot.clear()
    pwslot.send_keys(password)
    time.sleep(1)
    driver.find_element('xpath','//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div/div').click()

login(email,password)

########################################################################################################################
# Troubleshooting
# 'abnormal activities'
time.sleep(2)
if driver.current_url == 'https://twitter.com/i/flow/login':
    input = driver.find_element('xpath','//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/label/div/div[2]/div/input')
    input.clear()
    input.send_keys(username)
    time.sleep(1)
    driver.find_element('xpath','//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/div/div').click()
    time.sleep(1)
    pwslot = driver.find_element('xpath','//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input')
    pwslot.clear()
    pwslot.send_keys(password)
    time.sleep(1)
    driver.find_element('xpath','//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div/div').click()

# Refuse Cookies
dp = '//*[@id="layers"]/div/div/div/div/div/div[2]/div[2]/div'
WebDriverWait(driver,5).until(EC.presence_of_element_located(('xpath',dp)))
driver.find_element('xpath','//*[@id="layers"]/div/div/div/div/div/div[2]/div[2]/div').click()

# Banner: "Mitteilungen aktivieren"
if driver.find_element('xpath',"//*[text()='Mitteilungen aktivieren']"):
    driver.find_element('xpath',"//*[text()='Nicht jetzt']").click()

########################################################################################################################
# Searching Process on Twitter
examObject = 'Bosch einfach heizen'

def search(x):
    startpage = driver.current_url
    try:
        searchbox = driver.find_element('xpath','//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[2]/div/div[2]/div/div/div/div[1]/div/div/div/form/div[1]/div/div/div/label/div[2]/div/input')
    except:
        searchbox = driver.find_element(By.CSS_SELECTOR,'input')
    action = ActionChains(driver)
    action.double_click(searchbox).perform()
    searchbox.send_keys(Keys.BACKSPACE)
    searchbox.send_keys(x)
    time.sleep(1)
    searchbox.send_keys(Keys.ENTER)
    time.sleep(2)
    # click on the first result
    try:
        driver.find_element('xpath','//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/section/div/div/div[5]/div/div/div/div/div[2]/div[1]/div[1]/div/div[1]/a/div/div[1]/span/span').click()
    except:
        driver.find_element(By.LINK_TEXT, examObject).click()

search(examObject)

###############################################################################
# Scrape the profile stats

class ScrapedProfile:
    def __init__(self):
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'css-1dbjc4n')))
        # to prevent errors:
        self.name, self.follower, self.following, self.tweets, self.desc, self.links = ['' for i in range(0, 6)]
        self.url = driver.current_url

        soup = BeautifulSoup(driver.page_source, 'lxml')
        header = soup.find('div', class_='css-1dbjc4n r-1ifxtd0 r-ymttw5 r-ttdzmv')
        dlist = [i.text for i in header.find_all('span', class_='css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0')]

        self.name = dlist[1]
        self.follower = [i for i in dlist if i[0].isdigit()][1]
        self.following = [i for i in dlist if i[0].isdigit()][0]
        self.tweets = soup.find('div',class_='css-901oao css-1hf3ou5 r-14j79pv r-37j5jr r-n6v787 r-16dba41 r-1cwl3u0 r-bcqeeo r-qvutc0').text.split(' ')[0]
        self.desc = ' '.join(dlist[3:]).replace('\n', ' ').replace('  ', ' ')
        self.links = [l['href'] for l in header.find_all('a', href=True) if l['href'][:5] == 'https']

pr = ScrapedProfile()
# I'm creating an empty DataFrame with the profile stats
header = ['name','url','follower','following','tweets', 'description','links']
dfProfiles = pd.DataFrame(columns = header)
print(dfProfiles)

# Run this for every profile you want to scrape (after moving to the target page)
s = ScrapedProfile()
data = [s.name,s.url,s.follower,s.following,s.tweets,s.desc,s.links]
dfProfiles.loc[len(dfProfiles)] = data

# Export to Excel
path = "C:\\Users\\andre\\Documents\Python\Web_Scraper\Social-Media-Bots\TwitterProfiles.xlsx"
with pd.ExcelWriter(path, engine='openpyxl') as writer:
    dfProfiles.to_excel(writer,sheet_name='Profile Stats')
    
###############################################################################   
# Scraper function for the posts with an integrated scrolling function
# It scrapes the details of the posts after every scroll, filters the results and appends them to a datalist
# I've set a limit of 200 scrolls and prompted it to stop when it reaches the year 2021 to prevent infinite scrolling.

def PostScraper():
    postdata = []
    datelist = []
    scrheight = driver.execute_script('return document.body.scrollHeight')
    scrolls = 0
    while True:
        # Scraping function
        soup = BeautifulSoup(driver.page_source, 'lxml')
        posts = soup.find_all('article')
        for p in posts:
            date, tweet_type, content, likes, retweets, comments, video, images, imagelinks, links, rawtext = ['' for i in range(0, 11)]
            date = p.find('time')['datetime']
            try:
                rawtext = p.text
            except:
                pass
            if 'retweet' in rawtext.lower():
                tweet_type = 'retweet'
            else:
                tweet_type = 'tweet'
            try:
                content = p.find('div',class_='css-901oao r-18jsvk2 r-37j5jr r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-bnwqim r-qvutc0').text.replace('\n',' ').replace('  ', ' ')
            except:
                pass
            interactions = [i.div['aria-label'] for i in p.find_all('div',class_='css-1dbjc4n r-18u37iz r-1h0z5md') if 'aria-label' in str(i.div)]
            likes = interactions[-2].split(' ')[0]
            retweets = interactions[-3].split(' ')[0]
            comments = interactions[-4].split(' ')[0]
            imagelinks = [i['src'] for i in p.find_all('img') if not 'emoji' in i['src'] and not 'profile' in i['src'] and not '_video' in i['src']]
            images = len(imagelinks)
            html = str(p).lower()
            if 'video' in html or 'livestream' in html:
                video = 1
            links = [l['href'] for l in p.find_all('a', href=True) if 'http' in l['href']]

            row = [date,tweet_type,content,likes,retweets,comments,video,images,imagelinks,links,rawtext]
            if str(date) not in datelist and '2021' not in str(date):
                postdata.append(row)
                datelist.append(str(date))

        # Scrolling function by pixel numbers
        # (if you scroll to the bottom of the page, some posts will be lost)
        if scrolls >= 200 or '2021' in str(date):
            break
        driver.execute_script("window.scrollBy(0,2000)", "")
        scrolls += 1
        time.sleep(2)

    return postdata

data = []
data = PostScraper()

# Scroll and scrape further and append the posts:
data = data + PostScraper()

# Create a DataFrame when you're done scraping
header=['date','tweet_type','content','likes','retweets','comments','video','images','imagelinks','links','rawtext']
dfPosts = pd.DataFrame(data,columns = header)

# Export to Excel
path = "C:\\Users\\andre\\Documents\Python\Web_Scraper\Social-Media-Bots\TwitterPosts.xlsx"
with pd.ExcelWriter(path, engine='openpyxl') as writer:
    dfPosts.to_excel(writer,sheet_name=examObject)
