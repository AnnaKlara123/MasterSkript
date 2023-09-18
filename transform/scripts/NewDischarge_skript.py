import pandas as pd
import argparse
import os
import numpy as np

# Create the parser
parser = argparse.ArgumentParser()
parser.add_argument('--dir', type=str, help='The directory where the files are located', default='C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/GitHubMasterSkripts/MasterSkript/transform/input/Abfluss')
parser.add_argument('--filename', type=str, help='The filename to read',  default='RQ30_data_20190625_20220818.csv')
parser.add_argument('--unit', type=str, help='The unit to plot', default="QStat")
parser.add_argument('--Station_name', type=str, help='Name of the Station', default="Jambach")
parser.add_argument('--hight', type=int, help='Height of the Station', default=0)
parser.add_argument('--latitude', type=float, help='Latitude of the Station', default=0.0)
parser.add_argument('--longitude', type=float, help='Longitude of the Station', default=0.0)
parser.add_argument('--startdate', type=str, help='The startdate that the df should start', default='2019-6-26')
parser.add_argument('--enddate', type=str, help='The enddate of the dataset', default='2022-8-19')
args = parser.parse_args()

# Get the base filename
file_name = os.path.basename(args.filename)

# Build the full filepath from the directory and filename arguments
file_path = os.path.join(args.dir, args.filename)

# Read in the CSV file
df = pd.read_csv(file_path, sep=';', na_values=['nan', 'NaN'], encoding='utf-8')

# Rename the columns
df.columns = ['date', 'h', 'v', 'QStat']
df['h'] = df['h'].astype(float)
df['v'] = df['v'].astype(float)
df['QStat'] = df['QStat'].astype(float)
unit_col = args.unit
df[unit_col] = df[unit_col].astype(float)

# Convert the Date column to a pandas datetime format
df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y %H:%M:%S')

# Define the desired start / end date
start_date = pd.to_datetime(args.startdate)
end_date = pd.to_datetime(args.enddate)

# Filter the DataFrame based on start and end dates
df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]

# Create a subdirectory for output files (same as input directory)
output_dir = args.dir

# Function to create Wasim File
def WaSiM_output(df, station_name, station_height, station_latitude, station_longitude, unit, start_date, end_date):
    output_file = os.path.join(output_dir, f'{file_name[:-4]}.txt')
    with open(output_file, 'w') as f:
        f.write(f'YY\tMM\tDD\tHH\tMN\t{station_name}\n')
        f.write(f'YY\tMM\tDD\tHH\tMN\t{station_height}\n')
        f.write(f'YY\tMM\tDD\tHH\tMN\t{station_latitude}\n')
        f.write(f'YY\tMM\tDD\tHH\tMN\t{station_longitude}\n')
        f.write(f'YY\tMM\tDD\tHH\tMN\t{unit}\n')
        
        # Create a date range with 10-minute intervals
        date_range = pd.date_range(start=start_date, end=end_date, freq='10T')
        
        # Iterate over the date range and write values from the DataFrame
        for timestamp in date_range:
            # Extract data for the 10-minute interval
            interval_data = df[(df['date'] >= timestamp) & (df['date'] < timestamp + pd.Timedelta(minutes=10))]
            
            if interval_data.empty:
                value = -9999  # Fill gaps with -9999 (NaN value)
            else:
                value = round(interval_data[unit_col].mean(), 3)  # Calculate mean for the interval
            f.write(f"{timestamp.year}\t{timestamp.month}\t{timestamp.day}\t{timestamp.hour}\t{timestamp.minute}\t{value}\n")
    print(f'WaSiM output saved to {output_file}')

# Call the function to create Wasim File
WaSiM_output(df, args.Station_name, args.hight, args.latitude, args.longitude, args.unit, start_date, end_date)
print("Wasim")

