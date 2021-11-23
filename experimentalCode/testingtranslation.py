'''
Authors: Stephanie Lee and Tara Paranjpe
Project: CSE472 - Fake News Detection
Fall 2021
File Description: This short file contains snippet code used to test the translation api
'''
#go through each URL and translate  titles[] (already stored)
for x in collected_URLs:
   driver.get(x)
   
   content = driver.page_source
   soup = BeautifulSoup(content, features="html.parser")

   translatedSentences = []
   translatedArticles = []

   for x in titles:

      print("x length: ", len(x))
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
         print(split_strings)
         for y in split_strings:
            print('orginal text: ',y)
            result = (ts.google(y))
            print('translated text: ', result)
            translatedSentences.append(result)
      else:
         print('orginal text: ',x)
         result = (ts.google(x))
         print('translated text: ', result)
         translatedSentences.append(result)
      
   print("translated sentences: ", translatedSentences)
   