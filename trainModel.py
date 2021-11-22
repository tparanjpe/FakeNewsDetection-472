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



submissionHeader = ['Id','Predicted']
with open('highestScoringSolutions/BESTofficialSubmissionLR.csv', 'w', encoding='UTF8') as file:
   writer = csv.writer(file, lineterminator='\n')
   writer.writerow(submissionHeader)
   file.close()
tfList = []
readInputDF = pd.read_csv('createdCSVs/train_data.csv')
labelsList = readInputDF["expectedLabel"].tolist()

readInputDF.drop(columns=readInputDF.columns[-1], 
        axis=1, 
        inplace=True)

for index, row in readInputDF.iterrows():
    tfList.append(row)

myModel = LogisticRegression(solver='liblinear', C=0.01)
myModel.fit(tfList, labelsList)
print(myModel)


counter = 1 
readTestDF = pd.read_csv('createdCSVs/test_dataInput.csv')
for index, row in readTestDF.iterrows():
    predValueArray = myModel.predict([row])
    predictionValue = predValueArray[0]
    with open('highestScoringSolutions/BESTofficialSubmissionLR.csv', 'a+', encoding='UTF8') as file:
        writer = csv.writer(file, lineterminator='\n')
        writer.writerow([counter, predictionValue])
        file.close()
    counter+=1
