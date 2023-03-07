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
parser.add_argument('--filename', type=str, help='The filename to read',  default='AirtempTest2102.csv')
parser.add_argument('--year', type=int, help='The year to plot', default= 2014)
parser.add_argument('--month', type=int, help='The month to plot', default= 2)
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

# If --year is specified, filter the dataframe to only include rows with the specified year
if args.month:
    df = df[df['date'].dt.month == args.month]

# Group the data by year
groups = df.groupby(df['date'].dt.year)


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

# Calculate the daily averages for each month
daily_data = monthly_data['Stat1'].mean().resample('D').mean()

## 1.
                    
                    # # Calculate the maximum, minimum, and mean values for each month (with date)
                    # monthly_max = monthly_data['Stat1'].max()
                    # #print(monthly_max, "Monthly Maximum Value")
                    # monthly_min = monthly_data['Stat1'].min()
                    # #print(monthly_min, "Monthly Minimum Value")
                    # monthly_mean = monthly_data['Stat1'].mean()
                    # #print(monthly_mean, "Monthly Mean Value")


# Function that creats a new figure for each month with Min, Max & Mean Values of the month as a line and Mean daily Data
##### If NaN Values are in the df it will not show that day! --> Maybe solve that later  ######## 
def data_monthly(file_name, year, month, daily_data, monthly_data):
        
    for month, data in monthly_data:
        # Only plot the month that matches the specified month argument
        if month.month != args.month:
            continue
        
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

        # Create a boolean mask indicating which values are NaN
        nan_mask = daily_means.isna()
        
        # Create a new figure for the month
        fig, ax = plt.subplots(figsize=(10, 5))
        
        # # Plot the daily data for the month ####
        # ax.plot(daily_means.index.day, daily_means.values, label='Daily')
        ######

         # Plot the daily data for the month, coloring missing values differently
        sc = ax.scatter(daily_means.index.day, daily_means.values, c=nan_mask, cmap='coolwarm', label='Daily mean')
        ######################

        
    #     Plot the monthly maximum values
        ax.axhline(monthly_max, linestyle='--', color='red', label='Max')
        ax.text(0.95, monthly_max, f'{monthly_max:.2f}', ha='center', va='baseline', color='red')
        ax.axhline(monthly_min, linestyle='--', color='blue', label='Min')
        ax.text(0.95, monthly_min, f'{monthly_min:.2f}', ha='center', va='baseline', color='blue')
        # Add a horizontal line for the mean value
        ax.axhline(monthly_mean, linestyle='-', color='green', label='Mean')
        ax.text(0.95, monthly_mean, f'{monthly_mean:.2f}', ha='center', va='baseline', color='green')    
        
        # Set the x-axis & y-axis label
        ax.set_xlabel('Day')
        ax.set_ylabel('Value')
        # Set the title & Legend 
        ax.set_title(f'Monthly Data for {month.strftime("%B %Y")}')
        ax.legend()

        # Add value annotations to each point on the plot
        for i, (x, y) in enumerate(zip(daily_means.index.day, daily_means.values)):
            if nan_mask[i]:
                # If the value is NaN, use a different color and add a "NaN" label
                color = 'gray'
                label = 'NaN'
            else:
                # Otherwise, use the default color and add the value as a label
                color = sc.cmap(sc.norm(y))
                label = f'{y:.2f}'
            ax.annotate(label, xy=(x, y), xytext=(x+0.2, y), color=color, fontsize=8)

        # Save the plot with a unique name based on the month and year
        plot_name = f'{file_name}_{month.strftime("%Y-%m")}.png'
        #  plot_name = f'DataanalyseMinMaxMean{file_name}{year}.png'
        plot_path = os.path.join(file_folder, plot_name)

        with tqdm(desc=colored(f'Saving {plot_name}', 'yellow'), total=1) as pbar:
            plt.savefig(plot_path)
            pbar.update()

        # Show the plot
        plt.show()

data_monthly(file_name, args.year, args.month, daily_data, monthly_data)


####################################Works perfekt for each month with dayly data plus max, min & mean ###################################################
# # Create a new figure for each month
# for month, data in monthly_data:
    
#     # Group the data by day within the month
#     daily_data = data.groupby(data['date'].dt.to_period('D'))
    
#     # Calculate the maximum, minimum, and mean values for the month
#     monthly_max = data['Stat1'].max()
#     monthly_min = data['Stat1'].min()
#     monthly_mean = data['Stat1'].mean()
    
#     # Calculate the daily averages for the month
#     daily_means = daily_data['Stat1'].mean()

#     # Convert the PeriodIndex to a DatetimeIndex
#     daily_means.index = daily_means.index.to_timestamp()
    
#     # # Create a new figure with a larger size
#     fig, ax = plt.subplots(figsize=(20, 12))
    
#     # # # Plot the daily data for the month
#     ax.scatter(daily_means.index, daily_means.values, color='black', marker='.')

#     # Plot the monthly maximum values
#     ax.axhline(monthly_max, linestyle='--', color='red', label='Max')
#     ax.axhline(monthly_min, linestyle='--', color='blue', label='Min')
#     # Add a horizontal line for the mean value
#     ax.axhline(monthly_mean, linestyle='-', color='green', label='Mean')
    
#     # Set the x-axis label
#     ax.set_xlabel('Date')
    
#     # Set the y-axis label
#     ax.set_ylabel('Value')
    
#     # Set the title
#     ax.set_title(f'Monthly Data for {month}')
    
#     # Add a legend
#     ax.legend()
    
#     # Show the plot
#     plt.show()
####################################################################################################################################

