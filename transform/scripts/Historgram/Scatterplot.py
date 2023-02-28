import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.dates import date2num
from matplotlib.dates import YearLocator, MonthLocator, DateFormatter
import matplotlib.dates as mdates
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
#header = pd.read_csv('C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/GitHubMasterSkripts/MasterSkript/transform/output/Airtemp_NaN.csv', nrows=1).columns

# Read in the CSV file ----> CHANGE NAME!
df = pd.read_csv('C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/GitHubMasterSkripts/MasterSkript/transform/output/Precipitation_NaN_test.csv', sep='\t')
# Get file_name ---> NEEDS to be CHANGED
file_name = os.path.basename('C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/GitHubMasterSkripts/MasterSkript/transform/output/Precipitation_NaN_test.csv')
plot_dir = 'C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/GitHubMasterSkripts/MasterSkript/transform/scripts/Historgram/plots_hardcoded'
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

# If --year is specified, filter the dataframe to only include rows with the specified year
if args.year:
    df = df[df['date'].dt.year == args.year]

# Group the data by year
groups = df.groupby(df['date'].dt.year)

# Calculate the 95th and 99th percentile of the data for each year and month
percentiles = df.groupby([df['date'].dt.year, df['date'].dt.month, df['date'].dt.day])['Stat1'].quantile([0.99, 0.999])
print(percentiles, 'percentiles')

# Create a new column to identify extreme values
df['is_extreme'] = df.apply(lambda row: row['Stat1'] > percentiles.loc[(row['date'].year, row['date'].month,row['date'].day, 0.999)], axis=1)
# compares the value in the 'Stat1' column for each row of the dataframe with the 99.9th percentile value for the corresponding year and month.


# Filter the DataFrame to only include extreme values
extreme_df = df[df['is_extreme']]
# print(extreme_df, 'exttrema')

# # Print the threshold quantiles for each month
# for month in range(1, 13):
#     quantiles = percentiles.loc[(slice(None), month), :]
#     print(f"Month {month}: 99th percentile = {quantiles.loc[:, 0.99].values[0]}, 99.9th percentile = {quantiles.loc[:, 0.999].values[0]}")


# Create a scatter plot of the extreme values for each year
groups = extreme_df.groupby(extreme_df['date'].dt.year)
for year, group in groups:
    fig, ax = plt.subplots(figsize=(15, 5))
    plt.scatter(group['date'], group['Stat1'])
    plt.title(f'Extreme Values for {year}')
    plt.xlabel('Date')
    plt.ylabel('Stat1')
    plt.show()
















# # Create a scatter plot of the extreme values for each year
# groups = extreme_df.groupby(extreme_df['date'].dt.year)
# for year, group in groups:
#     fig, ax = plt.subplots(figsize=(15, 5))
#     plt.scatter(group['date'], group['Stat1'])

    
#     # Plot the 0.99 and 0.999 percentiles for each year and month
#     monthly_percentiles = percentiles.loc[year]
#     print(monthly_percentiles,'monthpercil')
#     for month in range(1, 13):
#         percentile_99 = df.loc[(2013, 1), 0.99]   # select row with year=2013, month=1, quantile=0.99
#        # percentile_999 = percentiles.loc[(year, month, 0.999)]
#         plt.axhline(percentile_99, color='orange', linestyle='--')
#        # plt.axhline(percentile_999, color='red', linestyle='--')
        
#     plt.title(f'Extreme Values for {year}')
#     plt.xlabel('Date')
#     plt.ylabel('Stat1')
#     plt.ylim(-50, 150)  # Set the y-axis limits to better display the percentiles
    
#     plt.show()

# # # Set tick positions and labels for x-axis
# # ax.xaxis.set_major_locator(YearLocator())
# # ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))

# # # Add minor ticks to show the month
# # ax.xaxis.set_minor_locator(MonthLocator())
# # ax.xaxis.set_minor_formatter(DateFormatter('%m'))


#     # # Create a folder for the current file if it doesn't exist
#     # file_folder = os.path.join(plot_dir, f'Scatterplot{file_name[:-4]}')
#     # if not os.path.exists(file_folder):
#     #     os.makedirs(file_folder)

#     # # Save the plot in the folder for the current file
#     # plot_name = f'Histogram_{file_name}{year}.png'
#     # plot_path = os.path.join(file_folder, plot_name)
#     # plt.savefig(plot_path)