import pandas as pd
import argparse
import os
from termcolor import colored
import matplotlib.pyplot as plt
import calendar
import matplotlib.dates as mdates
import numpy as np


# Create the parser
parser = argparse.ArgumentParser()
parser.add_argument('--dir', type=str, help='The directory where the file is located', default='C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/GitHubMasterSkripts/MasterSkript/transform/input/Abfluss')
parser.add_argument('--filename', type=str, help='The filename to read',  default='RQ30_data_20190625_20220818.csv')
parser.add_argument('--unit', type=str, help='The unit to plot', default="QStat")
parser.add_argument('--Station_name', type=str, help='Name of the Station', default="Jambach")
parser.add_argument('--hight', type=int, help='Hight of the Station', default="0")
parser.add_argument('--latitude', type=float, help='latitude of the Station', default="0.0")
parser.add_argument('--longitude', type=float, help='longitude of the Station', default="0.0")
args = parser.parse_args()

# Select the appropriate column based on the input unit
if args.unit == 'QStat':
    unit_col = 'QStat'
    unit_lable = "l/s"
elif args.unit == 'h':
    unit_col = 'h'
    unit_lable = "cm"
elif args.unit == 'v':
    unit_col = 'v'
    unit_lable = "m^3"
else:
    raise ValueError('Invalid unit specified')

# Get the base filename
file_name = os.path.basename(args.filename)

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

# Read in the CSV file
#df = pd.read_csv(file_path, sep=';')
df = pd.read_csv(file_path, sep=';', na_values=['nan', 'NaN'], encoding='utf-8' )

# Rename the columns
df.columns = ['date', 'h', 'v', 'QStat']
df['h'] = df['h'].astype(float)
df['v'] = df['v'].astype(float)
df['QStat'] = df['QStat'].astype(float)
df[unit_col] = df[unit_col].astype(float)


# Convert the Date column to a pandas datetime format
df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y %H:%M:%S')

################## create Wasim File --> Change Unit if needed! ################################################

def WaSiM_output(df, station_name, station_height, station_latitude, station_longitude, unit):
    output_file = os.path.join(file_folder, f'{file_name[:-4]}.txt')
    with open(output_file, 'w') as f:
        f.write(f'YY\tMM\tDD\tHH\tMN\t{station_name}\n')
        f.write(f'YY\tMM\tDD\tHH\tMN\t{station_height}\n')
        f.write(f'YY\tMM\tDD\tHH\tMN\t{station_latitude}\n')
        f.write(f'YY\tMM\tDD\tHH\tMN\t{station_longitude}\n')
        f.write(f'YY\tMM\tDD\tHH\tMN\t{unit}\n')
        for _, row in df.iterrows():
            if pd.isna(row[unit_col]):
                value = -9999
            else:
                value = round(row[unit_col],3) ### NOCHMAL ANPASSE auf minuten! Jetzt auf h nur umgerechnet
                
            f.write(f"{row['date'].year}\t{row['date'].month}\t{row['date'].day}\t{row['date'].hour}\t{row['date'].minute}\t{value}\n")
    print(f'WaSiM output saved to {colored(output_file, "green")}')


WaSiM_output(df, args.Station_name, args.hight, args.latitude, args.longitude, args.unit)
print("Wasim")
################################### Create NaN Outputfile of Discharge --> Change Unit if needed! #############

def NaN_output(df, station_name, station_height, station_latitude, station_longitude, unit):
    output_file = os.path.join(file_folder, f'NaN{unit}{file_name[:-4]}.csv')
    with open(output_file, 'w') as f:
        f.write(f"Date;{unit}\n")
        for _, row in df.iterrows():
            if pd.isna(row[unit_col]):
                value = "NaN"
            else:
                value = row[unit_col]
            f.write(f"{row['date']};{value}\n")
    print(f'NaN output saved to {colored(output_file, "green")}')

NaN_output(df, args.Station_name, args.hight, args.latitude, args.longitude, args.unit)
print("NaN Output")

   

