# Social-Media-Bots
This project includes Social Media Bots with a focus on Data Scraping and Data Analytics.</br>

I've written this code to observe german corporate Social Media profiles. It may not work in different countries and for other types of accounts. This is the reason, why I didn't put the whole code in one class or function and split it in short sections instead.</br>

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
- The details of every video in a specific timeframe
as well as:
- crawling through YouTube
- getting around cookie banners
