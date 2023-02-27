import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.dates import date2num
import datetime
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('--year', type=int, help='The year to plot')
args = parser.parse_args()

# Read the header row separately to get the column names
#header = pd.read_csv('C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/GitHubMasterSkripts/MasterSkript/transform/output/AirtempTest.csv', nrows=1).columns

import pandas as pd

# Read in the CSV file ----> CHANGE NAME!
df = pd.read_csv('C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/GitHubMasterSkripts/MasterSkript/transform/output/Precipitation_NaN.csv', sep='\t')
# Get file_name ---> NEEDS to be CHANGED
file_name = os.path.basename('C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/GitHubMasterSkripts/MasterSkript/transform/output/Precipitation_NaN.csv')

# Extract the values from the Stat1 column
x = df['Stat1'].values

# Combine the datetime columns into a single datetime object
dates = [pd.Timestamp(int(row['YY']), int(row['MM']), int(row['DD']), int(row['HH']), int(row['MM.1'])) for i, row in df.iterrows()]

# Set the datetime index for the dataframe
df.index = dates

# Remove the YY, MM, DD, HH, and MM.1 columns from the dataframe
df = df.drop(columns=['YY', 'MM', 'DD', 'HH', 'MM.1'])

# Print the resulting dataframe
# print(df)

# Create a boolean mask of NaN values
mask = df['Stat1'].isna()

# Convert the boolean mask to 0 and 1 values
plot_data = mask.astype(int)

# Group the data by year
groups = df.groupby(df.index.year)

for year, group in groups:
    if args.year is None or year == args.year:
        fig, ax = plt.subplots()
        ax.plot(group.index, plot_data.loc[group.index])
        ax.set_title(str(year))
        plt.savefig(file_name + '_' + str(year) + '.png')
        plt.close(fig)