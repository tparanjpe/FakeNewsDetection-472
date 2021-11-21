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

# class ParseHTML(HTMLParser):
#    dataReturned = ""
#    def handle_data(self, data):
#       #self.dataReturned.append(data)
#       self.dataReturned+=data
#       #print("Encountered some data  :", data)

def remove_dataComponents(htmlContent):
   mySoup = BeautifulSoup(htmlContent, "html.parser")
   for data in mySoup(['style', 'script']):
      data.decompose()
   return ' '.join(soup.stripped_strings)

#contentToTranslate:String with HTML data
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
#parse data.data to get the URLs
df_train = pd.read_csv("datasets/train.csv")
headers = ["truthcount","falsecount", "expectedLabel"]

with open('train_dataInput4.csv', 'w', encoding='UTF8') as file:
   writer = csv.writer(file)
   writer.writerow(headers)
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



# testTFInputs.append([0, 1])
# for myPair in testTFInputs:
#    print(myPair)
#    print([myPair])
# this is how to get specific item from csv data
# i iterates through the row(number of data entries) and the second array access is the column
for i in range(len(df_train)):
   collected_URLs_Train.append(df_train.values[i][5]) 
   expected_label.append(int(df_train.values[i][4]))


#loop through URLs to get data from websites
for x in collected_URLs_Train:
   print("URL" + x)
   label = expected_label[labelCounter]
   labelCounter+=1

   try:
      
      driver.get(x)
      
      content = driver.page_source
      soup = BeautifulSoup(content, features="html.parser")

      #check if most of the website titles are in h1 and record how many
      if soup.find('h1'):
         # print('found h1')
         if(soup.find('h1').getText()):
            titles_Train.append(soup.find('h1').getText()) 
            print('content of h1: '+ titles_Train[counter])
            counter = counter + 1
         else:
            print('no value found in h1, URL: '+ x)
      
      # print(content)
      collected_HTML_Train.append(content)
      dataToBeTranslated = remove_dataComponents(content)

      Englishstr = translateContent(dataToBeTranslated)
      print(Englishstr)
      #gets the data from the html file and adds it to a class array
      myTerms = [Englishstr]
   
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
      with open('train_dataInput4.csv', 'a+', encoding='UTF8') as file:
         writer = csv.writer(file)
         writer.writerow([falseCount, truthCount, label])
         file.close()

   except:
      #error was thrown, we can scrap the train data for this one.
      print("error was thrown, scraping train data")


#this will write all the input data to the csv. 
train_data = pd.DataFrame(model_train_list, columns=["truthcount","falsecount", "expectedLabel"])
train_data.to_csv('train_dataInput.csv', index=False)

# readInputDF = pd.read_csv('train_dataInput.csv')
# labelsList = readInputDF["expectedLabel"].tolist()

# print(tfInput)
# print(labelsList)

# myModel = KNeighborsClassifier(n_neighbors=4)
# myModel.fit(tfInput, labelsList)
# print(myModel)

# # this is how to get specific item from csv data
# # i iterates through the row(number of data entries) and the second array access is the column
# for i in range(len(df_test)):
#    collected_URLs_Test.append(df_test.values[i][4]) 


# #loop through URLs to get data from websites
# for x in collected_URLs_Test:
#    testCounter+=1
#    try:
#       driver.get(x)
      
#       content = driver.page_source
#       soup = BeautifulSoup(content, features="html.parser")

#       #check if most of the website titles are in h1 and record how many
#       if soup.find('h1'):
#          # print('found h1')
#          if(soup.find('h1').getText()):
#             titles_Test.append(soup.find('h1').getText()) 
#             print('content of h1: '+ titles_Test[counter2])
#             counter2 = counter2 + 1
#          else:
#             print('no value found in h1, URL: '+ x)
      
#       # print(content)
#       collected_HTML_Test.append(content)
#       dataToBeTranslated = remove_dataComponents(content)

#       Englishstr = translateContent(dataToBeTranslated)

#       #gets the data from the html file and adds it to a class array
#       #myParser.feed(Englishstr)
#       myTerms = [Englishstr]
#       # with open("Output.txt", "w") as text_file:
#       #    text_file.write(myParser.dataReturned)
#       #gets the term frequency values for each word in the data
#       termFrequencyResults=termFrequency.fit_transform(myTerms)
#       myTerms = pd.DataFrame(termFrequencyResults.toarray(), columns=termFrequency.get_feature_names())
#       # print(myTerms)
#       truthCount = 0
#       for term in truthList:
#          try:
#             myVal = myTerms[term]
#             truthCount += myVal.get(key=0)
#          except:
#             print(term + " not found")

#       falseCount = 0
#       for term in falseList:
#          try:
#             myVal = myTerms[term]
#             falseCount += myVal.get(key=0)
#          except:
#             print(term + " not found")

#       testTFInputs.append([falseCount, truthCount])
      
      
#    except:
#       print("error thrown")
#       testTFInputs.append([-1, -1])

# #this will write all the input data to the csv. 
# testInputs = pd.DataFrame(testTFInputs, columns=["truthcount","falsecount"])
# testInputs.to_csv('test_dataInput.csv', index=False)    



# predictionCounter = 1
# for myPair in testTFInputs:
#    if(myPair[0] == -1 and myPair[1] == -1):
#       model_test_list.append([testCounter, 3])
#    else:
#       predictionValue = myModel.predict([myPair])
#       print(predictionValue)
#       model_test_list.append([testCounter, predictionValue[0]])

# #print(model_test_list)
# outputDF = pd.DataFrame(model_test_list, columns=["Id","Predicted"])
# #print(outputDF)
# outputDF.to_csv('submission.csv', index=False)

#pass in the false count and true count and claim for each article, and corresponding label in another array
#knearest neighbors with btoh arrays
#run same pre-processing on test data, and pass that into the model to predict result