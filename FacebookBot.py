# -*- coding: utf-8 -*-
"""
Created on Mon Oct 10 11:20:14 2022

@author: andre
"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC
from selenium.common.exceptions import *
import pyautogui

from bs4 import BeautifulSoup
import lxml
import time
import pandas as pd

# Imports for fixing the driver bug (Window closes unintended)
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Driverbug function
def fixDriverbug():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    driver.get(loginpage)
    time.sleep(1)
    if loginpage != driver.current_url:
        print('There is something wrong with the page')
        
###############################################################################
# Login process
# Get to the login page
driver = webdriver.Chrome('[path to your driver]\chromedriver.exe')
driver.maximize_window()
loginpage = r'https://www.facebook.com/'
driver.get(loginpage)
time.sleep(1)
if loginpage != driver.current_url:
    fixDriverbug()
    
# Click through the first cookie-banner
WebDriverWait(driver,5).until(EC.presence_of_element_located((By.CLASS_NAME,'_3ixn')))
driver.find_element('xpath','/html/body/div[3]/div[2]/div/div/div/div/div[3]/button[1]').click()

# Push your Name and Password to the Website and login
username = '[your username]'
password = '[your password]'

def login(username,password):
    WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[1]/div[1]/div[1]/div/div/div/div[1]/div/img')))
    nameslot = driver.find_element('xpath','/html/body/div[1]/div[1]/div[1]/div/div/div/div[2]/div/div[1]/form/div[1]/div[1]/input')
    nameslot.clear()                        
    nameslot.send_keys(username)
    pwslot = driver.find_element('xpath','/html/body/div[1]/div[1]/div[1]/div/div/div/div[2]/div/div[1]/form/div[1]/div[2]/div/input')
    pwslot.clear()
    pwslot.send_keys(password)
    driver.find_element('xpath','/html/body/div[1]/div[1]/div[1]/div/div/div/div[2]/div/div[1]/form/div[2]/button').click()

try:
    login(username,password)
except:
    try:
        time.sleep(1)
        login(username,password)
    except Exception as e:
        print(repr(e))

###############################################################################        
# Searching process on Facebook
examObject = 'comdirect'

def getprofile(examObject):
    try:
        searchbox = driver.find_element('xpath','/html/body/div[1]/div/div[1]/div/div[2]/div[2]/div/div/div/div/div/label/input')
    except NoSuchElementException:
        searchbox = driver.find_element(By.CSS_SELECTOR,"[aria-label^='Facebook durchsuchen']")
    searchbox.click()
    searchbox.clear()
    searchbox.send_keys(examObject)
    time.sleep(1)
    searchbox.send_keys(Keys.ENTER)
    # Find and click on the first result
    WebDriverWait(driver,5).until(EC.presence_of_element_located((By.CLASS_NAME,'x1heor9g')))
    try:
        result1 = '//*[@id="mount_0_0_5D"]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div[2]/div/div/div/div/div/div[1]/div/div/div/div/div/div/div/div/div[1]/div/div[2]/div/div[1]/h2/span/span/span/a/span[1]'
        driver.find_element('xpath',result1).click()
    except NoSuchElementException:
        try:
            time.sleep(1)
            soup = BeautifulSoup(driver.page_source,'lxml')   
            fburl = soup.find('span',class_='xt0psk2').find('a')['href']
            print(fburl)
            driver.get(fburl)
        except:
            pyautogui.moveTo(806,301)
            pyautogui.click()         
            # Or insert your examObject manually
            # driver.find_element(By.CSS_SELECTOR,"[aria-label^=comdirect]").click()
        
getprofile(examObject)

# check if you are on the right page
def checkpage():
    try:
        WebDriverWait(driver,5).until(EC.presence_of_element_located((By.CLASS_NAME,'x1heor9g')))
    except:
        pass
    if not examObject in driver.current_url:
        if 'data_policy' in driver.current_url:
            pyautogui.moveTo(1855,188)
            pyautogui.click()
        else:
            pyautogui.moveTo(25,62)
            pyautogui.click()
        WebDriverWait(driver,5).until(EC.presence_of_element_located((By.CLASS_NAME,'xe3v8dz')))
        getprofile(examObject)
        time.sleep(2)
checkpage()

###############################################################################
# Scrape the profile stats

class ScrapedProfile:
    def __init__(self):
        try:
            WebDriverWait(driver,5).until(EC.presence_of_element_located((By.CLASS_NAME,'x1heor9g')))
        except:
            pass
        # to prevent errors:
        self.pagelikes,self.follower,self.visits,self.desc = ['' for i in range(0,4)]
        self.url = driver.current_url
        soup = BeautifulSoup(driver.page_source,'lxml')
        try:
            stats = [s.text for s in soup.find_all('span',class_='x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x6prxxf xvq8zen xo1l8bm xzsf02u') if s.text[:1].isdigit()]
            self.pagelikes = stats[0].split(' ')[0]
            self.follower = stats[1].split(' ')[0]
            self.visits = stats[2].split(' ')[0]
            self.desc = soup.find_all('div',class_='x11i5rnm xat24cr x1mh8g0r x1vvkbs xdj266r')[1].text
            self.links = [l['href'] for l in soup.find('div',class_='x1yztbdb').find_all('a',href=True)]
        except Exception as e:
            print(repr(e))
            pass

pr = ScrapedProfile()
# I'm creating my first DataFrame with the profile stats
data = [examObject,pr.url,pr.pagelikes,pr.follower,pr.visits,pr.desc,pr.links]
dfProfiles = pd.DataFrame(columns = ['name','url','pagelikes','follower','visits','description','links'])

# Run this for every profile you want to scrape (after moving to the target page)
pr = ScrapedProfile()
dfProfiles.loc[len(dfProfiles)] = data
print(dfProfiles)

###############################################################################
# This codeblock scrolls until it reaches the Month 'Juni'
def scroller():
    scrheight = driver.execute_script('return document.body.scrollHeight')
    while True:
        driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
        time.sleep(1)
        newheight = driver.execute_script('return document.body.scrollHeight')
        soup = BeautifulSoup(driver.page_source,'lxml')
        lastpost = postings = soup.find_all('div',class_='x1ja2u2z xh8yej3 x1n2onr6 x1yztbdb')[-1]
        lastdate = lastpost.find('span',class_='x4k7w5x x1h91t0o x1h9r5lt x1jfb8zj xv2umb2 x1beo9mf xaigb6o x12ejxvf x3igimt xarpa2k xedcshv x1lytzrv x1t2pt76 x7ja8zs x1qrby5j').text
        if lastdate.split(' ')[-1] == 'Juni':
                break
scroller()
    
# Scrape the postings
postData = []
emoData = []
allimagelinks = []
soup = BeautifulSoup(driver.page_source,'lxml')
postings = soup.find_all('div',class_='x1ja2u2z x1n2onr6')
print('Postings: ' + str(len(postings)))
for p in postings:
    date = p.find('a',class_='x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1heor9g xt0b8zv xo1l8bm').text         
    try:
        content = p.find('span',class_='x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xo1l8bm xzsf02u x1yc453h').text
    except AttributeError:
        content = ''
    imagelinks = []
    imagecontents = []
    # smaller html code    
    sp = p.find('div',class_='x1n2onr6')
    try:
        imagelinks.append(sp.find('img',class_='x1ey2m1c xds687c x5yr21d x10l6tqk x17qophe x13vifvy xh8yej3 xl1xv1r')['src'])
    except:
        pass   
    try:
        images = sp.find_all('img','x1gqwnh9 x1snlj24')
        for i in images:
            imagelinks.append(i['src'])
    except:
        pass
    allimagelinks = allimagelinks + imagelinks        
    try:
        everylink = [l['href'] for l in sp.find_all('a',href = True)]
        links = [l for l in everylink if not 'www.facebook' in l]
    except AttributeError:
        links = ''
    try:
        video = str(sp.find('video',class_='xh8yej3 x5yr21d x1lliihq')['src']).split('blob:')[1]
    except:
        video = ''
    try:
        n_likes = sp.find('span',class_='x16hj40l').text
    except AttributeError:
        n_likes = '' 
    try:
        interact = p.find_all('span',class_='x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xo1l8bm xi81zsa')
        try:
            comments = interact[0].text
        except:
            comments = ''
        try:
            shares = interact[1].text
        except:
            shares = ''
        # just in case there is a structural error
        if "geteilt" in comments and shares == '':
            shares = comments.split(' ')[0]
            comments = ''
        comments = comments.split(' ')[0]
        shares = shares.split(' ')[0]
    except AttributeError:
        comments = ''
        shares = ''   
    # pdata contains the basic data of every post
    postData.append([date,content,n_likes,comments,shares,imagelinks,links])
        
    # I also want to collect the emotional reactions on the postings
    emohtml = p.find_all('div',class_='x1i10hfl x1qjc9v5 xjbqb8w xjqpnuy xa49m3k xqeqjp1 x2hbi6w x13fuv20 xu3j5b3 x1q0q8m5 x26u7qi x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xdl72j9 x2lah0s xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x2lwn1j xeuugli xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 x16tdsg8 x1hl2dhg xggy1nq x1ja2u2z x1t137rt x1o1ewxj x3x9cwd x1e5q0jg x13rtm0m x3nfvp2 x1q0g3np x87ps6o x1lku1pv x1a2a7pz')
    emoList = ['Gefällt','Love','Umarmung','Haha','Traurig','Wütend']
    emotions = ['','','','','','']
    for e in emohtml[:-3]:
        for l in emoList:
            try:
                if l in str(e):
                    emotions[emoList.index(l)] = (e['aria-label'].split(': ')[1].split(' ')[0])
            except:
                pass
    emoData.append(emotions)       
    
##############################################################################
# save all pictures with screenshots
saving_path = 'C:/Users/andre/Documents/Python/Web_Scraper/Social-Media-Bots/Images/'
for i in allimagelinks:
    driver.get(i)
#    print(saving_path + examObject + '_' + str(allimagelinks.index(i)) + '.png')
    driver.find_element('xpath','/html/body/img').screenshot(saving_path + examObject + '_' + str(allimagelinks.index(i) + 1) + '.png')
    # If i just want to get the first 50 pictures
    if allimagelinks.index(i) == 50:
        break

##############################################################################
# Two Dataframes for two categories             
dfPostings = pd.DataFrame(postData, columns = ['date','content','likes','comments','shares','image links','links']) 
dfEmotions = pd.DataFrame(emoData, columns = ['likes','heart','hug','laughter','sad','angry'])

# Finally we save the Data in an excel file seperated in three sheets
path = '[path to the place where you want to save this file]\FacebookResults.xlsx'
with pd.ExcelWriter(path, engine='openpyxl') as writer:
    dfProfiles.to_excel(writer,sheet_name='Profile Stats')
    dfPostings.to_excel(writer,sheet_name='Postings Data')
    dfEmotions.to_excel(writer,sheet_name='Postings Emotions') 
