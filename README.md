# Social-Media-Bots
This project includes Social Media Bots with a focus on Data Scraping and Data Analytics.</br>

## InstaCrawler_file: A crawler for Instagram as an executable file 
(Written for German social media pages, but easily transferable to other languages)

Instructions:
1. Install all necessary Python modules
2. Install or update Google Chrome Driver
3. Download Chromedriver and save it in the same path while paying attention to the browser version (but select win32 despite 64)
https://chromedriver.chromium.org/downloads
4. Save "login data" as a text file with the content:
username: username
password: password
in the folder
Otherwise, the program will prompt for manual input
5. Update company names and pages in the Excel file
6. Create a Python link and modify it:</br>
   Example for "target" (location of Python.exe and location of the script):</br>
   C:\Users\andre\Documents\Python\Python310_Interpreter\python.exe C:\Users\andre\OneDrive\Desktop\IT-Projekte\GitHub\Social-Media-Bots-main\InstaCrawler_file
-Media-Bots\InstaCrawler_file\InstaCrawler.py</br>
   Example of "run in":</br>
   C:\Users\andre\OneDrive\Desktop\IT-Projekte\GitHub\Social-Media-Bots-main\InstaCrawler_file
-Media-Bots\InstaCrawler_file
7. Click on the Python link and run the program</br>
   For security reasons, I have limited the scraper to five posts per profile ;)

I've written the following code to observe german corporate Social Media profiles. It may not work in different countries and for other types of accounts. This is the reason, why I didn't put the whole code in one class or function and split it in short sections instead.</br>

## FacebookBot

- automated login
- several ways to get around cookie banners
- searching for and getting on a profile
- collection of the profile stats
- scrolling down the feed until you reach a specific date
  - The DateTime isn't displayed as text anymore, so I had to solve this problem with screenshots and image reading (Pillow/ Pytesseract)
- scraping of the date, content, images, links, likes, number of comments and number of shares of every posting 
  - I've written a new function that handles the changed DateTime accessibility of the posts 
- scraping of every specific emotional reaction (old code)
- saving the data in DataFrames 
- and finally an export of the DataFrames to an excel file 

## InstagramBot

- automated login
- several ways to get around cookie banners
- searching for and getting on a profile
- collection of the profile stats
- scrolling down the feed until you reach a specific date (with the datetime module)
- scraping of the date, content, images, links, pictures, likes and number of comments of every posting (this includes screenshots)
- saving the data in DataFrames 
- exporting the DataFrames to an excel file 

- Bonus:
  - Follow
  - Like
  - Comment

## TwitterBot

- automated login
- several ways to get around different cookie banners
- searching for and getting on a profile
- collection of the profile stats
- A post scraper with an integrated scrolling function by pixel numbers that stops on a specific date
- saving the data in DataFrames
- exporting the DataFrames to an excel file 

## YouTubeScraper

This is just a little program to scrape:
- The statistics of a YouTube account
- The details of every video in a specific timeframe</br>

as well as:
- crawling through YouTube
- getting around cookie banners
