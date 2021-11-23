'''
Authors: Stephanie Lee and Tara Paranjpe
Project: CSE472 - Fake News Detection
Fall 2021
File Description: This file was implemented by following a tutorial for machine learning using sklearn. This file was used for understanding machine learning.
'''

#following this tutorial:
#https://www.analyticssteps.com/blogs/what-naive-bayes-algorithm-machine-learning
#Trying figure out the predicter and target in data(the X and Y ) in few.data (only has 2 sets of data) but haven't done much

import matplotlib
import numpy as np
import pandas as pd
import seaborn as sns
sns.set(color_codes=True)
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler
 
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn import metrics
 

pima_df = pd.read_csv("../datasets/few.data")
 
X = pima_df.drop("Outcome", axis = 1)
Y = pima_df[ ["outcome"] ]
X_train, X_test, Y_train, Y_test = train_test_split(X,Y, test_size= 0.2, random_state = 1)
 
model = GaussianNB()
model.fit(X_train, Y_train)
Y_pred = model.predict(X_test)