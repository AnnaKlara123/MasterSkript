import matplotlib.pyplot as plt
import pandas as pd
import argparse
import os
import numpy as np
from tqdm import tqdm
from termcolor import colored


# Create the parser
parser = argparse.ArgumentParser()
parser.add_argument('--dir', type=str, help='The directory where the file is located', default= 'C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/Meteo_Discharge/AnalyseTest_0610/Discharge')
parser.add_argument('--filename', type=str, help='The filename to read', default= 'DischargeQStat.csv')
parser.add_argument('--year', type=int, help='The year to plot', default= '2022')
parser.add_argument('--percentage', type=float, help='Percentage for highest values',default="5.0")
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
file_folder = os.path.join(plot_dir, f'Histogramm_{file_name[:-4]}')
if not os.path.exists(file_folder):
    os.makedirs(file_folder)
    print(f'Created directory: {colored(file_folder, "green")}')

# Read in the CSV file
df = pd.read_csv(file_path, sep='\t')

# Extract the values from the Stat1 column
x = df['Stat1'].values

# Combine the datetime columns into a single datetime object
dates = [pd.Timestamp(int(row['YY']), int(row['MM']), int(row['DD']), int(row['HH']), int(row['MN'])) for i, row in df.iterrows()]


# Create a new column called 'date' by combining the individual date columns
df['date'] = pd.to_datetime(df[['YY', 'MM', 'DD', 'HH', 'MN']].rename(columns={'YY':'year', 'MM':'month', 'DD':'day', 'HH':'hour', 'MN':'minute' }))

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

    # Get the highest and lowest values, filtering out NaNs
    highest_values = sorted(df['Stat1'].dropna())[-5:]
    lowest_values = sorted(df['Stat1'].dropna())[:5]

    # Create a string with the highest and lowest values and their corresponding dates
    highest_values_str = ', '.join([f'{value:.2f} ({date})' for value, date in zip(sorted(df['Stat1'])[-5:], highest_dates)])
    lowest_values_str = ', '.join([f'{value:.2f} ({date})' for value, date in zip(sorted(df['Stat1'])[:5], lowest_dates)])
    # Return the strings for the highest and lowest values
    return highest_values_str, lowest_values_str, highest_values, lowest_values

def most_common_values(df):
    # Get the counts of each value in the 'Stat1' column
    value_counts = df['Stat1'].value_counts()

    # Get the 10 most common values
    most_common_values = value_counts.iloc[:5]

    # Convert the index (the 'Stat1' values) to strings for display purposes
    most_common_values.index = most_common_values.index.astype(str)

    # Combine the values and their counts into a single string for display purposes
    most_common_values_str = ', '.join([f'{value} ({count})' for value, count in most_common_values.items()])

    # Return the string of the 10 most common values and their counts
    return most_common_values_str

# Call the histogram_plotter function
most_common_values(df)

def histogram_plotter(df, plot_dir, file_name, year, highest_values_str, lowest_values_str, most_common_values_str):
    data = df['Stat1'].dropna().replace(-9999, np.nan).values
    finite_data = data[np.isfinite(data)]
    hist, bins = np.histogram(finite_data, bins=15)
    bin_centers = (bins[1:] + bins[:-1]) / 2
    bar_width = bins[1] - bins[0]
    plt.bar(bin_centers, hist, width=bar_width, align='center')
    num_nan_values = df['Stat1'].isna().sum()
    #if num_nan_values > 0:
    #    nan_bin_center = bin_centers.max() + bar_width
    #    plt.bar(nan_bin_center, num_nan_values, width=bar_width, align='center', color='gray')
    #    plt.text(nan_bin_center, num_nan_values, f'{num_nan_values}', ha='center', va='bottom')
    #plt.title(f'Histogram for {file_name[:-4]}')#
    #plt.title(f'Histogram for {year}')
    plt.title(f'Histogram')
    plt.xlabel('Discharge m3/s')
   # plt.xlabel('Temperature in °C')
    plt.ylabel('Count')

    # Set y-axis to be logarithmic
    #plt.yscale('log')
    
    # Set the y-axis and x-axis limits
    plt.ylim(0, 8000)
    plt.xlim(0, 16)

    # Print to Plot 
    plt.text(0.02, 0.85, f'Highest values: {highest_values}', transform=plt.gca().transAxes, fontsize=8, verticalalignment='top')
    plt.text(0.02, 0.75, f'Lowest values: {lowest_values}', transform=plt.gca().transAxes, fontsize=8, verticalalignment='top')
   # plt.text(0.02, 0.65, f'Most common values: {most_common_values_str}', transform=plt.gca().transAxes, fontsize=8, verticalalignment='top')

    file_folder = os.path.join(plot_dir, f'Histogramm_{file_name[:-4]}')
    if not os.path.exists(file_folder):
        os.makedirs(file_folder)

    plot_name = f'Histogram_{file_name[:-4]}{year}.png'
    plot_path = os.path.join(file_folder, plot_name)

    with tqdm(desc=f'Saving {plot_name}', total=1) as pbar:
        plt.savefig(plot_path)
        pbar.update()
    
    plt.show()

highest_values_str, lowest_values_str, highest_values, lowest_values = high_low_values(df)
most_common_values_str = most_common_values(df)
histogram_plotter(df, plot_dir, file_name, args.year, highest_values_str, lowest_values_str, most_common_values_str)

### ## Print most common values & Max & min to console 
highest_values_str, lowest_values_str, highest_values, lowest_values = high_low_values(df)
print(colored(f'Highest values of Stat1 are {highest_values_str}', 'red'))
print(colored(f'Lowest values of Stat1 are {lowest_values_str}', 'blue'))
most_common_values_str = most_common_values(df)
print(colored(f'Most common values of Stat1 are {most_common_values_str}', 'green'))




# ############# Berechnung % Anteile ###########################
# def find_highest_values_and_boundary(df, percentage):
#     if percentage is None or percentage <= 0 or percentage >= 100:
#         return  # Exit the function if percentage is not provided or is invalid
#     # Group data by day and calculate daily sum
#     daily_sums = df['Stat1'].resample('D').max()
    
#     # Extract the values from the daily sums
#     data = daily_sums.dropna().values
#     finite_data = data[np.isfinite(data)]
#     sorted_data = np.sort(finite_data)
    
#     # Calculate the boundary (5th percentile)
#     boundary = np.percentile(sorted_data, 100 - percentage)
    
#     # Filter values greater than the boundaryndicator 
#     highest_values = sorted_data[sorted_data >= boundary]
    
#     # Count the number of values in the list
#     num_values = len(highest_values)
#     print(f"Number of values: {num_values}")
    
#     return highest_values, boundary

# # Call this function to find the 5% highest values and their boundary
# highest_values, boundary = find_highest_values_and_boundary(df, args.percentage)

# print(f"Boundary for {args.percentage}% highest values: {boundary}")
# print(f"{args.percentage}% Highest Values: {highest_values}")