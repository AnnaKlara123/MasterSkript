import pandas as pd
import argparse
import os
from termcolor import colored
import matplotlib.pyplot as plt
import calendar
import matplotlib.dates as mdates


# Create the parser
parser = argparse.ArgumentParser()
parser.add_argument('--dir', type=str, help='The directory where the file is located', default='C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/GitHubMasterSkripts/MasterSkript/transform/input/Abfluss')
parser.add_argument('--filename', type=str, help='The filename to read',  default='RQ30_data_20190625_20220818.csv')
parser.add_argument('--unit', type=str, help='The unit to plot', default="QStat")
parser.add_argument('--year', type=int, help='The year to plot', default= 2020)
parser.add_argument('--month', type=int, help='The month to plot', default= 7)
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
df = pd.read_csv(file_path, sep=';')
# Rename the columns
df.columns = ['date', 'h', 'v', 'QStat']
df['h'] = df['h'].astype(float)
df['v'] = df['v'].astype(float)
df['QStat'] = df['QStat'].astype(float)
df[unit_col] = df[unit_col].astype(float)


# Convert the Date column to a pandas datetime format
df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y %H:%M:%S')

################## create Wasim File ################################################

def WaSiM_output(df, station_name, station_height, station_latitude, station_longitude):
    output_file = os.path.join(file_folder, f'{file_name[:-4]}.txt')
    with open(output_file, 'w') as f:
        f.write(f'YY\tMM\tDD\tHH\tMN\t{station_name}\n')
        f.write(f'YY\tMM\tDD\tHH\tMN\t{station_height}\n')
        f.write(f'YY\tMM\tDD\tHH\tMN\t{station_latitude}\n')
        f.write(f'YY\tMM\tDD\tHH\tMN\t{station_longitude}\n')
        f.write(f'YY\tMM\tDD\tHH\tMN\t{station_name}\n')
        for _, row in df.iterrows():
            if pd.isna(row[unit_col]):
                value = -9999
            else:
                value = row[unit_col]
            f.write(f"{row['date'].year}\t{row['date'].month}\t{row['date'].day}\t{row['date'].hour}\t{row['date'].minute}\t{value}\n")
    print(f'WaSiM output saved to {colored(output_file, "green")}')


# WaSiM_output(df, args.Station_name, args.hight, args.latitude, args.longitude)
print("Wasim")

# Extract the values from the Stat1 column
x = df[unit_col].values

# Set the datetime index for the dataframe
df = df.set_index('date')

# # Create a boolean mask of NaN values
# mask = df[unit_col].isna()

# # Convert the boolean mask to 0 and 1 values
# plot_data = mask.astype(int)

# # Group the data by year and month
# groups = df.groupby([df.index.year, df.index.month])

# # Loop through each group and create a bar chart
# for (year, month), group in groups:
#     if (args.year is None or year == args.year) and (args.month is None or month == args.month):
#         # Create a bar chart of the NaN values in the Value column
#         fig, ax = plt.subplots(figsize=(20, 5))
#         plt.bar(group.index, plot_data.loc[group.index].values, width=0.01, color='red')

#         # Set the title and axis labels
#         plt.title(f'Occurrences of NaN values ({year}/{month:02d})')
#         plt.xlabel('Date')
#         plt.ylabel('NaN values')
#          # Add a label to the plot
#         ax.text(group.index[-1], 1.05, f'{year}/{month:02d}', ha='right', va='bottom', transform=ax.transAxes)
        
#         # Add a label to the plot for each NaN value
#         for i, nan_index in enumerate(group.index):
#             nan_value = plot_data.loc[nan_index]
#             if nan_value == 1:
#                 ax.text(nan_index, nan_value+0.1, f"{nan_index.strftime('%m-%d %H:%M')}", ha='center', fontsize=6)

#         # Set the x-axis ticks and tick labels
#         ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
#         ax.xaxis.set_major_formatter(mdates.DateFormatter('%d'))

#          # Set the y-axis tick labels
#         ax.set_yticks([0, 1])
#         ax.set_yticklabels(['No NaN', 'NaN'])

#         # Display the chart
#         plt.show()


def show_NaN_monthly(df, unit_col, year, month):
    # Create a boolean mask of NaN values
    mask = df[unit_col].isna()

    # Convert the boolean mask to 0 and 1 values
    plot_data = mask.astype(int)

    # Group the data by year and month
    groups = df.groupby([df.index.year, df.index.month])

    # Loop through each group and create a bar chart
    for (group_year, group_month), group in groups:
        if (year is None or group_year == year) and (month is None or group_month == month):
            # Create a bar chart of the NaN values in the Value column
            fig, ax = plt.subplots(figsize=(20, 5))
            plt.bar(group.index, plot_data.loc[group.index].values, width=0.01, color='red')

            # Set the title and axis labels
            plt.title(f'Occurrences of NaN values ({group_year}/{group_month:02d})')
            plt.xlabel('Date')
            plt.ylabel('NaN values')

#   Add a label to the plot for each NaN value
            for i, nan_index in enumerate(group.index):
                nan_value = plot_data.loc[nan_index]
                if nan_value == 1:
                    ax.text(nan_index, nan_value+0.1, f"{nan_index.strftime('%m-%d %H:%M')}", ha='center', fontsize=6)
            # Add a label to the plot for each NaN value
            for i, nan_index in enumerate(group.index):
                nan_value = plot_data.loc[nan_index]
                if nan_value == 1:
                    ax.text(nan_index, nan_value+0.1, f"{nan_index.strftime('%m-%d %H:%M')}", ha='center', fontsize=6)

            # Set the x-axis ticks and tick labels
            ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%d'))

            # Set the y-axis tick labels
            ax.set_yticks([0, 1])
            ax.set_yticklabels(['No NaN', 'NaN'])

            # Display the chart
            plt.show()

show_NaN_monthly(df, unit_col, args.year, args.month)