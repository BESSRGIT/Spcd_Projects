# -*- coding: utf-8 -*-
"""
Created on Mon Jan  7 19:43:57 2019

Spiced Academy Project-01:
Analyzing Babynames based on US dataset from 1880 - 2017

@author: DataCoach
"""
#%%
# Import Libraries
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
#%%
"""
11.1.4 ANALYZE A DATASET WITH PANDAS
"""
"""
Read and write data
"""
# Read all .txt files in directory
years = range(1880, 2018, 1)
data = []
for y in years:
    fn = f'yob{str(y)}.txt'
    df = pd.read_csv(fn, names = ['name', 'gender', 'count'])
    df['year'] = y
    data.append(df)
df = pd.concat(data, ignore_index = True)

# Size of resulting dataframe
print(df.shape)

# Generate dataframe for the year 2000
df2000 = df[df['year'] == 2000]

# Print the first 10 entries
print(df2000.head(10))

# Write df2000 to file
df2000.to_excel('US_Babynames_2000.xls')
#%%
"""
# Calculate total birth
"""
# Calculate the sum of the birth count column in the file yob2000.txt.
sum_of_birth_2000 = df2000['count'].sum()
#%%
"""
Separate boys / girls
"""
# Calculate separate sums for boys and girls.
df2000_gender = df2000.groupby('gender')['count'].sum()

# Plot both sums in a bar plot
plt.bar(df2000_gender.index.values[0], df2000_gender[0], width = 0.4, color = 'r')
plt.bar(df2000_gender.index.values[1], df2000_gender[1], width = 0.4, color = 'b')
plt.title("Total birth' in 2000 separated by gender", fontweight = 'bold')
plt.xlabel('Gender')
plt.ylabel("counts(#)")
plt.xticks(np.arange(2), ('Female', 'Male'))
#%%
"""
Frequent names
"""
# Count how many names occur at least 1000 times in the file yob2000.txt.
df2000_1k = df2000[df2000['count']>= 1000].count()
#%%
"""
Relative amount
"""
# Create a new column containing the percentage of a name on the total births of a given year
df2000['percentage'] = df2000['count'] / sum_of_birth_2000 * 100

# Verify that the sum of percentages is 100%.
print(df2000['percentage'].sum())

# Calculate the percentage of the top 10 names on all births
df2000_sorted = df2000.sort_values(by = 'count', ascending = False)
df2000_top10 = df2000_sorted[0:10]['percentage'].sum()
#%%
"""
Search your name
"""
# Identify and print all lines containing your name in the year 2000
my_name = df2000[df2000['name'] == 'Bilgehan'].count()
#%%
"""
Bar plot
"""
# Create a bar plot showing 5 selected names for the year 2000
df2000_sorted[0:5].plot.bar('name', 'count', legend = None)
#%%
"""
Read all names (see above)
"""
#%%
"""
Plot a time series
"""
# Extract all rows containing your name from the variable df
#--------
# As "my_name" contains only zeros, this part is skipped.
# Alternative: Use a male-name that is close to "Bilgehan", such as "Billy"
#--------
df_Billy = df[(df['name'] == 'Billy') & (df['gender'] == 'M')]

# Plot the number of babies having Billy and male gender over time
# Make the plot nicer by adding row/column labels and a title
# Change the color and thickness of the line
df_Billy.plot('year', 'count')
plt.plot(df_Billy['year'], df_Billy['count'], color = 'r') # legend = None doesn't work ???
plt.grid(axis = 'y', color='black', linestyle='--', linewidth=0.2)
plt.xlabel('Year')
plt.ylabel('count (#)')
plt.title('Frequency of the name "Billy"', fontweight="bold")
plt.show()

# save the plot as a high-resolution diagram
plt.savefig(f'Frequency_Billy.png', dpi=600)
#%%%
#--------
# Comparison to solar spectrum :)
#--------
fn_solar = 'AM0AM1_5.xls'
column_names = ['wavelength', '--', 'Global Tilt', 'Direct+Circumsolar', 'nan', 'wavelength2', 'standard spectra' ]
solar = pd.read_excel(fn_solar, header = None, skiprows = 10, names = column_names)
wl_1 = solar['wavelength'][:1694]
wl_2 = solar['wavelength2'][:1439]

plt.plot(wl_2, solar['standard spectra'][:1439], color = 'r')
plt.plot(wl_1, solar['Global Tilt'][:1694], color = 'b')
plt.plot( wl_1, solar['Direct+Circumsolar'][:1694], color = 'g')
plt.grid(axis = 'y', color='black', linestyle='--', linewidth=0.2)
plt.xlabel('wavelength (nm)')
plt.ylabel('Spectral Irradiance (Wm$^{-2}$nm$^{-1}$)')
plt.title('Solar Spectrum', fontweight="bold")
plt.show()
plt.savefig(f'Solar Spectrum.png', dpi=600)
#%%
"""
Celebrities
"""
# Plot time lines of names of celebrities
#--------
# TO BE DONE
#--------
#%%
"""
Total births over time
"""
# Create a plot that shows the total birth rate in the U.S. over time
# Plot girls/boys separately
df_M = df[df['gender'] == 'M']
df_F = df[df['gender'] == 'F']
birth_rate = df.groupby('year')['count'].sum()
birth_rate_M = df_M.groupby('year')['count'].sum()
birth_rate_F = df_F.groupby('year')['count'].sum()

plt.plot(birth_rate.index.values, birth_rate, color = 'r')
plt.plot(birth_rate_M.index.values, birth_rate_M, color = 'b')
plt.plot(birth_rate_F.index.values, birth_rate_F, color = 'g')
plt.grid(axis = 'y', color='black', linestyle='--', linewidth=0.2)
plt.xlabel('Year')
plt.ylabel('birth (#)')
plt.title('Birthrate in the USA', fontweight="bold")
plt.show()
plt.savefig(f'US Birthrate.png', dpi=600)
#%%
"""
Normalize
"""
# divide the number of births by the total number of births in that
# year to obtain the relative frequency
# plot the time series of your name or the celebrity names again.
#--------
# TO BE DONE
#--------
#%%
"""
Name diversity
"""
# Have the baby names become more diverse over time?
# What assumptions is your calculation based upon?
name_div = df['name'].unique()
#--------
# TO BE DONE
#--------
#%%
"""
Long names
"""
# Add an extra column that contains the length of the name
def get_len(s):
    return(len(s))
name_length = df['name'].apply(get_len)
df['name length'] = name_length

# Print the 10 longest names to the screen
df_sorted = df.sort_values(by = 'name length', ascending = False)
print(df_sorted[0:10])
#%%
"""
First Letter Statistics
"""
# Add an extra column that contains the first letter of the name.
def get_initial(s):
    return(s[0])
first_letter = df['name'].apply(get_initial)
df['first letter'] = first_letter

# Count how many names start with ‘A’
num_of_A = df[df['first letter'] == 'A']['first letter'].count()
# num_of_B = df[df['first letter'] == 'B']['first letter'].count()
#%%
#--------
# TO BE CONTINUED
#--------
