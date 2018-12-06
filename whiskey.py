##
# Author: Justin A. Hathaway
# Class: CS 391
# Assignment: Final Project
##

import io # To help get panda methods to write to text file rather than the terminal
import pandas as pd
import numpy as np
import matplotlib as plt
import matplotlib.pyplot as plt

# Set pandas to display all of the columns
pd.set_option('display.max_columns', None)
# Set pandas to have no limit on the width when printing to console
pd.set_option('display.width', None)

# Load our data into a dataframe
df = pd.read_csv("data\whiskey\whiskey.csv")

# Drop the columns that we don't need
df = df.drop(['Timestamp', 'Link To Reddit Review', 'Date of Review', "Reviewer's Reddit Username", 'Full Bottle Price Paid', 'Whisky Region or Style'], axis=1)

# Get rid of all non-numeric values in 'Reviewer Rating'
df['Reviewer Rating'] = df['Reviewer Rating'].str.extract('(\d+)', expand=False)

# Drop Reviews that are null or are just white space
df['Reviewer Rating'].str.strip().replace('', np.nan, inplace=True)
df = df.dropna(subset=['Reviewer Rating'])

# Convert the ratings to integers
df['Reviewer Rating'] = df['Reviewer Rating'].astype(str).astype(float)

# Only keep ratings between 0 and 100
df = df[~(df['Reviewer Rating'] >= 100)]  
df = df[~(df['Reviewer Rating'] < 0)] 

# Open a text file to pipe our results to
answers = open('whiskey.txt', 'w')

# Display the number of reviews
answers.write("Number of Reviews: ")
answers.write(str(len(df.index)) + "\n\n")

df['Whisky Name'] = df['Whisky Name'].str.strip()

answers.write("First 5 entries (after removing cols 'Timestamp, 'Link to Reddit Review', 'Date of Review': \n")
answers.write(str(df.head(5)))

occurances = df['Whisky Name'].value_counts()

item_list = occurances.index


mean_per_whiskey = df.groupby('Whisky Name').mean()

# The average rating for a whiskey
avg_rating = mean_per_whiskey.mean()

print(df.shape)
df = df[df['Whisky Name'].isin(df['Whisky Name'].value_counts()[df['Whisky Name'].value_counts()>=20].index)]
print(df.shape)

occurances = df['Whisky Name'].value_counts()
print(occurances)
###########################################
df_by_whiskey = df.groupby('Whisky Name')
print(df_by_whiskey.describe())
print(list(df_by_whiskey)[1])
# print(df_by_whiskey.index)



# indices = pd.Series(df.groupby('Whisky Name').index, index=metadata['title']).drop_duplicates()





answers.write(str(df.head(5)))

# Close the text file we've been writing to
answers.close()

# def weighted_rating(x, m=m, C=C):
