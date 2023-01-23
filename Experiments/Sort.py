import csv
import pandas as pd
import numpy as np

# csv file name
filename = "C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/GitHubMasterSkripts/dfCSVfile2013cut.csv"


# reading csv file
# with open(filename, 'w') as csvfile:
#     # creating a csv reader object
#     csvreader = csv.reader(csvfile, delimiter = " ")

data = pd.read_csv(filename, sep=' ', dtype= int)


# iterating the columns
for col in data.columns:
    print(col)

# data['YY'] = pd.to_datetime(data['YY'])

# print(list(data.columns))  
# print(list(data.columns.values))


# checking datatype
#print(type(data.yy[0]))
 
#
print(data)


# for year in yy:
#     if yy == 2013:
#        df.to_csv("dfCSVfilefullnew2013.csv", sep=' ', index=False)
#     elif yy == 2014:
#         df.to_csv("dfCSVfilefullnew2014.csv", sep=' ', index=False)
#     else:


# df[pd.to_datetime(df.index).year == 2013]

# df_date= pd.to_datetime(df['YY'])


# print(df)