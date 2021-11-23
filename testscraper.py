'''
Authors: Stephanie Lee and Tara Paranjpe
Project: CSE472 - Fake News Detection
Fall 2021
File Description: This file uses the Selenium Web Scraper package to analyze the fact check articles, srape the contents, translate it, 
run term frequency on the text, and train our Logistic Regression model. 
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
from sklearn.linear_model import LogisticRegression
import translators as ts


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
   #in order to avoid hitting the Google Translate API limit, we have to break the strings up. 
   if len(x) > 100:
         split_strings = []
         temp = ''
         for index in range(0, len(x)):
            #split at period to indicate end of a sentence
            if x[index] != '.' and x[index] != '!':
               temp += x[index]
            else:
               split_strings.append(temp)
               temp = ''
         for y in split_strings:
            #translate the words and append them to a string to produce result
            result = (ts.google(y))
            translatedSentences.append(result)
            translatedString+=result
   else:
      result = (ts.google(x))
      translatedSentences.append(result)
      translatedString+=result
   
   return translatedString

#true and false lists for words to search for. 
truthList = ["true", "truth"]
falseList = ["false", "fake"]

#webdriver initialization
options = Options()
options.headless = True
options.add_argument("--window-size=1920,1080")

chromeOptions = webdriver.ChromeOptions()
#SPECIFY YOUR CHROME BINARY LOCATION PATH HERE!!
chromeOptions.binary_location = "C:\Program Files\Google\Chrome\Application\chrome.exe" 
#SPECIFY YOUR CHROME DRIVER LOCATION HERE!!
driver = webdriver.Chrome("C:\\Users\\tarap\\Dropbox\\My PC (LAPTOP-EFB1H1KE)\\Desktop\\CSE472\\project2\\chromedriver.exe",  options=chromeOptions)


# Initialize the Beautiful Soup object for parsing the data from Selenium
content = driver.page_source
soup = BeautifulSoup(content, features="html.parser")
#initialize the countvectorizer object
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
df_train = pd.read_csv("datasets/train.csv")
headers = ["truthcount","falsecount", "expectedLabel"]

#write the headers for the train_dataInput file
with open('createdCSVs/train_data.csv', 'w', encoding='UTF8') as file:
   writer = csv.writer(file)
   writer.writerow(headers)
   file.close()

#write the headers for the test_dataInput file
with open('createdCSVs/test_dataInput.csv', 'w', encoding='UTF8') as file:
   writer = csv.writer(file)
   writer.writerow(["truthcount","falsecount"])
   file.close()

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

#iterate through the training df and get the column values for the label and URL
#potential point for improvement: avoid for loop and grab the column using pandas!
for i in range(len(df_train)):
   collected_URLs_Train.append(df_train.values[i][5]) 
   expected_label.append(int(df_train.values[i][4]))

#loop through URLs to get data from websites
for x in collected_URLs_Train:
   #print out which url it is on
   print("URL" + x)
   label = expected_label[labelCounter]
   labelCounter+=1

   try:
      #use the webdriver to get the article
      driver.get(x)
      
      content = driver.page_source
      soup = BeautifulSoup(content, features="html.parser")

      #check if most of the website titles are in h1 and record how many
      if soup.find('h1'):
         # print('found h1')
         if(soup.find('h1').getText()):
            #append the title names
            titles_Train.append(soup.find('h1').getText()) 
            print('content of h1: '+ titles_Train[counter])
            counter = counter + 1
         else:
            print('no value found in h1, URL: '+ x)
      
      # print(content)
      collected_HTML_Train.append(content)
      #pass it in to remove_dataComponents to remove unneeded tags
      dataToBeTranslated = remove_dataComponents(content)

      #translate the text to english. 
      Englishstr = translateContent(dataToBeTranslated)
      print(Englishstr)

      myTerms = [Englishstr]
   
      #gets the term frequency values for each word in the data
      termFrequencyResults=termFrequency.fit_transform(myTerms)
      #stores TF results in a DF.
      myTerms = pd.DataFrame(termFrequencyResults.toarray(), columns=termFrequency.get_feature_names())


      #evaluate frequency of terms in both lists
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
      #store the results
      tfInput.append([falseCount, truthCount])
      model_train_list.append([falseCount, truthCount, label])

      #write the data to the file.
      with open('createdCSVs/train_data.csv', 'a+', encoding='UTF8') as file:
         writer = csv.writer(file)
         writer.writerow([falseCount, truthCount, label])
         file.close()

   except:
      #error was thrown, we can scrap the train data for this one.
      print("error was thrown, scraping train data")




# this is how to get specific item from csv data
# i iterates through the row(number of data entries) and the second array access is the column
for i in range(len(df_test)):
   collected_URLs_Test.append(df_test.values[i][4]) 


#loop through URLs to get data from websites
for x in collected_URLs_Test:
   testCounter+=1
   try:
      driver.get(x)
      
      content = driver.page_source
      soup = BeautifulSoup(content, features="html.parser")

      #check if most of the website titles are in h1 and record how many
      if soup.find('h1'):
         # print('found h1')
         if(soup.find('h1').getText()):
            titles_Test.append(soup.find('h1').getText()) 
            print('content of h1: '+ titles_Test[counter2])
            counter2 = counter2 + 1
         else:
            print('no value found in h1, URL: '+ x)
      
      # print(content)
      collected_HTML_Test.append(content)
      dataToBeTranslated = remove_dataComponents(content)

      Englishstr = translateContent(dataToBeTranslated)

      myTerms = [Englishstr]
    
      #gets the term frequency values for each word in the data
      termFrequencyResults=termFrequency.fit_transform(myTerms)
      myTerms = pd.DataFrame(termFrequencyResults.toarray(), columns=termFrequency.get_feature_names())

      #evaluate frequency
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

      #Write the data to the file
      testTFInputs.append([falseCount, truthCount])
      with open('createdCSVs/test_dataInput.csv', 'a+', encoding='UTF8') as file:
         writer = csv.writer(file)
         writer.writerow([falseCount, truthCount])
         file.close()
      
   except:
      print("error thrown")

      #if an error is thrown, we indicate it and mark it as -1, since we need the row for the test data.
      with open('createdCSVs/test_dataInput.csv', 'a+', encoding='UTF8') as file:
         writer = csv.writer(file)
         writer.writerow([-1, -1])
         file.close()




submissionHeader = ['Id','Predicted']
#write submission headers to the the file
with open('highestScoringSolutions/BESTofficialSubmissionLR.csv', 'w', encoding='UTF8') as file:
   writer = csv.writer(file, lineterminator='\n')
   writer.writerow(submissionHeader)
   file.close()
tfList = []
readInputDF = pd.read_csv('createdCSVs/train_data.csv')
labelsList = readInputDF["expectedLabel"].tolist()
#get rid of the last column for label.
readInputDF.drop(columns=readInputDF.columns[-1], 
        axis=1, 
        inplace=True)

for index, row in readInputDF.iterrows():
   tfList.append(row)


#this is our model! LR with liblinear solver and regularization strength of 0.01.
myModel = LogisticRegression(solver='liblinear', C=0.01)
myModel.fit(tfList, labelsList)
print(myModel)


counter = 1 
readTestDF = pd.read_csv('createdCSVs/test_dataInput.csv')
for index, row in readTestDF.iterrows():
   #get the prediction from the model for the test data
   predValueArray = myModel.predict([row])
   predictionValue = predValueArray[0]
   #store it in the submission file.
   with open('highestScoringSolutions/BESTofficialSubmissionLR.csv', 'a+', encoding='UTF8') as file:
      writer = csv.writer(file, lineterminator='\n')
      writer.writerow([counter, predictionValue])
      file.close()
   counter+=1
