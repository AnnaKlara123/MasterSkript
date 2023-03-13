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
parser.add_argument('--unit', type=str, help='The unit to plot', default="v")
parser.add_argument('--year', type=int, help='The year to plot', default= 2020)
parser.add_argument('--month', type=int, help='The month to plot', default= 10)
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

# print(file_folder)

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

# Set the Date column as the index
df.set_index('date', inplace=True)
# # Access the data for a specific timestamp (e.g. 25-06-2019 11:00:00)
# data_for_timestamp = df.loc['2019-06-25 11:00:00']


####################### Resample df due to days and Month #############################################
# Resample the data to daily frequency and calculate the mean of each day
df_daily = df.resample('D')[unit_col].mean()

# Resample the data to monthly frequency and calculate the mean, max, and min of each month
df_monthly = df.resample('M')[unit_col].agg(['mean', 'max', 'min'])

top_15_days = df.resample('D')[unit_col].mean().nlargest(15)
print(top_15_days)


#################################  Plot the data #########################################################

def plotter(df, df_monthly, args):
    # Filter the data for the specified year and month
    df_filtered = df.loc[(df.index.year == args.year) & (df.index.month == args.month)]

    # Resample the filtered data to daily frequency and calculate the mean and max/min of each day
    df_daily = df_filtered.resample('D')[unit_col].agg(['mean', 'max', 'min'])

    # Get the monthly max and min values for the specified year and month
    monthly_data = df_monthly.loc[f'{args.year}-{args.month:02d}']
    monthly_max = monthly_data['max']
    monthly_min = monthly_data['min']

    # create plot
    fig, ax = plt.subplots(figsize=(15, 5))
    ax = df_daily['mean'].plot(label='Daily Average')
    
    # Add labels to the scatter plot
    for index, row in df_daily.iterrows():
        ax.annotate(round(row['max'], 2), xy=(index, row['max']), 
                    xytext=(-5, 10), textcoords='offset points', color='red', fontsize=5)
        ax.annotate(round(row['min'], 2), xy=(index, row['min']), 
                    xytext=(-5, -15), textcoords='offset points', color='green', fontsize=5)
    
    ax.scatter(df_daily['max'].index, df_daily['max'], marker='.', color='red', label='Daily Max')
    ax.scatter(df_daily['min'].index, df_daily['min'], marker='.', color='green', label='Daily Min')
    
    # Add horizontal lines for the monthly max and min values
    ax.hlines(monthly_max, xmin=df_daily.index.min(), xmax=df_daily.index.max(), 
              color='red', linestyle='dashed', label='Monthly Max')
    ax.hlines(monthly_min, xmin=df_daily.index.min(), xmax=df_daily.index.max(), 
              color='green', linestyle='dashed', label='Monthly Min')
    
    # Lable plot
    ax.set_xlabel('Date')
    ax.set_ylabel(f'Discharge {args.unit}')
    ax.set_title(f'Average of {args.month:02d}/{args.year}')
    ax.legend()

    # Save the plot to a file
    plt.savefig(os.path.join(file_folder, f'Average_Discharge_{args.unit}{args.month:02d}_{args.year}.png'))

    plt.show()

plotter(df, df_monthly, args)

############### Max Value Events Plotter #######################################################
def max_events(df, unit_col, top_15_days, plot=False): # If I don't want plot than set to False!
    # Iterate overt 15 days
    for date in top_15_days.index:
        max_value_timestamp = df.loc[date.strftime('%Y-%m-%d')][unit_col].idxmax()
        # Start & Endtime of the Plot
        start_time = max_value_timestamp - pd.Timedelta(hours=6)
        end_time = max_value_timestamp + pd.Timedelta(hours=6)
        data_for_plot = df[start_time:end_time][unit_col]
        # Aggregate 15min with mean
        data_for_plot = data_for_plot.resample('15T').mean()
        if plot:
            fig, ax = plt.subplots(figsize=(25, 5))
            ax.plot(data_for_plot.index, data_for_plot.values)
            ax.set_title(f'{date.strftime("%Y-%m-%d")}')
            ax.set_xlabel('Time')
            ax.set_ylabel(unit_col)
            ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=15))
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
            ax.tick_params(axis='x', labelsize=6)
            for i, value in enumerate(data_for_plot.values):
                ax.annotate(round(value, 2), (data_for_plot.index[i], value), xytext=(0, 5), textcoords='offset points', ha='center', fontsize=6)
            # Save the plot to a file
            plt.savefig(os.path.join(file_folder, f'MaximumEvents_{unit_col}_{date.strftime("%Y-%m-%d")}.png'))
            plt.show()
    return top_15_days

top_15_days = df.resample('D')[unit_col].mean().nlargest(15)
file_folder = prepare_output(file_name, args.dir)
max_events(df, unit_col, top_15_days, plot=True)
#######################################################################################################

######################### yearly and specific year total discharge ###################################
def total_discharge_year(df, unit_col, year):
    # Filter the data for the specified year
    df_filtered = df.loc[df.index.year == year]

    # Calculate the total discharge for the year
    total_discharge = df_filtered[unit_col].sum()

    # Return the result
    return total_discharge


# Calculate the total discharge for the specified year
total_discharge = total_discharge_year(df, unit_col, args.year)

# Print the result
print(f'Total discharge for {args.year}: {total_discharge} {unit_lable}')

def total_discharge_all_years(df, unit_col, output_file):
    # Group the data by year and calculate the total discharge for each year
    yearly_totals = df.groupby(df.index.year)[unit_col].sum()

    # Convert the result to a dictionary
    yearly_totals_dict = yearly_totals.to_dict()

    # Create a pandas DataFrame from the dictionary
    yearly_totals_df = pd.DataFrame.from_dict(yearly_totals_dict, orient='index', columns=['total_discharge'])

    # Add a column for the year
    yearly_totals_df['year'] = yearly_totals_df.index

    # Reorder the columns
    yearly_totals_df = yearly_totals_df[['year', 'total_discharge']]

    # Save the DataFrame to a CSV file
    yearly_totals_df.to_csv(output_file, sep='\t', index=False)

    # Return the dictionary
    return yearly_totals_dict

# Calculate the total discharge for each year and save to a CSV file
yearly_totals_dict = total_discharge_all_years(df, unit_col, os.path.join(file_folder, 'yearly_totaldischarge.csv'))

# Print the result
for year, total in yearly_totals_dict.items():
    print(f'Total discharge for {year}: {total} {unit_lable}')

#######################################################################################################
