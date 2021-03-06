'''
Authors: Stephanie Lee and Tara Paranjpe
Project: CSE472 - Fake News Detection
Fall 2021
File Description: This file runs term frequency on the claims
'''

from sklearn import metrics
from sklearn.naive_bayes import MultinomialNB
from operator import truth
from bs4.element import Declaration
from numpy import vectorize
from scipy.stats.stats import RelfreqResult
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import json
import csv
from html.parser import HTMLParser
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.neighbors import KNeighborsClassifier
import translators as ts
import re
import nltk
from sklearn.metrics import classification_report
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))


termFrequency = CountVectorizer()
counter = 0
counter2 = 0

# train variables
collected_URLs_Train = []
collected_HTML_Train = []
titles_Train = []
articles_Train = []
model_train_list = []
expected_label = []
labelCounter = 0
tfInput = []
collected_source = []
collected_claim = []
collected_label = []
collected_claim_test = []

# parse train.csv to get the URLs
df_train = pd.read_csv("../datasets/train.csv")
headers = ["truthcount","falsecount", "expectedLabel"]

with open('../createdCSVs/train_data_TM_claim.csv', 'w', encoding='UTF8') as file:
   writer = csv.writer(file)
   writer.writerow(headers)
   file.close()

# test variables
collected_URLs_Test = []
collected_HTML_Test = []
titles_Test = []
articles_Test = []
model_test_list = []
expected_label = []
testCounter = 0
testTFInputs = []
df_test = pd.read_csv("../datasets/test.csv")

# get the claims and labels from train dataset
for i in range(len(df_train)):
    collected_claim.append(df_train.values[i][2])
    expected_label.append(int(df_train.values[i][4]))
# get the claims from test dataset
for i in range(len(df_test)):
    collected_claim_test.append(df_train.values[i][2])


# truth and false list
truthList = ["true", "truth", "real", "accurate", "correct", "not false", "not fake"]
falseList = ["false", "fake", "wrong", "inaccurate", "not true", "not fake"]

# Go through each claim and run term frequency
for x in collected_claim:
    try:
        myTerms = [x]
        label = expected_label[labelCounter]
        labelCounter+=1
        #gets the term frequency values for each word in the data
        termFrequencyResults=termFrequency.fit_transform(myTerms)
        myTerms = pd.DataFrame(termFrequencyResults.toarray(), columns=termFrequency.get_feature_names())
        # print(myTerms)
        truthCount = 0
        for term in truthList:
            try:
                myVal = myTerms[term]
                truthCount += myVal.get(key=0)
            except:
                print(term + " not found")

            falseCount = 0
        for term in falseList:
            try:
                myVal = myTerms[term]
                falseCount += myVal.get(key=0)
            except:
                print(term + " not found")
        tfInput.append([falseCount, truthCount])
        model_train_list.append([falseCount, truthCount, label])
        with open('../createdCSVs/train_data_TM_claim.csv', 'a+', encoding='UTF8') as file:
            writer = csv.writer(file)
            writer.writerow([falseCount, truthCount, label])
            file.close()
    except:
      #error was thrown, we can scrap the train data for this one.
      print("error was thrown, scraping train data")
      tfInput.append([-1, -1])
      with open('../createdCSVs/train_data_TM_claim.csv', 'a+', encoding='UTF8') as file:
         writer = csv.writer(file)
         writer.writerow([-1, -1, label])
         file.close()

