#Importing packages
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
from sklearn.linear_model import LogisticRegression


headers = ['Id','Predicted']
with open('officialSubmissionLR.csv', 'w', encoding='UTF8') as file:
   writer = csv.writer(file, lineterminator='\n')
   writer.writerow(headers)
   file.close()
tfList = []
readInputDF = pd.read_csv('train_data.csv')
labelsList = readInputDF["expectedLabel"].tolist()

for tValue, fValue in zip(readInputDF.truthcount, readInputDF.falsecount):
    tfList.append([tValue, fValue])

#myModel = KNeighborsClassifier(n_neighbors=4)
myModel = LogisticRegression()
myModel.fit(tfList, labelsList)
print(myModel)

counter = 1
readTestDF = pd.read_csv('test_dataInput.csv')
for tValue, fValue in zip(readTestDF.truthcount, readTestDF.falsecount):
    if tValue == -1 and fValue == -1:
        predictionValue = 0
    else:
        predValueArray = myModel.predict([[tValue, fValue]])
        predictionValue = predValueArray[0]
    with open('officialSubmissionLR.csv', 'a+', encoding='UTF8') as file:
        writer = csv.writer(file, lineterminator='\n')
        writer.writerow([counter, predictionValue])
        file.close()
    counter+=1

    