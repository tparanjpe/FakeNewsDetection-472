# Fake News Detection Using NLP Techniques and Machine Learning

### CSE472 Social Media Mining
### By Tara Paranjpe and Stephanie Lee

## Run instructions
There are 2 main python files:
* testscraper.py: This file is the  main source file that includes web scraping with Selenium webdriver and BeautifulSoup. Our program gathers the content from the websites and immediately processes it through a translator, which will then be used to calculate term frequency. The model is trained using Logistic Regression classification model.
  * To run this file, change the chrome driver and binary path to the paths in your machine
  * Please note that scraping the websites may take a while, so we have included the trainModel.py file that has the same function as testscraper.py but omits the data gathering part. It uses the csv file that we have already gathered from running testscraper.py
* trainModel.py: Run this file instead if you do not wish to scrape the websites. This file will train the model from the data from the already gathered csv file located in createdCSVs folder. Since this file does not scrape the web, Selenium webdriver is not used.

## Folders and Organization
There are 4 subfolders total:
* createdCSVs: Contains all the csv files
* datasets: Contains all the datasets
* experimentalCode: Contains all the experimental .py files
* highestScoringSolutions: Contains the csv files that scored the best when running with Least Squared Error metric.

There are 2 txt files and 1 README file
* actionPlan.txt: This file details our plannings and research that took place at the beginning of the project
* README.md: Contains run instructions and folder/organization details
* requirements.txt: This file contains all the python packages and version used
