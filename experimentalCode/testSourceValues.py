'''
Authors: Stephanie Lee and Tara Paranjpe
Project: CSE472 - Fake News Detection
Fall 2021
File Description: This file runs the model with source obtained from dataset and uses Naive Bayes classification model
'''

#import packages
from operator import truth
from bs4.element import Declaration
from scipy.stats.stats import RelfreqResult
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import json
import csv
from html.parser import HTMLParser
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.neighbors import KNeighborsClassifier
import translators as ts
from sklearn.naive_bayes import MultinomialNB

'''
This method removes style and script tags from the html body to get the text
ready for translation and analysis. 
'''
def remove_dataComponents(htmlContent):
   mySoup = BeautifulSoup(htmlContent, "html.parser")
   for data in mySoup(['style', 'script']):
      data.decompose()
   return ' '.join(soup.stripped_strings)

'''
This method takes the parsed html (with removed style and script tags) and translates
the data from the autodetected language to English.
'''
def translateContent(x):
   translatedString = ""
   translatedSentences = []
   if len(x) > 100:
         split_strings = []
         temp = ''
         for index in range(0, len(x)):
            if x[index] != '.' and x[index] != '!':
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
   else:
      #print('orginal text: ',x)
      result = (ts.google(x))
      #print('translated text: ', result)
      translatedSentences.append(result)
      translatedString+=result
   
   return translatedString


truthList = ["true", "truth"]
falseList = ["false", "fake"]

# selenium webdriver settings
options = Options()
options.headless = True
options.add_argument("--window-size=1920,1080")

chromeOptions = webdriver.ChromeOptions()
chromeOptions.binary_location = "C:\Program Files\Google\Chrome\Application\chrome.exe" 
driver = webdriver.Chrome("C:\\Users\\tarap\\Dropbox\\My PC (LAPTOP-EFB1H1KE)\\Desktop\\CSE472\\project2\\chromedriver.exe",  options=chromeOptions)

content = driver.page_source
soup = BeautifulSoup(content, features="html.parser")


#myParser = ParseHTML()
termFrequency = CountVectorizer()
counter = 0
counter2 = 0

#train variables
collected_URLs_Train = []
collected_HTML_Train = []
titles_Train = []
articles_Train = []
model_train_list = []
expected_label = []
labelCounter = 0
tfInput = []
collected_source = []

df_train = pd.read_csv("datasets/train.csv")

#test variables
collected_URLs_Test = []
collected_HTML_Test = []
titles_Test = []
articles_Test = []
model_test_list = []
expected_label = []
testCounter = 0
testTFInputs = []
df_test = pd.read_csv("datasets/test.csv")

#iterate through the training df and get the column values for the label and source
for i in range(len(df_train)):
    if(df_train.values[i][3] not in collected_source):
        collected_source.append(df_train.values[i][3])
#iterate through the testing df and get the column values for the label and source
for i in range(len(df_test)):
    if(df_test.values[i][3] not in collected_source):
        collected_source.append(df_test.values[i][3])

print(collected_source)

with open('createdCSVs/test_dataInputSource.csv', 'w', encoding='UTF8') as file:
   writer = csv.writer(file, lineterminator='\n')
   writer.writerow(collected_source)
   file.close()

trainheaders = collected_source
trainheaders.append('expected_label')
#write header of csv to file
with open('createdCSVs/train_dataInputSource.csv', 'w', encoding='UTF8') as file:
   writer = csv.writer(file, lineterminator='\n')
   writer.writerow(trainheaders)
   file.close()

# create feature vector
for index, row in df_train.iterrows():
    rowToSet = []
    sourceGiven = row[3]
    labelGiven = row[4]
    for value in collected_source:
        if value == sourceGiven:
            rowToSet.append(1)
        else:
            rowToSet.append(0)
    rowToSet.append(labelGiven)
    with open('createdCSVs/train_dataInputSource.csv', 'a+', encoding='UTF8') as file:
        writer = csv.writer(file, lineterminator='\n')
        writer.writerow(rowToSet)
        file.close()


for index, row in df_test.iterrows():
    rowToSet = []
    sourceGiven = row[3]
    
    for value in collected_source:
        
        if value == sourceGiven:
            rowToSet.append(1)
        else:
            rowToSet.append(0)

    with open('createdCSVs/test_dataInputSource.csv', 'a+', encoding='UTF8') as file:
        writer = csv.writer(file, lineterminator='\n')
        writer.writerow(rowToSet)
        file.close()

#write header to submission csv
headers = ['Id','Predicted']
with open('highestScoringSolutions/BESTofficialSubmissionTestMNB.csv', 'w', encoding='UTF8') as file:
   writer = csv.writer(file, lineterminator='\n')
   writer.writerow(headers)
   file.close()
tfList = []

readInputDF = pd.read_csv('createdCSVs/train_dataInputSource.csv')
labelsList = readInputDF["expected_label"].tolist()

readInputDF.drop(columns=readInputDF.columns[-1], 
        axis=1, 
        inplace=True)

for index, row in readInputDF.iterrows():
    tfList.append(row)

# set classification model to naive bayes and fit
myModel = MultinomialNB(alpha=0.5)
myModel.fit(tfList, labelsList)
print(myModel)

#write to csv
counter = 1 
readTestDF = pd.read_csv('createdCSVs/test_dataInputSource.csv')
for index, row in readTestDF.iterrows():
    predValueArray = myModel.predict([row])
    predictionValue = predValueArray[0]
    with open('highestScoringSolutions/BESTofficialSubmissionTestMNB.csv', 'a+', encoding='UTF8') as file:
        writer = csv.writer(file, lineterminator='\n')
        writer.writerow([counter, predictionValue])
        file.close()
    counter+=1