#Importing packages
from bs4.element import Declaration
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import json
from html.parser import HTMLParser
from sklearn.feature_extraction.text import CountVectorizer
from textblob import TextBlob


class ParseHTML(HTMLParser):
   dataReturned = ""
   def handle_data(self, data):
      #self.dataReturned.append(data)
      self.dataReturned+=data
      #print("Encountered some data  :", data)

truthList = ["true", "truth"]
falseList = ["false", "fake"]
options = Options()
options.headless = True
options.add_argument("--window-size=1920,1080")

chromeOptions = webdriver.ChromeOptions()
chromeOptions.binary_location = "C:\Program Files\Google\Chrome\Application\chrome.exe" 
driver = webdriver.Chrome("C:\\Users\\tarap\\Dropbox\\My PC (LAPTOP-EFB1H1KE)\\Desktop\\CSE472\\project2\\chromedriver.exe",  options=chromeOptions)

content = driver.page_source
soup = BeautifulSoup(content, features="html.parser")

collected_URLs = []
collected_HTML = []
titles = []
articles = []
myParser = ParseHTML()
termFrequency = CountVectorizer()
counter = 0
counter2 = 0
model_df_columns = ["claim", "tf"]
model_df = pd.DataFrame(columns=model_df_columns)

#parse data.data to get the URLs
df = pd.read_csv("datasets/data.csv")
#print(df) 

# this is how to get specific item from csv data
# i iterates through the row(number of data entries) and the second array access is the column
for i in range(len(df)):
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
   
   # print(content)
   collected_HTML.append(content)
   # languageDetected = TextBlob(content)
   Englishstr = content

   #gets the data from the html file and adds it to a class array
   myParser.feed(Englishstr)
   myTerms = [myParser.dataReturned]
   # with open("Output.txt", "w") as text_file:
   #    text_file.write(myParser.dataReturned)
   #gets the term frequency values for each word in the data
   termFrequencyResults=termFrequency.fit_transform(myTerms)
   myTerms = pd.DataFrame(termFrequencyResults.toarray(), columns=termFrequency.get_feature_names())
   truthCount = 0
   for term in truthList:
      try:
      #index = [i for i, x in enumerate(termFrequency.vocabulary_) if x == term]
         myVal = myTerms[term]
         truthCount += myVal.get(key=0)
         #print(myVal.get(key=0))
      except:
         print(term + " not found")

   falseCount = 0
   for term in falseList:
      try:
      #index = [i for i, x in enumerate(termFrequency.vocabulary_) if x == term]
         myVal = myTerms[term]
         falseCount += myVal.get(key=0)
         #print(myVal.get(key=0))
      except:
         print(term + " not found")

   print("false list", falseCount)
   print("truth list",  truthCount)

   leaningResult = truthCount + (falseCount * -1)
   if(leaningResult < 0):
      print("false leaning")
   elif(leaningResult > 0):
      print("true leaning")
   elif (leaningResult == 0):
      print("undetermined")
   # print(collected_HTML[counter2])

#store collected HTML into html.json file
# with open('html.json', 'w', encoding='utf-8') as f:
#     json.dump(collected_HTML, f, ensure_ascii=False, indent=4)
# #close driver
# driver.close()


