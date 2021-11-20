from afinn import Afinn
afinn = Afinn(language='en')

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import json
import csv

import translators as ts

options = Options()
options.headless = True
options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome("/Users/stephanie/Downloads/chromedriver")

content = driver.page_source
soup = BeautifulSoup(content, features="html.parser")

collected_URLs = []
collected_HTML = []
collected_URLs_Train = []
collected_HTML_Train = []

titles = []
articles = []

counter = 0
counter2 = 0
df_train = pd.read_csv("few.csv")


def remove_dataComponents(htmlContent):
   mySoup = BeautifulSoup(htmlContent, "html.parser")
   for data in mySoup(['style', 'script']):
      data.decompose()
   return ' '.join(soup.stripped_strings)

#contentToTranslate:String with HTML data
def translateContent(x):
   translatedString = ""
   translatedSentences = []
   split_strings = []
   temp = ''
   for index in range(0, len(x)):
      if x[index] != '.' and x[index] != '!' and x[index] != '?':
         temp += x[index]
         # print(temp)
      else:
         split_strings.append(temp)
         temp = ''
   #print(split_strings)
   for y in split_strings:
      #print('orginal text: ',y)
      result = (ts.google(y))
      #print('translated text: ', result)
      translatedSentences.append(result)
      translatedString+=result
   return translatedString


for i in range(len(df_train)):
   collected_URLs.append(df_train.values[i][5]) 
#    expected_label.append(int(df_train.values[i][4]))



#loop through URLs to get data from websites
for x in collected_URLs:
    print("URL: ", x)
    driver.get(x)
   
    content = driver.page_source
    soup = BeautifulSoup(content, features="html.parser")

    titlefound = False
    #check if most of the website titles are in h1 and record how many
    if soup.find('h1'):
      if soup.find('h1').getText():
         temp = soup.find('h1').getText()
         if temp.isspace() == 0:
            if soup.find('h1').getText() != '':
               temp2 = soup.find('h1').getText()
               titles.append(temp2.strip()) 
               print('content of h1: '+ titles[counter])
               counter = counter + 1
               titlefound = True
         else:
            print('h2 is whitespace, URL: '+ x)
      else:
         print('no value found in h2, URL: '+ x)
    if soup.find('h2'):
      if soup.find('h2').getText():
         temp = soup.find('h2').getText()
         if temp.isspace() == 0:
            if soup.find('h2').getText() != '':
               temp2 = soup.find('h2').getText()
               titles.append(temp2.strip()) 
               print('content of h2: '+ titles[counter])
               counter = counter + 1
               titlefound = True
         else:
            print('h2 is whitespace, URL: '+ x)
      else:
         print('no value found in h2, URL: '+ x)
    if soup.find('h3'):
      if soup.find('h3').getText():
         temp = soup.find('h3').getText()
         if temp.isspace() == 0:
            if soup.find('h3').getText() != '':
               temp2 = soup.find('h3').getText()
               titles.append(temp2.strip()) 
               print('content of h3: '+ titles[counter])
               counter = counter + 1
               titlefound = True
         else:
            print('h3 is whitespace, URL: '+ x)
      else:
         print('no value found in h3, URL: '+ x)

    if titlefound == False:
        # append content if title not found in h1, h2, or h3
        dataToBeTranslated = remove_dataComponents(content)
        Englishstr = translateContent(dataToBeTranslated)
        print(Englishstr)
        titles.append(Englishstr)
        sa_score = afinn.score(Englishstr)
        print("sa_score: ", sa_score)

        with open('sa_score.csv', 'a+', encoding='UTF8') as file:
            writer = csv.writer(file)
            writer.writerow([sa_score])
            file.close()
    else:
        counter3 = 0
        for x in titles:
            result = (ts.google(x))
            titles[counter3] = result
            counter3 = counter3 + 1
        s = ''.join(titles)
        sa_score = afinn.score(s)
        print("sa_score: ", sa_score)
        
        with open('sa_score.csv', 'a+', encoding='UTF8') as file:
             writer = csv.writer(file)
             writer.writerow([sa_score])
             file.close()


    collected_HTML.append(content)
   # print(collected_HTML[counter2])


driver.close()
