#Importing packages
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd

#parse few.data to get the URLs

driver = webdriver.Chrome("/Users/stephanie/Downloads/chromedriver")
driver.get("https://leadstories.com/hoax-alert/2021/09/fact-check-harris-did-not-admit-vaccine-does-not-work.html")

#driver.save_screenshot('screenshot.png')
titles = []
articles = []

content = driver.page_source
soup = BeautifulSoup(content, features="html.parser")

# for element in soup.findAll('header', attrs={'class': 'mod-full-article-header'}):
#    title = element.find('h1', attrs={'itemprop': 'name'})
#    titles.append(title.text)
# df = pd.DataFrame({'Post title': titles})
# df.to_csv('posts.csv', index=False, encoding='utf-8')

#check if most of the website titles are in h1 and record how many
if soup.find('h1'):
   print('found h1')
   titles[i] = soup.find('h1').getText()
   print('content of h1: '+ titles[i])
#find the other possible tag that titles could be stored in

#find the tags of article contents and implement switch cases


# if soup.find('header'):
#    print('found header')
#    print('content of header: '+soup.find('header').getText())

# print(driver.page_source) 
driver.close()

