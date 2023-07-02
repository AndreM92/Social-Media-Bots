from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC
from selenium.common.exceptions import *

import pyautogui

from datetime import datetime

import requests
from bs4 import BeautifulSoup
import lxml
import time
import numpy as np
import pandas as pd

import os

# Files in the current path
my_path = os.getcwd()
if my_path.split('\\')[-1] != 'InstaCrawler_file':
    os.chdir(my_path + '\\InstaCrawler_file')
    my_path = os.getcwd()
print(my_path)

username, password = ['','']
files = [f for f in os.listdir(my_path)]
if 'chromedriver.exe' not in files:
    print('Install chromedriver and place it in the folder')
if 'logindata.txt' in files:
    with open ('logindata.txt', 'r', encoding='utf-8') as file:
        content = file.read().split('\n')
    for c in content:
        if 'username' in c and len(c) > 10:
            username = c.split()[1].strip()
        if 'password' in c and len(c) > 10:
            password = c.split(':')[1].strip()
if len(username) < 1:
    username = str(input('Username(Email oder Name):'))
if len(password) < 1:
    password = str(input('Password:'))

if 'sources.xlsx' in files:
    df_us = pd.read_excel(my_path + '/sources.xlsx')
    links = list(df_us['link'])
    companies = list(df_us['companies'])
else:
    links = []
    links.append(str(input("Paste the link to an Instagram profile you want to scrape:")))
    links.append(str(input("Add another link for testing purposes")))
print(f'Username: {username}')
print('Companies to investigate:')
for e in companies:
    print(e)

# Setting the dates and time limit
timepoint = input('Capture social media posts until the date (format: YYYY-MM-TT):')
while len(timepoint) != 10 or timepoint[0].isdigit()== False or timepoint[4] != '-':
    print('Wrong date format')
    timepoint = input('Capture social media posts until the date (format: YYYY-MM-TT):')
datelimit = datetime.strptime(timepoint, "%Y-%m-%d")
curr_date = datetime.now()
#try:
#    timepoint
#except NameError:
#    timepoint = '2023-05-01'

# Open the browser
driver = webdriver.Chrome('chromedriver.exe')
loginpage = 'https://www.instagram.com/accounts/login/'
driver.get(loginpage)
driver.maximize_window()
time.sleep(3)

# Click through the first Cookie Banner
try:
    driver.find_element('xpath', "//*[text()='Optionale Cookies ablehnen']").click()
except:
    try:
        time.sleep(1)
        driver.find_element('xpath', "//*[text()='Optionale Cookies ablehnen']").click()
    except Exception as e:
        print(repr(e))
        try:
            soup = BeautifulSoup(driver.page_source, 'lxml')
            buttons = [b.text for b in soup.find_all('button') if 'cookies' in b.text.lower()]
            searchfor = "//*[text()='" + buttons[-1] + "']"
            driver.find_element('xpath', searchfor).click()
        except Exception as e:
            print(repr(e))
            pyautogui.moveTo(923, 838)
            time.sleep(1)
            pyautogui.click()

# login
def login(username,password):
    WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH,'//*[@id="loginForm"]/div/div[1]/div/label/input')))
    nameslot = driver.find_element('xpath','//*[@id="loginForm"]/div/div[1]/div/label/input')
    pwslot = driver.find_element('xpath','//*[@id="loginForm"]/div/div[2]/div/label/input')
    nameslot.clear()
    nameslot.send_keys(username)
    pwslot.clear()
    pwslot.send_keys(password)
    driver.find_element('xpath','//*[@id="loginForm"]/div/div[3]/button/div').click()

time.sleep(3)
try:
    login(username,password)
except:
    try:
        time.sleep(1)
        login(username,password)
    except Exception as e:
        print(repr(e))

# Don't save login information
time.sleep(10)
page = driver.current_url
if page != 'https://www.instagram.com/':
    try:
        driver.find_element('xpath',"//*[text()='Jetzt nicht']").click()
    except Exception as e:
        print(repr(e))
        time.sleep(3)
        pyautogui.moveTo(1092,638)
        pyautogui.click()
        time.sleep(1)
        if page != 'https://www.instagram.com/':
            pyautogui.click()

# Deactivate notifications
time.sleep(5)
soup = BeautifulSoup(driver.page_source, 'lxml')
banner = [s.text for s in soup.find_all('div') if 'Benachrichtigungen aktivieren' in s.text]
if banner:
    try:
        driver.find_element('xpath',"//*[text()='Jetzt nicht']").click()
    except:
        time.sleep(1)
        pyautogui.moveTo(942,775)
        pyautogui.click()

##############################################################################
# A function to open the targetpage and scrape the profile stats
def scrapeProfile(link):
    driver.get(link)
    dt = datetime.now()
    dt_str = dt.strftime("%Y-%m-%d %H:%M:%S")
    time.sleep(5)
    xheader = '//*[@id="mount_0_0_g+"]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section'
    try:
        headertext = driver.find_element('xpath',xheader).text
    except:
        xheader = '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section'
        try:
            headertext = driver.find_element('xpath', xheader).text
        except:
            pass
    info, pname, bges, follower, following = np.zeros(5)
    desclist = []
    if headertext:
        info = headertext.split('\n')
        pname = info[0]
        for i in info:
            if 'Beiträge' in i:
                bges = i.split()[0]
            elif 'Follower' in i:
                follower = i.split()[0]
            elif 'Gefolgt' in i:
                following = i.split()[0]
            else:
                if i not in desclist:
                    desclist.append(i)
            description = ' '.join(desclist)
    data = [pname,dt_str,bges,follower,following,description]
    return data


# I'm creating my first DataFrame with the profile stats
dfProfiles = pd.DataFrame(columns = ['Profil','Datum','Beiträge','Follower','Gefolgt','Beschreibung'])

##############################################################################
# The scrapePost function scrapes the details of every post
def scrapePost(p_name, count):
    # Click on the first or next post
    if count == 1:
        try:
            driver.find_element(By.CLASS_NAME,'_aagw').click()
        except Exception as e:
            print(repr(e))
            time.sleep(3)
            pyautogui.moveTo(800,880)
            pyautogui.click()
    else:
        link = driver.current_url
        try:
            #driver.find_element(By.CSS_SELECTOR, "[aria-label=^'Weiter']").click()
            driver.find_element('xpath', "//*[text()='Weiter']").click()
        except:
            pyautogui.moveTo(1865, 575)
            pyautogui.click()
            if link == driver.current_url:
                time.sleep(1)
                pyautogui.click()
    link = driver.current_url
    time.sleep(2)

    date, likes, comments, video, image = np.zeros(5)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    date = soup.find('time', class_='_aaqe')['datetime'].replace('T',' ').split('.')[0]
    #date = soup.find('time', class_='_aaqe')['datetime'].split('T')[0]
    #postdate = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")

    try:
        content = soup.find('div', class_='_a9zs').text
    except:
        try:
            content = driver.find_element(By.CLASS_NAME, '_a9zs').text
        except:
            pass
    links = content.count('https')
    try:
        likes = soup.find('span', class_='x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs xt0psk2 x1i0vuye xvs91rp x1s688f x5n08af x10wh9bi x1wdrske x8viiok x18hxmgj').text
    except AttributeError:
        try:
            likes = soup.find_all('div', class_='_aacl _aaco _aacw _aacx _aada _aade')[-1].span.text
        except:
            try:
                driver.find_element(By.CLASS_NAME, '_aauw').click()
                time.sleep(1)
                likes = driver.find_element(By.CLASS_NAME, '_aauu').text.split(' ')[0]
                if not str(likes).isdigit():
                    likes = driver.find_element(By.CLASS_NAME, '_aauu').text.split(' ')[1]
                driver.find_element(By.CLASS_NAME, '_aauw').click()
            except:
                pass

    if len(str(likes)) > 1:
        if likes[0].isdigit() == False:
            likes = likes.split(' ')[1]
    comments = len(soup.find_all('ul', class_='_a9ym'))

    #At least one Video
    if soup.find('video'):
        video = 1
    # this can also contain a row of images
    else:
        if soup.find('div', class_='_aagv').find('img', src=True):
            image = 1

    # Take a screenshot and save it
    saving_path = my_path + '/Images/'
    driver.save_screenshot(saving_path + p_name + '_' + str(count) + '.png')
    # If you only want the picture:
    # driver.find_element(By.CLASS_NAME,'_aagw').screenshot(saving_path + examObject + '_' + str(count) +'.png')

    return [p_name,count,date,content,likes,comments,links,video,image,link]


# Empty DataFrame for the post details
dfPosts = pd.DataFrame(columns = ['profile','number','date','content','likes','comments','links','video','image','link'])

##############################################################################
# Combination of the functions
# Iteration over the links
for l in links:
    profile_stats = scrapeProfile(l)
    profile_name = profile_stats[0]
    dfProfiles.loc[len(dfProfiles)] = profile_stats

    # Iteration over the posts
    count = 1
    while curr_date >= datelimit and count <= 5:
        dfPosts.loc[len(dfPosts)] = scrapePost(profile_name, count)
        count += 1


# Save the DataFrames in Excel:
with pd.ExcelWriter(my_path + '/InstagramData.xlsx') as writer:
    dfProfiles.to_excel(writer,sheet_name='Profiledata')
    dfPosts.to_excel(writer,sheet_name='Postings')


# Pyautogui Investigation process
#time.sleep(3)
#x,y = pyautogui.position()
#print(str(x)+ ','+ str(y))