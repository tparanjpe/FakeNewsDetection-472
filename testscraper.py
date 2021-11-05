#Importing packages
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd

driver = webdriver.Chrome("/Users/stephanie/Downloads/chromedriver")
driver.get("https://leadstories.com/hoax-alert/2021/09/fact-check-harris-did-not-admit-vaccine-does-not-work.html")

#driver.save_screenshot('screenshot.png')
titles = []

content = driver.page_source
soup = BeautifulSoup(content, features="html.parser")

for element in soup.findAll('header', attrs={'class': 'mod-full-article-header'}):
   title = element.find('h1', attrs={'itemprop': 'name'})
   titles.append(title.text)
df = pd.DataFrame({'Post title': titles})
df.to_csv('posts.csv', index=False, encoding='utf-8')

print(driver.page_source) 
driver.close()

