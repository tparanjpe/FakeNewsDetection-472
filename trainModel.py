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
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import PassiveAggressiveClassifier



headers = ['Id','Predicted']
with open('BESTofficialSubmissionTestMNB.csv', 'w', encoding='UTF8') as file:
   writer = csv.writer(file, lineterminator='\n')
   writer.writerow(headers)
   file.close()
tfList = []
readInputDF = pd.read_csv('train_dataInputSource.csv')
labelsList = readInputDF["expected_label"].tolist()

readInputDF.drop(columns=readInputDF.columns[-1], 
        axis=1, 
        inplace=True)

for index, row in readInputDF.iterrows():
    tfList.append(row)

#myModel = KNeighborsClassifier(n_neighbors=4)
#myModel = LogisticRegression(solver='liblinear')
#myModel = LogisticRegression(solver='liblinear', C=0.01)
myModel = MultinomialNB(alpha=0.5)
#myModel = PassiveAggressiveClassifier()
myModel.fit(tfList, labelsList)
print(myModel)

# counter = 1
# readTestDF = pd.read_csv('test_dataInput.csv')
# for tValue, fValue in zip(readTestDF.truthcount, readTestDF.falsecount):
#     if tValue == -1 and fValue == -1:
#         predictionValue = 0
#     else:
#         predValueArray = myModel.predict([[tValue, fValue]])
#         predictionValue = predValueArray[0]
#     with open('officialSubmissionTestPAC.csv', 'a+', encoding='UTF8') as file:
#         writer = csv.writer(file, lineterminator='\n')
#         writer.writerow([counter, predictionValue])
#         file.close()
#     counter+=1

counter = 1 
readTestDF = pd.read_csv('test_dataInputSource.csv')
for index, row in readTestDF.iterrows():
    predValueArray = myModel.predict([row])
    predictionValue = predValueArray[0]
    with open('BESTofficialSubmissionTestMNB.csv', 'a+', encoding='UTF8') as file:
        writer = csv.writer(file, lineterminator='\n')
        writer.writerow([counter, predictionValue])
        file.close()
    counter+=1