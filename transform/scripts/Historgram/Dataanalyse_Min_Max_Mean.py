import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.dates import date2num
import datetime
import argparse
import os
import numpy as np
import seaborn as sns
from tqdm import tqdm
from termcolor import colored


# Create the parser
parser = argparse.ArgumentParser()
parser.add_argument('--dir', type=str, help='The directory where the file is located', default='C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/GitHubMasterSkripts/MasterSkript/transform/output')
parser.add_argument('--filename', type=str, help='The filename to read',  default='ZAMG_RR_20131023T0000_20230402T2350NaN.csv')
parser.add_argument('--year', type=int, help='The year to plot', default= 2020)
parser.add_argument('--month', type=int, help='The month to plot', default= 10)
args = parser.parse_args()

# Get the base filename
file_name = os.path.basename(args.filename)


# Build the full filepath from the directory and filename arguments
file_path = os.path.join(args.dir, args.filename)


# Create a subdirectory called 'plots' within the directory specified by --dir
plot_dir = os.path.join(args.dir, 'plots')
if not os.path.exists(plot_dir):
    os.makedirs(plot_dir)
    print(f'Created directory: {colored(plot_dir, "green")}')

# Create a folder for the current file if it doesn't exist
file_folder = os.path.join(plot_dir, f'Dataanalys_plots_{file_name[:-4]}')
if not os.path.exists(file_folder):
    os.makedirs(file_folder)
    print(f'Created directory: {colored(file_folder, "green")}')

# Read in the CSV file
df = pd.read_csv(file_path, sep='\t')

# Extract the values from the Stat1 column
x = df['Stat1'].values


# Combine the datetime columns into a single datetime object
dates = [pd.Timestamp(int(row['YY']), int(row['MM']), int(row['DD']), int(row['HH']), int(row['MM.1'])) for i, row in df.iterrows()]


# Create a new column called 'date' by combining the individual date columns
df['date'] = pd.to_datetime(df[['YY', 'MM', 'DD', 'HH', 'MM.1']].rename(columns={'YY':'year', 'MM':'month', 'DD':'day', 'HH':'hour', 'MM.1':'minute' }))

# Set the datetime index for the dataframe
df.index = df['date']

# Remove the YY, MM, DD, HH, MM.1 and date columns from the dataframe
df = df.drop(columns=['YY', 'MM', 'DD', 'HH', 'MM.1'])

# If --year is specified, filter the dataframe to only include rows with the specified year
if args.year:
    df = df[df['date'].dt.year == args.year]

# If --month is specified, filter the dataframe to only include rows with the specified month
if args.month:
    df = df[df['date'].dt.month == args.month]

##### Data analyse ######

# 1. Max/ Min  Values with Date & Time each month
# 2. Mean Value each month 
# 3. compare months of all years --> Min-Max-Mean 

# # Filter out NaN values
# df = df[pd.notnull(df['Stat1'])]
# print(df)

# Group the data by month
monthly_data = df.groupby(pd.Grouper(key='date', freq='M'))
# monthly_data = df.groupby(df['date'].dt.to_period('M'))
### orig
# # Group the data by month. Each group contains all values of one month
# monthly_data = df.groupby(pd.Grouper(key='date', freq='M'))
#####
# Filter the dataframe to only include rows with the specified year and month
df_filtered = df[(df['date'].dt.year == args.year) & (df['date'].dt.month == args.month)]
# Filter the dataframe to only include rows with the specified year and month
df_filtered_year = df[(df['date'].dt.year == args.year)]

# Group the data by day within the month and calculate the mean, including NaN values --> change skipna=True)) to see the days with NaN Values!
daily_data = df_filtered.groupby(df_filtered['date'].dt.day)['Stat1'].apply(lambda x: x.mean(skipna=False))
#print("Daily data:\n", daily_data)


###################################Works perfekt for each month with dayly data plus max, min & mean ###################################################
# Create a new figure for each month
for month, data in monthly_data:
    
    # Group the data by day within the month
    daily_data = data.groupby(data['date'].dt.to_period('D'))
    
    # Calculate the maximum, minimum, and mean values for the month
    monthly_max = data['Stat1'].max()
    monthly_min = data['Stat1'].min()
    monthly_mean = data['Stat1'].mean()
    
    # Calculate the daily averages for the month
    daily_means = daily_data['Stat1'].mean()

    # Convert the PeriodIndex to a DatetimeIndex
    daily_means.index = daily_means.index.to_timestamp()
    
    # # Create a new figure with a larger size
    fig, ax = plt.subplots(figsize=(20, 12))
    
    # # # Plot the daily data for the month
    ax.scatter(daily_means.index, daily_means.values, color='black', marker='.')

    # Plot the monthly maximum values
    ax.axhline(monthly_max, linestyle='--', color='red', label='Max')
    ax.axhline(monthly_min, linestyle='--', color='blue', label='Min')
    # Add a horizontal line for the mean value
    ax.axhline(monthly_mean, linestyle='-', color='green', label='Mean')
    
    # Set the x-axis label
    ax.set_xlabel('Date')
    
    # Set the y-axis label
    ax.set_ylabel('Value')
    
    # Set the title
    ax.set_title(f'Monthly Data for {month}')
    
    # Add a legend
    ax.legend()

    # Create the plot filename with the base filename, year, and .png extension
    plot_filename = f"{file_name}{args.month}{args.year}.png"
    # Construct the full path to the plot file
    plot_path = os.path.join(file_folder, plot_filename)

    # Save the plot
    with tqdm(desc=colored(f'Saving {args.year} {plot_filename}', 'yellow'), total=1) as pbar:
        plt.savefig(plot_path)
        pbar.update()
  
    # Show the plot
    plt.show()
# ###################################################################################################################################

def yearly_plot(file_path, year, filename):
    # Read in the CSV file
    df = pd.read_csv(file_path, sep='\t')

    # Combine the datetime columns into a single datetime object
    dates = [pd.Timestamp(int(row['YY']), int(row['MM']), int(row['DD']), int(row['HH']), int(row['MM.1'])) for i, row in df.iterrows()]

    # Create a new column called 'date' by combining the individual date columns
    df['date'] = pd.to_datetime(df[['YY', 'MM', 'DD', 'HH', 'MM.1']].rename(columns={'YY':'year', 'MM':'month', 'DD':'day', 'HH':'hour', 'MM.1':'minute' }))

    # Set the datetime index for the dataframe
    df.index = df['date']

    # Remove the YY, MM, DD, HH, MM.1 and date columns from the dataframe
    df = df.drop(columns=['YY', 'MM', 'DD', 'HH', 'MM.1'])

    # Filter the dataframe to only include rows with the specified year
    df = df[df['date'].dt.year == year]

    # Group the data by day and calculate the mean of Stat1 for each day
    daily_data = df.groupby(pd.Grouper(key='date', freq='D')).mean()

    fig, ax = plt.subplots(figsize=(20, 5))
    # Create a line plot of the daily average of Stat1
    plt.plot(daily_data.index, daily_data['Stat1'])
    plt.xlabel('Date')
    plt.ylabel('Daily Average of Precipitation mm')                        # ANPASSEN!
    plt.title('Yearly Plot of Daily Precipitation')
    
    # Get the base filename without the extension
    file_name, extension = os.path.splitext(args.filename)

    # Create the plot filename with the base filename, year, and .png extension
    plot_filename = f"{file_name}{year}.png"

    # Construct the full path to the plot file
    plot_path = os.path.join(file_folder, plot_filename)

    # Save the plot
    with tqdm(desc=colored(f'Saving {year} {plot_filename}', 'yellow'), total=1) as pbar:
        plt.savefig(plot_path)
        pbar.update()

# Show the plot
plt.show()

yearly_plot(file_path, args.year, args.filename)



def plot_all(file_path, filename):
    # Read in the CSV file
    df = pd.read_csv(file_path, sep='\t')

    # Combine the datetime columns into a single datetime object
    dates = [pd.Timestamp(int(row['YY']), int(row['MM']), int(row['DD']), int(row['HH']), int(row['MM.1'])) for i, row in df.iterrows()]

    # Create a new column called 'date' by combining the individual date columns
    df['date'] = pd.to_datetime(df[['YY', 'MM', 'DD', 'HH', 'MM.1']].rename(columns={'YY':'year', 'MM':'month', 'DD':'day', 'HH':'hour', 'MM.1':'minute' }))

    # Set the datetime index for the dataframe
    df.index = df['date']

    # Remove the YY, MM, DD, HH, MM.1 and date columns from the dataframe
    df = df.drop(columns=['YY', 'MM', 'DD', 'HH', 'MM.1'])

    # Group the data by day and calculate the mean of Stat1 for each day
    daily_data = df.groupby(pd.Grouper(key='date', freq='D')).mean()

    fig, ax = plt.subplots(figsize=(20, 5))
    # Create a line plot of the daily average of Stat1 for all years
    plt.plot(daily_data.index, daily_data['Stat1'])
    plt.xlabel('Date')
    plt.ylabel('Daily Average of Precipitation mm')
    plt.title('Plot of Daily Average of precipitation')

    # Get the base filename without the extension
    file_name, extension = os.path.splitext(filename)

    # Create the plot filename with the base filename and .png extension
    plot_filename = f"{file_name}.png"

    # Construct the full path to the plot file
    plot_path = os.path.join(file_folder, plot_filename)

    # Save the plot
    with tqdm(desc=colored(f'Saving {plot_filename}', 'yellow'), total=1) as pbar:
        plt.savefig(plot_path)
        pbar.update()

    # Show the plot
    plt.show()

plot_all(file_path, args.filename)