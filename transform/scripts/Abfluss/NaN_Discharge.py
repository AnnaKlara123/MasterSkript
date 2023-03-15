import pandas as pd
import argparse
import os
from termcolor import colored
import matplotlib.pyplot as plt
import calendar
import matplotlib.dates as mdates
import numpy as np



parser = argparse.ArgumentParser()
parser.add_argument('--dir', type=str, help='The directory where the file is located', default='C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/GitHubMasterSkripts/MasterSkript/transform/input/Abfluss/Dischargeanalyse/DischargeRQ30_data_20190625_20220818')
parser.add_argument('--filename', type=str, help='The filename to read',  default='NaNRQ30_data_20190625_20220818test.csv')
parser.add_argument('--unit', type=str, help='The unit to plot', default="QStat")
parser.add_argument('--year', type=int, help='The year to plot' )
parser.add_argument('--month', type=int, help='The month to plot' )
parser.add_argument('--Station_name', type=str, help='Name of the Station', default="Jambach")
parser.add_argument('--hight', type=int, help='Hight of the Station', default="0")
parser.add_argument('--latitude', type=float, help='latitude of the Station', default="0.0")
parser.add_argument('--longitude', type=float, help='longitude of the Station', default="0.0")
args = parser.parse_args()

# # Select the appropriate column based on the input unit
# if args.unit == 'QStat':
#     unit_col = 'QStat'
#     unit_lable = "l/s"
# elif args.unit == 'h':
#     unit_col = 'h'
#     unit_lable = "cm"
# elif args.unit == 'v':
#     unit_col = 'v'
#     unit_lable = "m^3"
# else:
#     raise ValueError('Invalid unit specified')

# # Get the base filename
# file_name = os.path.basename(args.filename)

# # Build the full filepath from the directory and filename arguments
# file_path = os.path.join(args.dir, args.filename)

# def prepare_output(file_name, plot_dir):
#     # Create a subdirectory called 'Dischargeanalyse' within the directory specified by --dir
#     plot_dir = os.path.join(args.dir, 'Dischargeanalyse')
#     if not os.path.exists(plot_dir):
#         os.makedirs(plot_dir)
#         print(f'Created directory: {colored(plot_dir, "green")}')

#     # Create a folder for the current file if it doesn't exist
#     file_folder = os.path.join(plot_dir, f'Discharge{file_name[:-4]}')
#     if not os.path.exists(file_folder):
#         os.makedirs(file_folder)
#         print(f'Created directory: {colored(file_folder, "green")}')
    
#     return file_folder

# # Call the function and assign the result to a variable
# file_folder = prepare_output(file_name, args.dir)

# # Read in the CSV file
# #df = pd.read_csv(file_path, sep=';')
# #df = pd.read_csv(file_path, sep=';', na_values=['NA', 'N/A', 'null', ' '], encoding='utf-8' )


# Read in the CSV file
df = pd.read_csv('C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/GitHubMasterSkripts/MasterSkript/transform/input/Abfluss/Dischargeanalyse/DischargeRQ30_data_20190625_20220818/NaNRQ30_data_20190625_20220818.csv', sep=';', parse_dates=['Date'], na_values=['NA','NaN', 'nan'], index_col='Date')

print(df)
# Convert the Date column to a pandas datetime format
#df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y %H:%M:%S')

# # Get the boolean mask of NaN values
# mask1 = pd.isna(df)

# # # Select only the rows with NaN values and print them out
# # print(df[mask.any(axis=1)])

# # Creates a df, that contains all days with nan Values
# df_nan = df[mask1.any(axis=1)]   # works fine!
# print(df_nan)

# Create a boolean mask indicating whether each value is NaN
mask = df.isna()

# Reduce the boolean mask to a boolean Series indicating whether each row contains NaN values
nan_mask = mask.any(axis=1)

# Index the DataFrame to get only the rows that contain NaN values
df_nan = df[nan_mask]           # Worls fine!
# df_nan.to_csv('C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/GitHubMasterSkripts/MasterSkript/transform/input/Abfluss/Dischargeanalyse/DischargeRQ30_data_20190625_20220818/nan_valuelist_discharge.csv')
# print('NaN outputlist saved')
# Extract the date column from the DataFrame
dates = df_nan.index
# df_nan.to_csv('C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/GitHubMasterSkripts/MasterSkript/transform/input/Abfluss/Dischargeanalyse/DischargeRQ30_data_20190625_20220818/nan_dates_discharge.csv')
# print('NaN Dates saved')

# Create a line plot where the x-axis represents the dates and the y-axis represents the occurrence of NaN values
fig, ax = plt.subplots(figsize=(20, 5))
plt.plot(dates, [1]*len(dates), '.')
plt.title('NaN Values over Time')
plt.xlabel('Date')
plt.ylabel('NaN Value Occurrence')

# Loop over each date and annotate the corresponding dot with the date
# Add a label to the plot for each NaN value
for i, date in enumerate(dates):
    ax.text(date, 0.9, f"{date.strftime('%m-%d %H:%M')}", ha='center', fontsize=6)

# Set the x-axis ticks and tick labels
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%y'),fontsize=6)

# Set the y-axis tick labels
ax.set_yticks([0, 1])
ax.set_yticklabels(['No NaN', 'NaN'])

plt.show()

# # Create a line plot of the data with NaN values highlighted in red
# fig, ax = plt.subplots()
# df.plot(ax=ax)
# nan_df_mask[nan_df_mask == 1].plot(ax=ax, color='red', linewidth=2)
# plt.show()

# Create a boolean mask of NaN values
# mask = []

# for _, row in df.iterrows():
#     if pd.isna(row['QStat']):
#         mask.append(row)
        
# # Create a new dataframe from the mask
# mask_df = pd.DataFrame(mask, columns=['Date', 'QStat'])

# # Print the new dataframe
# print(mask_df)

            #     value = row['QStat']
#df.to_csv('C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/GitHubMasterSkripts/MasterSkript/transform/input/Abfluss/Dischargeanalyse/DischargeRQ30_data_20190625_20220818/new_file.csv', sep=';', index=False)


# #Convert the boolean mask to 0 and 1 values
# plot_data = mask.astype(int)

# # Create a bar chart of the NaN values in the QStat column
# fig, ax = plt.subplots(figsize=(20, 5))
# plt.bar(df.index, plot_data.values, width=0.1, color='red')

# # Set the title and axis labels
# plt.title('Occurrences of NaN values')
# plt.xlabel('Date')
# plt.ylabel('NaN values')

# # Add a label to the plot for each NaN value
# for i, nan_index in enumerate(df[mask].index):
#     ax.text(nan_index, plot_data.loc[nan_index]+0.1, f"{nan_index.strftime('%m-%d %H:%M')}", ha='center', fontsize=6)

# # Set the x-axis ticks and tick labels
# ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
# ax.xaxis.set_major_formatter(mdates.DateFormatter('%d'))

# # Set the y-axis tick labels
# ax.set_yticks([0, 1])
# ax.set_yticklabels(['No NaN', 'NaN'])

# # Display the chart
# plt.show()

