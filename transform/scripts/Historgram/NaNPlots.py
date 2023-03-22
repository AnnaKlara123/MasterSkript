import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
from matplotlib.dates import date2num
import argparse
import os

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
    print(f'Created directory: {plot_dir}')

# Create a folder for the current file if it doesn't exist
file_folder = os.path.join(plot_dir, f'NaN_Plots{file_name[:-4]}')
if not os.path.exists(file_folder):
    os.makedirs(file_folder)
    print(f'Created directory: {file_folder}')

# Extract the values from the Stat1 column
x = df['Stat1'].values

# Combine the datetime columns into a single datetime object
dates = [pd.Timestamp(int(row['YY']), int(row['MM']), int(row['DD']), int(row['HH']), int(row['MN'])) for i, row in df.iterrows()]

# Set the datetime index for the dataframe
df.index = dates

# Remove the YY, MM, DD, HH, and MN columns from the dataframe
df = df.drop(columns=['YY', 'MM', 'DD', 'HH', 'MN'])

# Create a boolean mask of NaN values
mask = df['Stat1'].isna()

# Convert the boolean mask to 0 and 1 values
plot_data = mask.astype(int)

# Group the data by year and month
groups = df.groupby([df.index.year, df.index.month])

############################## NaN Plot specific Month / Year ###################################

# # Loop through each group and create a bar chart
# for (year, month), group in groups:
#     if (args.year is None or year == args.year) and (args.month is None or month == args.month):
#         # Create a bar chart of the NaN values in the 'Stat1' column
#         fig, ax = plt.subplots(figsize=(20, 8))
#         plt.bar(group.index, plot_data.loc[group.index].values, width=0.001, color='red')

#         # Set the title and axis labels
#         plt.title(f'Occurrences of NaN values in Stat1 column ({year}/{month:02d})')
#         plt.xlabel('Date')
#         plt.ylabel('NaN values')
#          # Add a label to the plot
#         ax.text(group.index[-1], 1.05, f'{year}/{month:02d}', ha='right', va='bottom', transform=ax.transAxes)
#          # Set the x-axis ticks and tick labels
#         ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
#         ax.xaxis.set_major_formatter(mdates.DateFormatter('%d'))

#         # Display the chart
#         plt.show()

###################################################################################################

###################### Get the data monthly for a specific year ###################################
# Filter the dataframe by the year specified in the command line argument
if args.year is not None:
    df = df[df.index.year == args.year]

# Create a bar chart of the NaN values in the 'Stat1' column
fig, ax = plt.subplots(figsize=(20, 8))
plt.bar(df.index, plot_data.loc[df.index].values, width=0.001, color='red')

# Set the title and axis labels
plt.title(f'Occurrences of NaN values in Stat1 column ({args.year})')
plt.xlabel('Month')
plt.ylabel('NaN values')

# Set the x-axis ticks and tick labels
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))

# Save the plot as a file
if args.year is not None:
    plot_filename = f'NaN_Plots_{file_name[:-4]}_{args.year}.png'
else:
    plot_filename = f'NaN_Plots_{file_name[:-4]}.png'
plot_filepath = os.path.join(file_folder, plot_filename)
fig.savefig(plot_filepath)

# Display the chart
plt.show()
