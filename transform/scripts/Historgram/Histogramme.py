import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.dates import date2num
import datetime
import argparse
import os
import numpy as np
import seaborn as sns

parser = argparse.ArgumentParser()
parser = argparse.ArgumentParser()
parser.add_argument('--year', type=int, help='The year to plot')
args = parser.parse_args()

# Read the header row separately to get the column names
#header = pd.read_csv('C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/GitHubMasterSkripts/MasterSkript/transform/output/AirtempTest2102.csv', nrows=1).columns

import pandas as pd

# Read in the CSV file ----> CHANGE NAME!
df = pd.read_csv('C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/GitHubMasterSkripts/MasterSkript/transform/output/AirtempTest2102.csv', sep='\t')
# Get file_name ---> NEEDS to be CHANGED
file_name = os.path.basename('C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/GitHubMasterSkripts/MasterSkript/transform/output/AirtempTest2102.csv')

# Extract the values from the Stat1 column
x = df['Stat1'].values

# Combine the datetime columns into a single datetime object
dates = [pd.Timestamp(int(row['YY']), int(row['MM']), int(row['DD']), int(row['HH']), int(row['MM.1'])) for i, row in df.iterrows()]


# Create a new column called 'date' by combining the individual date columns
df['date'] = pd.to_datetime(df[['YY', 'MM', 'DD', 'HH', 'MM.1']].rename(columns={'YY':'year', 'MM':'month', 'DD':'day', 'HH':'hour', 'MM.1':'minute' }))

# Set the datetime index for the dataframe
df.index = df['date']

# Remove the YY, MM, DD, HH, MM.1 and date columns from the dataframe
#df = df.drop(columns=['YY', 'MM', 'DD', 'HH', 'MM.1', 'date'])

# Group the data by year
groups = df.groupby(df['date'].dt.year)

# # Loop through each group and plot a histogram
# for year, group in groups:
#     plt.hist(group['Stat1'], bins=100)
#     plt.title(f'Histogram for {year}')
#     plt.xlabel('Stat1')
#     plt.ylabel('Count')
#     plt.show()

num_nan_values = df['Stat1'].isna().sum()
print(f'Number of NaN values: {num_nan_values}')

test_array = np.array([1, 2, np.nan, 3, 4])
finite_array = test_array[np.isfinite(test_array)]
print(finite_array)


for year, group in groups:
    data = group['Stat1'].replace(-9999, np.nan).values
    finite_data = data[np.isfinite(data)]
    hist, bins = np.histogram(finite_data, bins=100)
    bin_centers = (bins[1:] + bins[:-1]) / 2
    bar_width = bins[1] - bins[0]
    plt.bar(bin_centers, hist, width=bar_width, align='center')
    num_nan_values = group['Stat1'].isna().sum()
    if num_nan_values > 0:
        nan_bin_center = bin_centers.max() + bar_width
        plt.bar(nan_bin_center, num_nan_values, width=bar_width, align='center', color='gray')
    plt.title(f'Histogram for {year}')
    plt.xlabel('Stat1')
    plt.ylabel('Count')
    plt.show()

# # Loop through each group and plot a histogram
# for year, group in groups:
#     data = group['Stat1'].replace(-9999, np.nan).values
#     finite_data = data[np.isfinite(data)]
#     hist, bins = np.histogram(finite_data, bins=100)
#     bin_centers = (bins[1:] + bins[:-1]) / 2
#     plt.bar(bin_centers, hist, width=(bins[1] - bins[0]), align='center')
#     plt.title(f'Histogram for {year}')
#     plt.xlabel('Stat1')
#     plt.ylabel('Count')
#     plt.show()