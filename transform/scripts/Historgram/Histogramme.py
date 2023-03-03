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
parser.add_argument('--dir', type=str, help='The directory where the file is located')
parser.add_argument('--filename', type=str, help='The filename to read')
parser.add_argument('--year', type=int, help='The year to plot')
args = parser.parse_args()

# Get the base filename
file_name = os.path.basename(args.filename)

# Build the full filepath from the directory and filename arguments
file_path = os.path.join(args.dir, args.filename)

# Create a subdirectory called 'plots' within the directory specified by --dir
plot_dir = os.path.join(args.dir, 'plots')
if not os.path.exists(plot_dir):
    os.makedirs(plot_dir)
    print(colored(f'Created directory:',f'{plot_dir}', 'red'))

# Create a folder for the current file if it doesn't exist
file_folder = os.path.join(plot_dir, f'Histogramm_{file_name[:-4]}')
if not os.path.exists(file_folder):
    os.makedirs(file_folder)
    print(colored(f'Created directory: {file_folder}', 'green'))

# Read in the CSV file
df = pd.read_csv(file_path, sep='\t')

# Get the base filename
file_name = os.path.basename(args.filename)
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

def high_low_values(df):
    # Find the indices of the highest and lowest values in the dataframe
    highest_indices = sorted(range(len(df)), key=lambda i: df.iloc[i]['Stat1'])[-5:]
    lowest_indices = sorted(range(len(df)), key=lambda i: df.iloc[i]['Stat1'])[:5]

    # Get the corresponding dates for the highest and lowest values
    highest_dates = [df.iloc[i]['date'] for i in highest_indices]
    lowest_dates = [df.iloc[i]['date'] for i in lowest_indices]

    # Get the highest and lowest values
    highest_values = sorted(df['Stat1'])[-5:]
    lowest_values = sorted(df['Stat1'])[:5]

    # Create a string with the highest and lowest values and their corresponding dates
    highest_values_str = ', '.join([f'{value:.2f} ({date})' for value, date in zip(sorted(df['Stat1'])[-5:], highest_dates)])
    lowest_values_str = ', '.join([f'{value:.2f} ({date})' for value, date in zip(sorted(df['Stat1'])[:5], lowest_dates)])
    # Return the strings for the highest and lowest values
    return highest_values_str, lowest_values_str, highest_values, lowest_values


def histogram_plotter(df, plot_dir, file_name, year):
    data = df['Stat1'].replace(-9999, np.nan).values
    finite_data = data[np.isfinite(data)]
    hist, bins = np.histogram(finite_data, bins=100)
    bin_centers = (bins[1:] + bins[:-1]) / 2
    bar_width = bins[1] - bins[0]
    plt.bar(bin_centers, hist, width=bar_width, align='center')
    num_nan_values = df['Stat1'].isna().sum()
    if num_nan_values > 0:
        nan_bin_center = bin_centers.max() + bar_width
        plt.bar(nan_bin_center, num_nan_values, width=bar_width, align='center', color='gray')
        plt.text(nan_bin_center, num_nan_values, f'{num_nan_values}', ha='center', va='bottom')
    plt.title(f'Histogram for {year}')
    plt.xlabel('Stat1')
    plt.ylabel('Count')

    ### This could be smarter somewhere else! #####
    highest_values_str, lowest_values_str, highest_values, lowest_values = high_low_values(df)
    print(colored(f'Highest values of Stat1 are {highest_values}', 'red'))
    print(colored(f'Lowest values of Stat1 are {lowest_values}', 'blue'))
    
    plt.text(0.02, 0.85, f'Highest values: {highest_values}', transform=plt.gca().transAxes, fontsize=10, verticalalignment='top')
    plt.text(0.02, 0.75, f'Lowest values: {lowest_values}', transform=plt.gca().transAxes, fontsize=10, verticalalignment='top')

    file_folder = os.path.join(plot_dir, f'Histogramm_{file_name[:-4]}')
    if not os.path.exists(file_folder):
        os.makedirs(file_folder)

    plot_name = f'Histogram_{file_name}{year}.png'
    plot_path = os.path.join(file_folder, plot_name)

    with tqdm(desc=f'Saving {plot_name}', total=1) as pbar:
        plt.savefig(plot_path)
        pbar.update()
    
    plt.show()

# Call the histogram_plotter function
histogram_plotter(df, plot_dir, file_name, args.year)