# -*- coding: utf-8 -*-
"""
Created on Mon Jan 14 11:07:58 2019

Spiced Academy Project-02:  With this side project I try to learn a bit more
about the LogisticRegression function. I would like to know, if and and how
coefficients change, when parameters are either added or calculated in a 
different sequence. For simplicity purposes and eventual comparisons the 
"Titanic" data is being used. 

@author: DataCoach
"""
# Import Libraries and read dataset
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from random import shuffle
import time

fn_train = 'train.csv'
df_train = pd.read_csv(fn_train)

# Pre-Processing: Design training dataframe, with (transformed) features to 
# be used for modelling. Transformed features are values of type 'str' to 
# 'int' or 'float' e.g. female --> 1, male --> 0 

# Calculate average age
average_age = df_train['Age'].dropna().mean()

# Add columns, where ...
# nan's in 'Age' column are replaced with average age
# letters in 'Sex' column are replaced with integers
# letters in 'Embarked' column are replaced with integers
df_train['Age_complete'] = df_train['Age'].replace(np.nan, average_age)

df_train['Gender'] = df_train['Sex'].replace(['female', 'male'], [1, 0])

list_emb = [np.nan, 'C', 'Q', 'S']
list_emb_num = [0,1,2,3]
df_train['Embarked_num'] = df_train['Embarked'].replace(list_emb, list_emb_num)

# Define y column for regression, i.e. in this case the column 'Survived'
y_train = df_train['Survived'] 


# Perform Logistic Regression in a loop with varying starting parameters and
# varying sequences of the parameters 

LogReg = LogisticRegression(C=1e5)
number_of_runs = range(1,11)

for n in number_of_runs:
    
# Starting Features
    features = ['Pclass', 'Age_complete', 'Gender', 'Embarked_num', 'Fare', 'SibSp', 'Parch']
    shuffle(features)

# Generate empty lists 
    coef_list  = []
    score_list = []
    Pclass_coef = []    
    Age_coef = []
    Gender_coef = []
    Embarked_coef = []
    Fare_coef = []
    SibSp_coef = []
    Parch_coef = []

# Identify indices of features after shuffle
    Pclass_index    = features.index('Pclass')
    Age_index       = features.index('Age_complete')
    Gender_index    = features.index('Gender')
    Embarked_index  = features.index('Embarked_num')
    Fare_index      = features.index('Fare')
    SibSp_index     = features.index('SibSp')
    Parch_index     = features.index('Parch')

# Perform logistic regression 
    for i in range(1, len(features) + 1):
        X_matrix = df_train[features[0:i]]
        LogReg.fit(X_matrix, y_train)
        score = LogReg.score(X_matrix, y_train)
        coef = list(LogReg.coef_[0])
        fit_extend = len(features) - len(coef)
        fit_extend = list(np.full(fit_extend, np.nan)) # fill empty spaces with nan's
        coef.extend(fit_extend)
        coef_list.append(coef)
        score_list.append(score)
 
# Generate matrix with all coefficients and scores     
    for j in range(0, len(features)):
        Pclass_coef.append(coef_list[j][Pclass_index])
        Age_coef.append(coef_list[j][Age_index])
        Gender_coef.append(coef_list[j][Gender_index])
        Embarked_coef.append(coef_list[j][Embarked_index])
        Fare_coef.append(coef_list[j][Fare_index])
        SibSp_coef.append(coef_list[j][SibSp_index])
        Parch_coef.append(coef_list[j][Parch_index])

    Coef_Score_Matrix = pd.DataFrame(np.column_stack([Pclass_coef, Age_coef,
                                            Gender_coef, Embarked_coef,
                                            Fare_coef, SibSp_coef, 
                                            Parch_coef, score_list]),
                               columns = ['Pclass', 'Age', 'Gender',
                                          'Embarked', 'Fare', 'SibSp', 
                                          'Parch', 'Score'])   

# Generate string for identification and sequence of parameters
    f = str()
    for s in range(0, len(features)):
        f = f + (str(features[s][0:2]))

# Write to excel including timestamp and above mentioned sequence string
    t = time.localtime()
    timestamp = time.strftime('%Y%m%d_%H%M%S', t)
    Coef_Score_Matrix.to_excel(str(timestamp) + '_Coefficients_' + f + '.xlsx')


# Data analysis and visualization 
######
#TO BE DONE
######

 






    
