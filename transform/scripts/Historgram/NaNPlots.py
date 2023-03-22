import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
from matplotlib.dates import date2num
import argparse
import os
from termcolor import colored
from tqdm import tqdm


# Create the parser
parser = argparse.ArgumentParser()
parser.add_argument('--dir', type=str, help='The directory where the file is located')
parser.add_argument('--filename', type=str, help='The filename to read')
parser.add_argument('--year', type=int, help='The year to plot')
parser.add_argument('--month', type=int, help='The month to plot')
args = parser.parse_args()

# Get the base filename
file_name = os.path.basename(args.filename)


# Build the full filepath from the directory and filename arguments
file_path = os.path.join(args.dir, args.filename)

# Read in the CSV file
df = pd.read_csv(file_path, sep='\t')

# Create a subdirectory called 'plots' within the directory specified by --dir
plot_dir = os.path.join(args.dir, 'plots')
if not os.path.exists(plot_dir):
    os.makedirs(plot_dir)
    print(f'Created directory: {colored(plot_dir, "green")}')

# Create a folder for the current file if it doesn't exist
file_folder = os.path.join(plot_dir, f'NaN_Plots{file_name[:-4]}')
if not os.path.exists(file_folder):
    os.makedirs(file_folder)
    print(f'Created directory: {colored(file_folder, "green")}')


# Extract the values from the Stat1 column
x = df['Stat1'].values

# Combine the datetime columns into a single datetime object
dates = [pd.Timestamp(int(row['YY']), int(row['MM']), int(row['DD']), int(row['HH']), int(row['MN'])) for i, row in df.iterrows()]

# Set the datetime index for the dataframe
df.index = dates

# Remove the YY, MM, DD, HH, and MN columns from the dataframe
df = df.drop(columns=['YY', 'MM', 'DD', 'HH', 'MN'])

# Print the number of NaN values per year
nan_count = df['Stat1'].isna().groupby(df.index.year).sum()
print(colored('Number of NaN values per year:', 'green'), colored(nan_count, 'red'))

# Create a boolean mask of NaN values
mask = df['Stat1'].isna()

# Convert the boolean mask to 0 and 1 values
plot_data = mask.astype(int)

# Group the data by year and month
groups = df.groupby([df.index.year, df.index.month])

# Get the year and month from the command line arguments
year = args.year
month = args.month

# If year and month are specified, plot data for the month of the year
if year is not None and month is not None:
    print(colored(f'plots data for {args.year}:{args.month}', 'blue'))
    # Filter the dataframe by the year and month specified in the command line arguments
    df_month = df[(df.index.year == year) & (df.index.month == month)]

    # Create a bar chart of the NaN values in the 'Stat1' column
    fig, ax = plt.subplots(figsize=(20, 8))
    plt.bar(df_month.index, plot_data.loc[df_month.index].values, width=0.001, color='red')

    # Set the title and axis labels
    plt.title(f'Occurrences of NaN values in {file_name} ({year}/{month:02d})')
    plt.xlabel('Date')
    plt.ylabel('NaN values')

    # Set the x-axis ticks and tick labels
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d'))

    # Save the plot as a file
    plot_filename = f'NaN_Plots_{file_name[:-4]}_{year}_{month:02d}.png'
    plot_filepath = os.path.join(file_folder, plot_filename)
    with tqdm(desc=f'Saving {plot_filename}', total=1) as pbar:
        fig.savefig(plot_filepath)
        pbar.update()

    # Display the chart
    #plt.show()

# If year is specified, plot monthly data for the year
elif year is not None:
    print(colored(f'The year{args.year} is plotted', 'blue'))
    # Filter the dataframe by the year specified in the command line argument
    df_year = df[df.index.year == year]

    # Create a bar chart of the NaN values in the 'Stat1' column
    fig, ax = plt.subplots(figsize=(20, 8))
    plt.bar(df_year.index, plot_data.loc[df_year.index].values, width=0.001, color='red')

    # Set the title and axis labels
    plt.title(f'Occurrences of NaN values in{file_name} ({year})')
    plt.xlabel('Month')
    plt.ylabel('NaN values')

    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    ax.tick_params(axis='x', labelsize=7)
    
    # Save the plot as a file
    plot_filename = f'NaN_Plots_{file_name[:-4]}_{year}.png'
    plot_filepath = os.path.join(file_folder, plot_filename)
    with tqdm(desc=f'Saving {plot_filename}', total=1) as pbar:
        fig.savefig(plot_filepath)
        pbar.update()

    # Display the chart
    #plt.show()

# If neither year nor month is specified, plot data for the entire dataframe
else:
    print(colored('The whole Dataframe is plotted', 'blue'))
    # Create a bar chart of the NaN values in the 'Stat1' column
    fig, ax = plt.subplots(figsize=(20, 8))
    plt.bar(df.index, plot_data.loc[df.index].values, width=0.01, color='red')

    # Set the title and axis labels
    plt.title(f'Occurrences of NaN values in {file_name}')
    plt.xlabel('Date')
    plt.ylabel('NaN values')

    # Set the x-axis ticks and tick labels
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.xticks(rotation=45)
    ax.tick_params(axis='x', labelsize=7)

    # Save the plot as a file
    plot_filename = f'NaN_Plots_{file_name[:-4]}.png'
    plot_filepath = os.path.join(file_folder, plot_filename)

    with tqdm(desc=f'Saving {plot_filename}', total=1) as pbar:
        fig.savefig(plot_filepath)
        pbar.update()  # update the progress bar with a value between 0 and 1

    # Display the chart
    #plt.show()
