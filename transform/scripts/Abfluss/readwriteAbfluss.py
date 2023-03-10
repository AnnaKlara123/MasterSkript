import pandas as pd
import argparse
import os
from termcolor import colored

# Create the parser
parser = argparse.ArgumentParser()
parser.add_argument('--dir', type=str, help='The directory where the file is located', default='C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/GitHubMasterSkripts/MasterSkript/transform/input/Abfluss')
parser.add_argument('--filename', type=str, help='The filename to read',  default='RQ30_data_20190625_20220818.csv')
parser.add_argument('--year', type=int, help='The year to plot', default= 2013)
parser.add_argument('--month', type=int, help='The month to plot', default= 10)
args = parser.parse_args()


# Get the base filename
file_name = os.path.basename(args.filename)

# Build the full filepath from the directory and filename arguments
file_path = os.path.join(args.dir, args.filename)

# Build the full filepath from the directory and filename arguments
file_path = os.path.join(args.dir, args.filename)

def prepare_output(file_name, plot_dir):
    # Create a subdirectory called 'Dischargeanalyse' within the directory specified by --dir
    plot_dir = os.path.join(args.dir, 'Dischargeanalyse')
    if not os.path.exists(plot_dir):
        os.makedirs(plot_dir)
        print(f'Created directory: {colored(plot_dir, "green")}')

    # Create a folder for the current file if it doesn't exist
    file_folder = os.path.join(plot_dir, f'Discharge{file_name[:-4]}')
    if not os.path.exists(file_folder):
        os.makedirs(file_folder)
        print(f'Created directory: {colored(file_folder, "green")}')
    
    return file_folder

# Call the function and assign the result to a variable
file_folder = prepare_output(file_name, args.dir)

print(file_folder)

# Read in the CSV file
df = pd.read_csv(file_path, sep=';')

# Rename the columns
df.columns = ['date', 'h', 'v', 'QStat']

# Convert the Date column to a pandas datetime format
df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y %H:%M:%S')

# Set the Date column as the index
df.set_index('date', inplace=True)

# Access the data for a specific timestamp (e.g. 25-06-2019 11:00:00)
data_for_timestamp = df.loc['2019-06-25 11:00:00']

print(df)

# If --year is specified, filter the dataframe to only include rows with the specified year
# Group the data by year / month

group_year = df.groupby(df['date'].dt.year)
groups_month = df.groupby(df['date'].dt.month)
