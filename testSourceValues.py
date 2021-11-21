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

# class ParseHTML(HTMLParser):
#    dataReturned = ""
#    def handle_data(self, data):
#       #self.dataReturned.append(data)
#       self.dataReturned+=data
#       #print("Encountered some data  :", data)

# def remove_dataComponents(htmlContent):
#    mySoup = BeautifulSoup(htmlContent, "html.parser")
#    for data in mySoup(['style', 'script']):
#       data.decompose()
#    return ' '.join(soup.stripped_strings)

# #contentToTranslate:String with HTML data
# def translateContent(x):
#    translatedString = ""
#    translatedSentences = []
#    if len(x) > 100:
#          split_strings = []
#          temp = ''
#          for index in range(0, len(x)):
#             if x[index] != '.' and x[index] != '!':
#                temp += x[index]
#                # print(temp)
#             else:
#                split_strings.append(temp)
#                temp = ''
#          #print(split_strings)
#          for y in split_strings:
#             #print('orginal text: ',y)
#             result = (ts.google(y))
#             #print('translated text: ', result)
#             translatedSentences.append(result)
#             translatedString+=result
#    else:
#       #print('orginal text: ',x)
#       result = (ts.google(x))
#       #print('translated text: ', result)
#       translatedSentences.append(result)
#       translatedString+=result
   
#    return translatedString


truthList = ["true", "truth"]
falseList = ["false", "fake"]

options = Options()
options.headless = True
options.add_argument("--window-size=1920,1080")

# chromeOptions = webdriver.ChromeOptions()
# chromeOptions.binary_location = "C:\Program Files\Google\Chrome\Application\chrome.exe" 
# driver = webdriver.Chrome("C:\\Users\\tarap\\Dropbox\\My PC (LAPTOP-EFB1H1KE)\\Desktop\\CSE472\\project2\\chromedriver.exe",  options=chromeOptions)

# content = driver.page_source
# soup = BeautifulSoup(content, features="html.parser")


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

#parse data.data to get the URLs
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


for i in range(len(df_train)):
    if(df_train.values[i][3] not in collected_source):
        collected_source.append(df_train.values[i][3])

for i in range(len(df_test)):
    if(df_test.values[i][3] not in collected_source):
        collected_source.append(df_test.values[i][3])

print(collected_source)

# with open('test_dataInputSource.csv', 'w', encoding='UTF8') as file:
#    writer = csv.writer(file, lineterminator='\n')
#    writer.writerow(collected_source)
#    file.close()

trainheaders = collected_source
trainheaders.append('expected_label')

with open('train_dataInputSource.csv', 'w', encoding='UTF8') as file:
   writer = csv.writer(file, lineterminator='\n')
   writer.writerow(trainheaders)
   file.close()

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
    with open('train_dataInputSource.csv', 'a+', encoding='UTF8') as file:
        writer = csv.writer(file, lineterminator='\n')
        writer.writerow(rowToSet)
        file.close()


# for index, row in df_test.iterrows():
#     rowToSet = []
#     sourceGiven = row[3]
    
#     for value in collected_source:
        
#         if value == sourceGiven:
#             rowToSet.append(1)
#         else:
#             rowToSet.append(0)

#     with open('test_dataInputSource.csv', 'a+', encoding='UTF8') as file:
#         writer = csv.writer(file, lineterminator='\n')
#         writer.writerow(rowToSet)
#         file.close()


