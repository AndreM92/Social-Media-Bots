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


# Setting options

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))
driver.maximize_window()
driver.get('[path to your driver]\chromedriver.exe')
time.sleep(2)

# Pyautogui Investigation process
time.sleep(3)
x,y = pyautogui.position()
print(str(x)+ ','+ str(y))
# 930,777

# Click through the Cookie Banner
try:
    driver.find_element('xpath','//*[@id="mount_0_0_dK"]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/button[1]').click()
except NoSuchElementException:
    time.sleep(1)
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
    except:
        print('There is something wrong with the page')

# Second Cookie Banner
try:
    WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH,'//*[@id="mount_0_0_St"]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div')))
    driver.find_element('xpath','//*[@id="mount_0_0_DI"]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[1]/div/div[3]/div[3]/div/div[1]/div/div[2]/div[1]/span').click()
except:
    time.sleep(1)                           
    pyautogui.moveTo(965,759)
    pyautogui.click()

# Save login informations? No!
try:
    WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH,'//*[@id="mount_0_0_St"]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div/div/div/button')))
    driver.find_element('xpath','//*[@id="mount_0_0_St"]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div/div/div/button').click()
    print('first')
except:
   time.sleep(1)
   pyautogui.moveTo(1092,638)
   pyautogui.click()

# (de)activate notifications
time.sleep(3)
try:
    WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH,'//*[@id="mount_0_0_yg"]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/button[2]')))
    driver.find_element('xpath','//*[@id="mount_0_0_yg"]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/button[2]').click()
except:
    time.sleep(1)
    pyautogui.moveTo(942,775)
    pyautogui.click()

###############################################################################    
# Searching Process
# Activate searchbutton
target = 'libertarian_monk'
try:
    WebDriverWait(driver,1).until(EC.presence_of_element_located((By.XPATH,'/html/body')))
    driver.find_element('xpath','/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[1]/div/div/div/div/div[2]/div[2]/div/a/div/div[1]/div/div/svg').click()
except NoSuchElementException:
    time.sleep(3)
    pyautogui.moveTo(21,379)
    pyautogui.click()
time.sleep(1)    

# Search for a profile
searchbutton = driver.find_element('xpath','/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[1]/div/div/div[2]/div/div/div[2]/div[1]/div/input')
searchbutton.send_keys(target)
time.sleep(1)
try:
    driver.find_element('xpath','//*[@id="mount_0_0_+3"]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[1]/div/div/div[2]/div/div/div[2]/div[2]/div/div[1]/div/a/div/div[1]/div/span/img').click()
except NoSuchElementException:
    time.sleep(1)
    pyautogui.moveTo(149,384)
    pyautogui.click()
time.sleep(2)

##############################################################################
# Scraping the page
class Scraper:
    def scrape(self):
        url = driver.current_url
        soup = BeautifulSoup(driver.page_source,'lxml')
        postings,follower,following = [e.text for e in soup.find_all('span',class_='_ac2a')]
        descrhtml = soup.find('div',class_='_aa_c')
        descraw = descrhtml.text

profilestats = Scraper().scrape()