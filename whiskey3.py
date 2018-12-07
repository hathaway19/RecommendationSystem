import io # To help get panda methods to write to text file rather than the terminal
import pandas as pd
import numpy as np
import matplotlib as plt
import matplotlib.pyplot as plt

if __name__ == "__main__":
    # Set pandas to display all of the columns
    pd.set_option('display.max_columns', None)
    # Set pandas to have no limit on the width when printing to console
    pd.set_option('display.width', None)

    # Load our data into a dataframe
    df = pd.read_csv("data\whiskey\whiskey.csv")

    # Drop the columns that we don't need
    df = df.drop(['Timestamp', 'Link To Reddit Review', 'Date of Review', "Reviewer's Reddit Username", 'Full Bottle Price Paid'], axis=1)

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

    # Get rid of extra white space to ensure grouping (for reviews of the same whiskey) work
    df['Whisky Name'] = df['Whisky Name'].str.strip()
    df['Whisky Region or Style'] = df['Whisky Region or Style'].str.strip()
    
    # Get rid of all whiskeys that have less than 20 reviews
    df = df[df['Whisky Name'].isin(df['Whisky Name'].value_counts()[df['Whisky Name'].value_counts()>=20].index)]

    # Group results by whiskey
    df_by_whiskey = df.groupby('Whisky Name')

    df_count_for_whiskey = df_by_whiskey.count().rename(index=str, columns={"Reviewer Rating": "count"})
    df_score_for_whiskey = df_by_whiskey.mean().rename(index=str, columns={"Reviewer Rating": "score"})

    # Combine the results for the count and the avg score
    df_final = pd.concat([df_count_for_whiskey, df_score_for_whiskey], axis=1)

    # Calculate the overall mean of the ratings
    C = df['Reviewer Rating'].mean()

    # Init a new column for our weighted scores
    df_final['weighted_score'] = ''

    # Calculate the weighted score for each whiskey
    weighted_scores = []   
    for index, row in df_final.iterrows():
        v = row['count']
        R = row['score']
        weighted_scores.append((v/(v+20) * R) + (20/(20+v) * C))

    df_final['weighted_score'] = weighted_scores

    # Sort whiskeys based on score calculated above
    df_final = df_final.sort_values('weighted_score', ascending=False)
    
    print(df_final[['count', 'score', 'weighted_score']])
    
    ### Scaterplot
    # plt.scatter(df_count_for_whiskey, df_score_for_whiskey)
    # plt.xlabel('Num. Reviews')
    # plt.ylabel('Avg. Score')
    # plt.title('Number of Reviews & Avg Score')
    # plt.show()

    # plt.scatter(df_final['count'],df_final['weighted_score'])
    # plt.xlabel('Num. Reviews')
    # plt.ylabel('Weighted Avg. Score')
    # plt.title('Number of Reviews & Weighted Avg Score')
    # plt.show()

    ## Bar Graph
    # print(df_count_for_whiskey.values)
    # print(df_count_for_whiskey['Reviewer Rating'].values)
    # plt.bar(df['Whisky Name'].values, df_count_for_whiskey['Reviewer Rating'].values, align='center', alpha=0.5)
    # plt.xticks(df['Whisky Name'].values, objects)
    # plt.ylabel('Num. Reviews')
    # plt.title('Reviews For Whiskey')
    # plt.show()

    # df_final = df_final.sort_values('count', ascending=True)
    # df_final['count'].head(20).plot(kind="bar")
    # plt.xlabel('Num. Reviews')
    # plt.show()