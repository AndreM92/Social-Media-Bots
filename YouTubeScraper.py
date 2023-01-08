from selenium import webdriver
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup
import time
import numpy as np
import pandas as pd

driver = webdriver.Chrome('[Your Path]\chromedriver.exe')
driver.maximize_window()

target = 'https://www.youtube.com/c/WOLFDeutschland'
driver.get(target)

# Cookie Banner
driver.find_element(By.XPATH,'//*[@id="yDmH0d"]/c-wiz/div/div/div/div[2]/div[1]/div[3]/div[1]/form[1]/div/div/button/span').click()
time.sleep(2)

########################################################################################################################
# Account stats
def accountStats():
    statslink = target + '/about'
    driver.get(statslink)
    time.sleep(2)
    username = driver.find_element('xpath','//*[@id="text"]').text
    subscriber = driver.find_element(By.ID,'subscriber-count').text.split(' ')[0]
    views = driver.find_element('xpath','//*[@id="right-column"]/yt-formatted-string[3]').text.split(' ')[0]
    joined = driver.find_element('xpath','//*[@id="right-column"]/yt-formatted-string[2]/span[2]').text
    accdesc = driver.find_element('xpath','//*[@id="description-container"]').text.replace('\n',' ').replace('  ',' ').replace('Beschreibung ','')

    return [username,target,subscriber,views,joined,accdesc]

account = accountStats()

dfAccount = pd.DataFrame(columns = ['username','url','subscriber','totalviews','joined','description'])
dfAccount.loc[len(dfAccount)] = account

########################################################################################################################
# Collect all the videolinks after one scroll
startlink = target + '/videos'
driver.get(startlink)
time.sleep(2)
driver.execute_script("window.scrollBy(0,3000)", "")
time.sleep(3)
soup = BeautifulSoup(driver.page_source,'lxml')
videos = soup.find_all('div',{'id':'details'})
videolinks = ['https://www.youtube.com' + v.find('a',href=True)['href'] for v in videos if v.find('a',href=True)]
print(len(videolinks))

########################################################################################################################
def videoScraper(l):
    driver.get(l)
    time.sleep(2)
    driver.execute_script("window.scrollBy(0,500)", "")
    time.sleep(1)
    driver.find_element(By.XPATH, '//*[@id="expand"]').click()
    time.sleep(2)
    date, title, views, likes, comments, links, desc = ['' for e in range(0,7)]
    soup = BeautifulSoup(driver.page_source,'lxml')
    title = soup.find('h1',class_='style-scope ytd-watch-metadata').text.strip()
    likes = soup.find('div',{'id':'segmented-like-button'}).text.split(' ')[0].strip()
    if likes.isdigit() == False:
        likes = ''.join([t for t in soup.find('div',{'id':'segmented-like-button'}).text if t.isdigit()])
    desc = soup.find('div',{'id':'description'}).text.strip().replace('\n',' ').replace('  ',' ')
    links = [l for l in desc.split(' ') if l[:4].lower() == 'http']
    infocontainer = [e for e in soup.find('div',{'id':'info-container'}).find_all('span') if e.text != ' ']
    if len(infocontainer) == 2:
        views = infocontainer[0].text.split(' ')[0]
        date = infocontainer[1].text
    if date.isdigit() == False and len(date) >= 1:
        date = date.split(' ')[-1]
    try:
        comments = driver.find_element('xpath', '//*[@id="count"]/yt-formatted-string/span[1]').text
    except:
        try:
            comments = driver.find_element('xpath', '//*[@id="message"]/span').text.split(' ')[-1]
        except:
            pass

    return [date,l,title,views,likes,comments,links,desc]


data = []
for l in videolinks:
    row = videoScraper(l)
    if '2021' in row[0]:
        break
    data.append(row)

header=['date','url','title','views','likes','comments','links','description']
dfVideos = pd.DataFrame(data,columns=header)

examObject = target.split('/')[-1]
path = "C:\\Users\\andre\\Documents\Python\Web_Scraper\Social-Media-Bots\YouTubeResults.xlsx"
with pd.ExcelWriter(path, engine='openpyxl') as writer:
    dfAccount.to_excel(writer,sheet_name='overview')
    dfVideos.to_excel(writer,sheet_name=examObject)