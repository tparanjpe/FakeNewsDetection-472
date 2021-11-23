'''
Authors: Stephanie Lee and Tara Paranjpe
Project: CSE472 - Fake News Detection
Fall 2021
File Description: This file is designed to run the already gathered code against our model and get predictions
This is designed as a driver for quick testing after the data has been gathered. 
'''

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



#headers for the submission csv
submissionHeader = ['Id','Predicted']
with open('highestScoringSolutions/BESTofficialSubmissionLR.csv', 'w', encoding='UTF8') as file:
   writer = csv.writer(file, lineterminator='\n')
   writer.writerow(submissionHeader)
   file.close()
tfList = []
readInputDF = pd.read_csv('createdCSVs/train_data.csv')
#extract the expectedLabel header
labelsList = readInputDF["expectedLabel"].tolist()

#remove the expected label from the model input
readInputDF.drop(columns=readInputDF.columns[-1], 
        axis=1, 
        inplace=True)

for index, row in readInputDF.iterrows():
    tfList.append(row)

#run our inputs against the logistic regression model
myModel = LogisticRegression(solver='liblinear', C=0.01)
myModel.fit(tfList, labelsList)
print(myModel)

#get the predictions and save them in the csv file
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
