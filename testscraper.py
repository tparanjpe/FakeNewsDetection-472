#Importing packages
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import json

options = Options()
options.headless = True
options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome("/Users/stephanie/Downloads/chromedriver")
# driver.get("https://leadstories.com/hoax-alert/2021/09/fact-check-harris-did-not-admit-vaccine-does-not-work.html")

content = driver.page_source
soup = BeautifulSoup(content, features="html.parser")

collected_URLs = []
collected_HTML = []
titles = []
articles = []

counter = 0
counter2 = 0

#parse data.data to get the URLs
df = pd.read_csv("datasets/data.csv")
print(df) 

# this is how to get specific item from csv data
# i iterates through the row(number of data entries) and the second array access is the column
for i in range(len(df)):
   #  col1 = df.values[i][0]
   #  col2 = df.values[i][1]
   #  col3 = df.values[i][2]
   #  col4 = df.values[i][3]
   #  col5 = df.values[i][4]
   #  col6 = df.values[i][5]
    collected_URLs.append(df.values[i][5]) 


#loop through URLs to get data from websites
for x in collected_URLs:
   driver.get(x)
   
   content = driver.page_source
   soup = BeautifulSoup(content, features="html.parser")

   #check if most of the website titles are in h1 and record how many
   if soup.find('h1'):
      # print('found h1')
      if(soup.find('h1').getText()):
         titles.append(soup.find('h1').getText()) 
         print('content of h1: '+ titles[counter])
         counter = counter + 1
      else:
         print('no value found in h1, URL: '+ x)
   
   collected_HTML.append(content)
   # print(collected_HTML[counter2])

#store collected HTML into html.json file
with open('html.json', 'w', encoding='utf-8') as f:
    json.dump(collected_HTML, f, ensure_ascii=False, indent=4)
#close driver
driver.close()

# # for element in soup.findAll('header', attrs={'class': 'mod-full-article-header'}):
# #    title = element.find('h1', attrs={'itemprop': 'name'})
# #    titles.append(title.text)
# # df = pd.DataFrame({'Post title': titles})
# # df.to_csv('posts.csv', index=False, encoding='utf-8')


# #find the tags of article contents and implement switch cases


# # if soup.find('header'):
# #    print('found header')
# #    print('content of header: '+soup.find('header').getText())



