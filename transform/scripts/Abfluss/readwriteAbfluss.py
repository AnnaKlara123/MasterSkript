import pandas as pd
import argparse
import os
from termcolor import colored
import matplotlib.pyplot as plt
import calendar

# Create the parser
parser = argparse.ArgumentParser()
parser.add_argument('--dir', type=str, help='The directory where the file is located', default='C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/GitHubMasterSkripts/MasterSkript/transform/input/Abfluss')
parser.add_argument('--filename', type=str, help='The filename to read',  default='RQ30_data_20190625_20220818.csv')
parser.add_argument('--year', type=int, help='The year to plot', default= 2019)
parser.add_argument('--month', type=int, help='The month to plot', default= 10)
args = parser.parse_args()


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

# print(file_folder)

# Read in the CSV file
df = pd.read_csv(file_path, sep=';')

# Rename the columns
df.columns = ['date', 'h', 'v', 'QStat']
df['h'] = df['h'].astype(float)
df['v'] = df['v'].astype(float)
df['QStat'] = df['QStat'].astype(float)


# Convert the Date column to a pandas datetime format
df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y %H:%M:%S')

# Set the Date column as the index
df.set_index('date', inplace=True)

# # Access the data for a specific timestamp (e.g. 25-06-2019 11:00:00)
# data_for_timestamp = df.loc['2019-06-25 11:00:00']

####################### Resample df due to days and Month #############################

# Resample the data to daily frequency and calculate the mean of each day
df_daily = df.resample('D')['QStat'].mean()

# Resample the data to monthly frequency and calculate the mean, max, and min of each month
df_monthly = df.resample('M')['QStat'].agg(['mean', 'max', 'min'])

# Save the daily DataFrame to a CSV file
df_daily.to_csv(os.path.join(file_folder, 'daily_average.csv'))

# Save the monthly DataFrame to a CSV file
df_monthly.to_csv(os.path.join(file_folder, 'monthly_average.csv'))


#################################  Plot the data #########################################################

def plotter(df, df_monthly, args):
    # Filter the data for the specified year and month
    df_filtered = df.loc[(df.index.year == args.year) & (df.index.month == args.month)]

    # Resample the filtered data to daily frequency and calculate the mean and max/min of each day
    df_daily = df_filtered.resample('D')['QStat'].agg(['mean', 'max', 'min'])

    # Get the monthly max and min values for the specified year and month
    monthly_data = df_monthly.loc[f'{args.year}-{args.month:02d}']
    monthly_max = monthly_data['max']
    monthly_min = monthly_data['min']


    # Plot the data
    fig, ax = plt.subplots(figsize=(10, 5))
    ax = df_daily['mean'].plot(label='Daily Average')
    ax.scatter(df_daily['max'].index, df_daily['max'], marker='.', color='red', label='Daily Max')
    ax.scatter(df_daily['min'].index, df_daily['min'], marker='.', color='green', label='Daily Min')
    # Add horizontal lines for the monthly max and min values
    ax.hlines(monthly_max, xmin=df_daily.index.min(), xmax=df_daily.index.max(), 
              color='red', linestyle='dashed', label='Monthly Max')
    ax.hlines(monthly_min, xmin=df_daily.index.min(), xmax=df_daily.index.max(), 
              color='green', linestyle='dashed', label='Monthly Min')
    ax.set_xlabel('Date')
    ax.set_ylabel('Discharge QStat mm/s')
    ax.set_title(f'Average of {args.month:02d}/{args.year}')
    ax.legend()
    plt.show()
    


# Save the plot to a file
    plt.savefig(os.path.join(file_folder, f'Average_Discharge_{args.month:02d}_{args.year}.png'))


plotter(df, df_monthly, args)
###########################################################################################
# # Plot the data
# fig, ax = plt.subplots(figsize=(10, 5))
# ax = df_daily['mean'].plot(label='Daily Average')
# ax.scatter(daily_max.index, daily_max, marker='.', color='red', label='Daily Max')
# ax.scatter(daily_min.index, daily_min, marker='.', color='green', label='Daily Min')
# ax.set_xlabel('Date')
# ax.set_ylabel('Discharge')
# ax.set_title(f'Average of {args.month:02d}/{args.year}')
# ax.legend()
# plt.show()

# # Save the plot to a file
# plt.savefig(os.path.join(file_folder, f'Average_Discharge_{args.month:02d}_{args.year}.png'))






#########################################################################################
# # Filter the data for the specified year and month
# df_filtered = df.loc[(df.index.year == args.year) & (df.index.month == args.month)]

# # Resample the filtered data to daily frequency and calculate the mean of each day
# df_daily = df_filtered.resample('D')['QStat'].mean()

# # Resample the filtered data to monthly frequency and calculate the mean, max, and min of each month
# df_monthly = df_filtered.resample('M')['QStat'].agg(['mean', 'max', 'min'])

# # Plot the data
# ax = df_daily.plot(label='Daily Average')
# df_monthly[['mean', 'max', 'min']].plot(style=['-', 'o', 'o'], ax=ax, label='Max/Min/Mean')
# ax.set_xlabel('Date')
# ax.set_ylabel('Discharge')
# ax.set_title(f'Average of {args.month:02d}/{args.year}')
# ax.legend()
# plt.show()

# # Save the plot to a file
# plt.savefig(os.path.join(file_folder, f'Average_{args.month:02d}_{args.year}.png'))




# # Get the month name from the month number
# month_name = calendar.month_name[args.month]

# # Filter the daily data to include only the data for the specified month
# df_daily_month = df_daily[df_daily.index.month == args.month]

# # Filter the monthly data to include only the data for the specified month
# df_monthly_month = df_monthly[df_monthly.index.month == args.month]

# # Create the plot title
# plot_title = f'Average of {month_name}'

# # Plot the data
# ax = df_daily_month.plot(label='Daily Average')
# df_monthly_month[['mean', 'max', 'min']].plot(style=['o', 'o', 'o'], ax=ax, label='Max/Min/Mean')
# ax.set_xlabel('Date')
# ax.set_ylabel('Discharge')
# ax.set_title(plot_title)
# ax.legend()
# plt.show()

# # Plot the data for the whole timeframe 
# ax = df_daily.plot(label='Daily Average')
# df_monthly['mean'].plot(ax=ax, label='Monthly Average')
# df_monthly[['max', 'min']].plot(style=['o', 'o'], ax=ax, label='Max/Min')
# ax.set_xlabel('Date')
# ax.set_ylabel('Discharge')
# ax.legend()
# plt.show()








# # Calculate the monthly average, maximum, and minimum
# df_resampled = df.resample('M')['QStat'].agg(['mean', 'max', 'min'])

# # Plot the data
# ax = df_grouped.plot(label='Daily Average')
# df_resampled['mean'].plot(ax=ax, label='Monthly Average')
# df_resampled[['max', 'min']].plot(style=['o', 'o'], ax=ax, label='Max/Min')
# ax.set_xlabel('Date')
# ax.set_ylabel('Discharge')
# ax.legend()
