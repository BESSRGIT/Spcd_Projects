# -*- coding: utf-8 -*-
"""
Created on Tue Dec 18 09:36:39 2018

"Spiced Academy" Assessment:

A dataset of 20 color-coded (x/y) points is given. The task is to implement a
k-means clustering algorithm, which divides the points into two separate groups.

@author: B. Gür
"""
# import libraries, packages, functionalities etc
import pandas as pd
from math import sqrt
# import matplotlib.pyplot as plt


# Open and read datafile
filename = 'SA_Assessment.xlsx'
Data = pd.ExcelFile(filename)
Data_DF = Data.parse('SA_Assessment')


# Rearrange dataset, reducing it to 3 colums x, y and color
left_set = Data_DF[['x', 'y', 'color' ]]
right_set = Data_DF[['x.1', 'y.1', 'color.1' ]]
combined_set = pd.concat([left_set,right_set.rename(columns={'x.1':'x', 'y.1':'y', 'color.1':'color'})], ignore_index=True)


# Task 1: Calculate means for x and y
#x_mean = combined_set.mean()[0]
#y_mean = combined_set.mean()[1]
x_mean, y_mean = combined_set.mean()

# Task 2: Determine red_center and blue_center
# Separate "combined_set" into two datasets, countaining only red or blue points
indices_r = combined_set['color'] == 'red'
Data_Red = combined_set.loc[indices_r, :]

indices_b = combined_set['color'] == 'blue'
Data_Blue = combined_set.loc[indices_b, :]


# Calculate red_center and blue_center
red_center_x = Data_Red.mean()[0]
red_center_y = Data_Red.mean()[1]
red_center = (red_center_x, red_center_y)

blue_center_x = Data_Blue.mean()[0]
blue_center_y = Data_Blue.mean()[1]
blue_center = (blue_center_x, blue_center_y)


# Task 3: Calculate the euclidean distance from each point to blue_center and red_center
distance_red = []
distance_blue = []

for index, row in combined_set.iterrows():
    dist =  sqrt(((red_center_x - combined_set.loc[index][0])**2)   +  (red_center_y - combined_set.loc[index][1])**2)
    distance_red.append(dist)

for index, row in combined_set.iterrows():
    dist =  sqrt(((blue_center_x - combined_set.loc[index][0])**2)   +  (blue_center_y - combined_set.loc[index][1])**2)
    distance_blue.append(dist)


# Task 4: Relabelling points based on their distance to red_center and blue_center
Diff_red_blue = []

for i in range(len(distance_red)):
    diff = distance_red[i] - distance_blue[i]
    Diff_red_blue.append(diff)

Relabelled = []
for i in range(len(Diff_red_blue)):
    if Diff_red_blue[i] > 0:
        Relabelled.append('red')
    else:
        Relabelled.append('blue')


# Lists --> Dataframes  (probably not needed)
distance_red_df = pd.DataFrame(distance_red, columns = ['Distance to red_center'])
distance_blue_df = pd.DataFrame(distance_blue, columns = ['Distance to blue_enter'])
Diff_red_blue_df = pd.DataFrame(Diff_red_blue, columns = ['Difference'])
Relabelled_df = pd.DataFrame(Relabelled, columns = ['Relabelled Color Code'])


# Generate new dataset containing all generated information
New_Dataset = pd.concat([combined_set, distance_red_df, distance_blue_df, Diff_red_blue_df, Relabelled_df], axis = 1)


# New datasets for red and blue points
indices_nr = New_Dataset['Relabelled Color Code'] == 'red'
New_Red = New_Dataset.loc[indices_nr, :]

indices_nb = New_Dataset['Relabelled Color Code'] == 'blue'
New_Blue = New_Dataset.loc[indices_nb, :]


# Tried to plot for comparison, unfortunately didn't work out :(  Still left the code in though
#plt.subplot(1, 2, 1)
#plt.scatter(Data_Red['x'], Data_Red['y'], color='r')
#plt.scatter(Data_Blue['x'], Data_Blue['y'], color='b')
#plt.title('Original')
#plt.xlabel('x')
#plt.ylabel('y')
#plt.subplot(1, 2, 2)
#plt.scatter(New_Red['x'], New_Red['y'],  color='r')
#plt.scatter(New_Blue['x'], New_Blue['y'],  color='b')
#plt.title('Relabelled')
#plt.xlabel('x')
#plt.ylabel('y')
#plt.subplots_adjust(wspace = 0.5)
#plt.show()
#plt.savefig('Relabelled')
