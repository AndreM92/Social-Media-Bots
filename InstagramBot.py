from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC
from selenium.common.exceptions import *

import pyautogui

from datetime import datetime

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
    driver.get('https://www.instagram.com/accounts/login/')
    time.sleep(1)
    if loginpage != driver.current_url:
        print('There is something wrong with the page')

# Pyautogui Investigation process
# time.sleep(3)
# x,y = pyautogui.position()
# print(str(x)+ ','+ str(y))

##############################################################################
# Login process

# Get to the login page
driver = webdriver.Chrome('[path to your driver]\chromedriver.exe')
loginpage = 'https://www.instagram.com/accounts/login/'
driver.get(loginpage)
driver.maximize_window()
time.sleep(1)
if loginpage != driver.current_url:
    fixDriverbug()

# Click through the first Cookie Banner (shown with four different methods)
try:
    driver.find_element('xpath','//*[@id="mount_0_0_dK"]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/button[1]').click()
except NoSuchElementException:
    try:
        driver.find_element('xpath',"//*[text()='Nur erforderliche Cookies erlauben']").click()
        time.sleep(1)
    except:
        try:
            driver.find_element(By.CLASS_NAME,'_a9--').click()
        except Exception as e:
            print(repr(e))
            pyautogui.moveTo(930,777)
            pyautogui.click()

# Push your Name and Password to the Website and login
username = '[your username]'
password = '[your password]'

def login(username,password):
    WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH,'//*[@id="loginForm"]/div/div[1]/div/label/input')))
    nameslot = driver.find_element('xpath','//*[@id="loginForm"]/div/div[1]/div/label/input')
    pwslot = driver.find_element('xpath','//*[@id="loginForm"]/div/div[2]/div/label/input')
    nameslot.clear()                        
    nameslot.send_keys(username)
    pwslot.clear()
    pwslot.send_keys(password)
    driver.find_element('xpath','//*[@id="loginForm"]/div/div[3]/button/div').click()

try:
    login(username,password)
except:
    try:
        time.sleep(1)
        login(username,password)
    except Exception as e: 
        print('There is something wrong with the page')
        print(repr(e))
        # closing the browser window
        driver.close()
        # closing the program
        exit()

# Second Cookie Banner
try:
    WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH,'//*[@id="mount_0_0_St"]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div')))
    driver.find_element('xpath','//*[@id="mount_0_0_DI"]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[1]/div/div[3]/div[3]/div/div[1]/div/div[2]/div[1]/span').click()
except:
    try:
        # This line seems to work best in the German internet
        # In English it might work with 'not now' (or whatever is writen on the decline button)
        driver.find_element('xpath',"//*[text()='Jetzt nicht']").click()
    except Exception as e:
        print(repr(e))
        time.sleep(1)                           
        pyautogui.moveTo(965,759)
        pyautogui.click()

# Save login informations? No!
try:
    WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH,'//*[@id="mount_0_0_St"]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div/div/div/button')))
    driver.find_element('xpath','//*[@id="mount_0_0_St"]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div/div/div/button').click()
except:
    try:
        driver.find_element('xpath',"//*[text()='Jetzt nicht']").click()
    except Exception as e:
        print(repr(e))
        time.sleep(1)  
        pyautogui.moveTo(1092,638)
        pyautogui.click()        

# (de)activate notifications
try: 
    WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH,'//*[@id="mount_0_0_yg"]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/button[2]')))
    driver.find_element('xpath','//*[@id="mount_0_0_yg"]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/button[2]').click()
except:
    try:
        driver.find_element('xpath',"//*[text()='Jetzt nicht']").click()
    except:
        time.sleep(1)
        pyautogui.moveTo(942,775)
        pyautogui.click() 
        
startpage = driver.current_url
        
###############################################################################    
# Searching Process on Instagram
# Activate searchbutton
examObject = 'libertarian_monk'

def getsearchbox():
    try:
        WebDriverWait(driver,1).until(EC.presence_of_element_located((By.XPATH,'/html/body')))
        driver.find_element('xpath','/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[1]/div/div/div/div/div[2]/div[2]/div/a/div/div[1]/div/div/svg').click()
    except NoSuchElementException:
        try:
            driver.find_element(By.CSS_SELECTOR,"[aria-label='Suche']").click()
        except NoSuchElementException:
            try:
                time.sleep(1)
                pyautogui.moveTo(21,379)
                pyautogui.click()
                time.sleep(1)
            except Exception as e:
                print(repr(e))       
    try:
        searchbutton = driver.find_element('xpath','/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[1]/div/div/div[2]/div/div/div[2]/div[1]/div/input')
    except:
        try:
            searchbox = driver.find_element(By.CSS_SELECTOR,"[aria-label='Sucheingabe']")
            return searchbox
        except Exception as e:
            print(repr(e))

def getprofile(target):
    searchbox = getsearchbox()
    searchbox.send_keys(target)
    time.sleep(1)
#        searchbox.send_keys(Keys.RETURN)
    searchbox.send_keys(Keys.ENTER)
    try:
        searchbox.send_keys(Keys.RETURN)
    except:
        pass
    time.sleep(1)
    if target not in driver.current_url:        
        pyautogui.moveTo(149,384)
        pyautogui.click()  
                    
getprofile(examObject)  

##############################################################################
# Scrape the profile stats
class ScrapedProfile:
    def __init__(self):
        WebDriverWait(driver,1).until(EC.presence_of_element_located((By.CLASS_NAME,'_aarf')))
        # to prevent errors:
        self.name,self.url,self.follower,self.following,self.postings,self.desc,self.link = ['' for i in range(0,7)]
        self.url = driver.current_url
        soup = BeautifulSoup(driver.page_source,'lxml')
        try:
            elements = soup.find_all('span',class_='_ac2a')
            self.postings = elements[0].text
            self.follower = elements[1].text
            self.following = elements[1].text
        except:
            time.sleep(1)
            try:
               elements = soup.find_all('span',class_='_ac2a')
               self.postings = elements[0].text
               self.follower = elements[1].text
               self.following = elements[1].text
            except Exception as e:
                print(repr(e))
                pass
                
        descrhtml = soup.find('div',class_='_aa_c')
        if len(descrhtml) > 0:
            dl = [e for e in descrhtml]
            self.name = dl[0].text
            if len(descrhtml) > 1:
                self.desc = ('\n').join([e.text for e in descrhtml][1:]).strip()
                self.link = descrhtml.find('a')['href']
       
pr = ScrapedProfile()
# I'm creating my first DataFrame with the profile stats
data = [profile.name,profile.url,profile.follower,profile.following,profile.postings,profile.desc,profile.link]
dfProfiles = pd.DataFrame(columns = ['name','url','follower','following','postings','desc','link'])

# Run this for every profile you want to scrape (after moving to the target page)
profile = ScrapedProfile()
dfProfiles.loc[len(dfProfiles)] = [profile.name,profile.url,profile.follower,profile.following,profile.postings,profile.desc,profile.link]
print(dfProfiles)

##############################################################################
# Crawler for the posts
# The class ScrapedPosts saves the details of every post
# scrollCrawler: Just scrolls down und scrapes the links

##############################################################################
# The clickCrawler is clicking through every post until it reaches a specific date
# and scrapes all the relevant details
# You have to run getprofile(examObject) first to get on the right page

timepoint = '2021-11-01'

class ScrapedPosts():
    def __init__(self,timepoint):
        self.postData = []
        # click on the first post
        try:
            driver.find_element('xpath','//*[@id="mount_0_0_aT"]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div[3]/article/div[1]/div/div[1]/div[1]/a/div[1]/div[2]').click()
        except:
            try:
                driver.find_element(By.CLASS_NAME,'_aagw').click()
            except:
                pass
        time.sleep(2)
        datelimit = datetime.strptime(timepoint,"%Y-%m-%d")
        soup = BeautifulSoup(driver.page_source,'lxml')
        date = soup.find('time',class_='_aaqe')['datetime'].split('T')[0]
        postdate = datetime.strptime(date,"%Y-%m-%d")
            
        count = 1
        while postdate >= datelimit:
            self.scrapePost(soup,postdate,count)
            
            # click to the next post
            if count == 1:
                try:                            
                    driver.find_element('xpath','//*[@id="mount_0_0_vs"]/div/div/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[1]/div/div/div/button').click()
                except:
                    driver.find_element(By.CSS_SELECTOR,"[aria-label='Weiter']").click()
            else:
                try:
                    driver.find_element('xpath','//*[@id="mount_0_0_Ay"]/div/div/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[1]/div/div/div[2]/button').click()
                except:
                    try:
                        driver.find_element(By.CSS_SELECTOR,"[aria-label='Weiter']").click()
                    except ElementClickInterceptedException:
                        pyautogui.moveTo(1865,575)
                        pyautogui.click()
                        pyautogui.click()
            time.sleep(2)
            soup = BeautifulSoup(driver.page_source,'lxml')
            if not soup.find('time',class_='_aaqe'):
                time.sleep(2)
                soup = BeautifulSoup(driver.page_source,'lxml')
            if soup.find('time',class_='_aaqe'):
                date = soup.find('time',class_='_aaqe')['datetime'].split('T')[0]
                postdate = datetime.strptime(date,"%Y-%m-%d")
            else:
                break
            count += 1
            
    def scrapePost(self,soup,date,count):
        likes,comments,video,image = [0 for i in range(0,4)]
        date = str(date).split(' ')[0]
        link = driver.current_url
        try:
            content = soup.find('div',class_='_a9zs').span
        except:
            try:
                content = driver.find_element(By.CLASS_NAME,'_a9zs').text
            except:
                content = ''
        if len(content) >= 2 and len(content) <= 10:
            content = ' '.join([c.text.strip() for c in content])
        else:
            content = content.text.strip()
        try:
            likes = soup.find('div',class_='_aacl _aaco _aacw _aacx _aada _aade').find('span').text
        except AttributeError:
            try:
                likes = soup.find_all('div',class_='_aacl _aaco _aacw _aacx _aada _aade')[-1].span.text
            except:
                try:
                    driver.find_element(By.CLASS_NAME,'_aauw').click()
                    time.sleep(1)
                    likes = driver.find_element(By.CLASS_NAME,'_aauu').text.split(' ')[0]
                    if not str(likes).isdigit():
                        likes = driver.find_element(By.CLASS_NAME,'_aauu').text.split(' ')[1]
                    driver.find_element(By.CLASS_NAME,'_aauw').click()
                        
                except:
                    pass
        comments = len(soup.find_all('ul',class_='_a9ym'))
        links = content.count('https')
        if soup.find('video'):
            video = 1
            if soup.find('article',class_='_aatb').find('div',class_='_9zm2'):
                video = '2+'
        # this can also contain a row of images
        else: 
            if soup.find('div',class_='_aagv').find('img',src=True):
                image = 1
                if soup.find('article',class_='_aatb').find('div',class_='_9zm2'):
                    image = '2+'
                # Take a screenshot and save it
                saving_path = 'C:/Users/andre/Documents/Python/Web_Scraper/Social-Media-Bots/Images/'
                driver.save_screenshot(saving_path + examObject + '_' + str(count) + '.png')
                # If you only want the picture:
                # driver.find_element(By.CLASS_NAME,'_aagw').screenshot(saving_path + examObject + '_' + str(count) +'.png')
        self.postData.append([date,content,likes,comments,video,image,link])
        

# This runs the Crawler and show the details of every scraped post in a DataFrame
datalist = ScrapedPosts(timepoint).postData
dfPostings = pd.DataFrame(datalist,columns=['date','content','likes','comments','video','image','link'])

# I'm saving the overview and post details in different excel sheets
path = r"C:\Users\andre\OneDrive\Desktop\InstagramBotResults.xlsx"
with pd.ExcelWriter(path, engine='openpyxl') as writer:
    dfProfiles.to_excel(writer,sheet_name='overview')
    dfPostings.to_excel(writer,sheet_name=examObject)
    

# Bonus: 
# Follow
driver.find_element('xpath','//*[@id="mount_0_0_aw"]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/header/section/div[1]/div[1]/div/div/button/div/div').click()
# Like
driver.find_element(By.CSS_SELECTOR,"[aria-label='Gefällt mir']").click()
# Commnent
slot = driver.find_element(By.CSS_SELECTOR,"[aria-label^='Kommentieren']")
slot.click()
slot.send_keys("That's amazing!")
time.sleep(1)
slot.send_keys(Keys.ENTER)

##############################################################################
# The scrollCrawler function scrolls down until it reaches a specific date 
# and saves alle the links of the posts in this timeframe
# I limited the function to 20 scrolls to prevent unforeseen errors
# You have to run getprofile(examObject) first to get on the right page
month = 'October'
year = 2021          

def scrollCrawler(month,year):
    count =  0
    links = []
    mDictEng = {'january':1,'february':2,'march':3,'april':4,'may':5,'june':6,'july':7,\
                'august':8,'september':9,'october':10,'november':11,'december':12}
    mDictGer = {'januar':1,'februar':2,'märz':3,'april':4,'mai':5,'juni':6,'juli':7,\
                'august':8,'september':9,'oktober':10,'november':11,'dezember':12}
    if month in mDictEng:
        mInt = mDictEng[month]
    if month in mDictGer:
        mInt = mDictEng[month]
        
    scrheight = driver.execute_script('return document.body.scrollHeight')
    while True:
        driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
        time.sleep(3)
        newheight = driver.execute_script('return document.body.scrollHeight')
        pyautogui.moveTo(1625,910)
        pyautogui.click()
        time.sleep(3)
        # The xpath of the postings changes after scrolling down, so we need to catch the links before they aren't visible anymore
        soup = BeautifulSoup(driver.page_source,'lxml')
        linkpart = [l['href'] for l in soup.find_all('a',href=True) if l['href'][:3] == '/p/']
        plinks = ['https://www.instagram.com/' + l for l in linkpart if not 'liked_by' in l]
        links = links + plinks
        try:
            rawdate = str(soup.find('time',class_='_aaqe'))
            cmonth = soup.find('time',class_='_aaqe').text.split(' ')[0].lower()
        except:
            pass
        try:
            driver.find_element(By.CSS_SELECTOR,"[aria-label='Schließen']").click()
        except NoSuchElementException:
            driver.find_element(By.CSS_SELECTOR,"[aria-label='Close']").click()
        time.sleep(1)
        
        try:
            print(cmonth)
            if cmonth in mDictEng:
                dInt = mDictEng[cmonth]
            if cmonth in mDictEng:
                dInt = mDictEng[cmonth]  
            if str(year) in rawdate and mInt <= dInt:
                # Return the links and remove duplicates of the collected links without losing the order
                return list(dict.fromkeys(links))
                break
        except:
            pass
        
        count += 1
        if count == 20:
            return list(dict.fromkeys(links))
            break
       
plinks = (crawler(month,year))
