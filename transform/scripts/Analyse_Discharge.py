import os
import argparse
import pandas as pd
from tqdm import tqdm

########################  Calculate top 100 Mean or Max Days #################################

# Set the folder path where the CSV files are located
parser = argparse.ArgumentParser()
parser.add_argument('--dirin', type=str, help='The directory where the files are located',
                    default="C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/Meteo_Discharge/AnalyseTest_0610/Discharge")
parser.add_argument('--dirout', type=str, help='The directory where the files should be saved',
                    default="C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/Meteo_Discharge/AnalyseTest_0610/Discharge")
args = parser.parse_args()

count = 0

# # Create an empty DataFrame to store the daily mean values
# daily_mean_df = pd.DataFrame(columns=['Date', 'Mean'])

# # Create an empty DataFrame to store the hourly mean values
# hourly_mean_df = pd.DataFrame(columns=['Date', 'Mean'])

# # Loop through all the files in the folder
# for file in os.listdir(args.dirin):
#     # Check if the file is a CSV file
#     if file.endswith(".csv"):
#         # Increment the counter variable
#         count += 1

#         # Read the CSV file into a pandas DataFrame
#         df = pd.read_csv(os.path.join(args.dirin, file), delimiter='\t')
#         # Extract the base name of the input file without the extension
#         input_file_name = os.path.splitext(os.path.basename(file))[0]


#         # Combine the datetime columns into a single datetime object
#         timestamp = [pd.Timestamp(int(row['YY']), int(row['MM']), int(row['DD']), int(row['HH']), int(row['MN'])) for i, row in df.iterrows()]

#         # Convert the timestamp list to a DatetimeIndex object and set it as the new index
#         df.index = pd.DatetimeIndex(timestamp)

#         # Convert the DataFrame values to float
#         df['Stat1'] = pd.to_numeric(df['Stat1'], errors='coerce')

#         # Calculate the daily mean/mean for the period between April 20th and October 20th each year (summer months)
#         df_filtered = df[(df.index.month >= 4) & (df.index.month <= 10) | ((df.index.month == 4) & (df.index.day >= 20)) | ((df.index.month == 10) & (df.index.day <= 20))]
#         daily_mean = df_filtered['Stat1'].resample('D').mean()
#         #daily_mean = df_filtered['Stat1'].resample('D').max()


#         # Create a DataFrame for daily_mean with 'Date' and 'Mean' columns
#         daily_mean = daily_mean.reset_index()
#         daily_mean.columns = ['Date', 'Mean']

#         # Append the daily_mean to the daily_mean_df
#         daily_mean_df = pd.concat([daily_mean_df, daily_mean], axis=0)

#         # Calculate the hourly mean for the period between April 20th and October 20th each year
#         hourly_mean = df_filtered['Stat1'].resample('H').mean()

#         # Create a DataFrame for hourly_mean with 'Date' and 'Mean' columns
#         hourly_mean = hourly_mean.reset_index()
#         hourly_mean.columns = ['Date', 'Mean']

#         # Append the hourly_mean to the hourly_mean_df
#         hourly_mean_df = pd.concat([hourly_mean_df, hourly_mean], axis=0)


# # Sort the daily_mean_df by the 'Mean' column in descending order
# daily_mean_df_sorted = daily_mean_df.sort_values(by='Mean', ascending=False)

# # Get the top 20 days with the highest mean values
# top_20_days = daily_mean_df_sorted.head(100)

# top_20_days['Mean'] = top_20_days['Mean'].round(2)

# # Print the top 20 days
# print("Top 20 days with the highest mean values:")
# print(top_20_days)

# # Save the top 20 days to a new CSV file without index and in a cleaner format
# output_csv_path = os.path.join(args.dirout, f"top_20_daysmean_{input_file_name}.txt")
# top_20_days.to_csv(output_csv_path, index=False, header=['Date', 'Mean'])
# print(f"Top 20 days saved to {output_csv_path}")

# # Sortiere die daily_max_df_sorted DataFrame nach dem Datum in aufsteigender Reihenfolge
# top_20_days_sorted = top_20_days.sort_values(by='Date')

# # Nun kannst du die sortierten Daten anzeigen oder speichern
# print("Events nach Datum sortiert:")
# print(top_20_days_sorted)

# # Um die sortierten Daten in eine neue CSV-Datei zu speichern
# output_csv_sorted_path = os.path.join(args.dirout, f"sorted_max_events_{input_file_name}.txt")
# top_20_days_sorted.to_csv(output_csv_sorted_path, index=False, header=['Date', 'Mean'])
# print(f"Sortierte Events nach Datum wurden in {output_csv_sorted_path} gespeichert.")

########################### Vergleich Top Discharge mit TOP RAIN #######################


# # Sort the hourly_mean_df by the 'Mean' column in descending order
# hourly_mean_df_sorted = hourly_mean_df.sort_values(by='Mean', ascending=False)

# # Get the top 20 hours with the highest mean values
# top_20_hours = hourly_mean_df_sorted.head(20)

# # Round the 'Mean' values to 2 decimal places
# top_20_hours['Mean'] = top_20_hours['Mean'].round(2)

# # Save the top 20 hours to a new CSV file without index and header
# output_top_20_hours_path = os.path.join(args.dirout, f"top_20_hours_{input_file_name}.txt")
# if not top_20_hours.empty:
#     top_20_hours.to_csv(output_top_20_hours_path, index=False, header=['Date', 'Mean'])
#     print(f"Top 20 hours with the highest mean values saved to {output_top_20_hours_path}")
# else:
#     print("No data available for the specified period.")



# ## Filter periods of rainfall for at least 3 days in a row
# rain_periods = []
# current_rain_period = []
# current_rain_mean = 0  # Variable to keep track of the current rain period's total mean
# for _, row in daily_mean_df.iterrows():
#     if row['Mean'] > 0:
#         current_rain_period.append(row['Date'])
#         current_rain_mean += row['Mean']
#     else:
#         if len(current_rain_period) >= 3:
#             current_rain_mean = round(current_rain_mean, 2)
#             rain_periods.append({'Period': current_rain_period, 'Total Rainfall': current_rain_mean})
#         current_rain_period = []
#         current_rain_mean = 0

# # Save the rain periods to a file
# rain_periods_output_path = os.path.join(args.dirout, "rain_periods.txt")
# with open(rain_periods_output_path, 'w') as f:
#     for i, period in enumerate(rain_periods, start=1):
#         f.write(f"Rain Period {i}:\n")
#         f.write(f"Start Date: {period['Period'][0]}\n")
#         f.write(f"End Date: {period['Period'][-1]}\n")
#         f.write(f"Total Rainfall: {period['Total Rainfall']} mm\n\n")
# print(f"Rain periods saved to {rain_periods_output_path}")


# # Convert the 'Date' columns in both DataFrames to a common date format
# top_20_days['Date'] = top_20_days['Date'].dt.strftime('%Y-%m-%d')
# top_20_hours['Date'] = top_20_hours['Date'].dt.strftime('%Y-%m-%d')

# # Check if any of the dates in top_20_days match any of the dates in top_20_hours
# matching_dates = top_20_days['Date'].isin(top_20_hours['Date'])

# # Get the matching days
# matching_days = top_20_days[matching_dates]

# # Save the matching days to a CSV file
# output_matching_days_path = os.path.join(args.dirout, "matching_top_days.txt")

# if not matching_days.empty:
#     matching_days.to_csv(output_matching_days_path, index=False)
#     print(f"Matching days saved to {output_matching_days_path}")
# else:
#     print("No matching days found between top 20 days and top 20 hours, so no file was saved.")



######### PLOT THE TOP 100 dayly mean discharge  DAYS!!! ##########################

# import pandas as pd
# import matplotlib.pyplot as plt

# # Read the CSV file
# data = pd.read_csv('C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/Meteo_Discharge/AnalyseTest_0610/Discharge/20.10.23/top_20_daysmax_DischargeQStat.csv')

# # Convert the 'Date' column to datetime format
# data['Date'] = pd.to_datetime(data['Date'])

# # Sort the DataFrame by the 'Date' column
# data.sort_values(by='Date', inplace=True)

# # Select the top 100 daily mean discharge values
# top_100_data = data.head(100)

# # Create subplots with adjusted spacing
# plt.subplots_adjust(top=0.586,
# bottom=0.307,
# left=0.137,
# right=0.96,
# hspace=0.2,
# wspace=0.2)
# fig, ax = plt.subplots(figsize=(10, 6))
# plt.plot(top_100_data['Date'], top_100_data['Mean'],  marker='o', color='b',  linewidth=0.8)
# plt.title('Top 100 Daily Mean Discharge Values')
# plt.xlabel('Date')
# plt.ylabel('Mean Discharge m3/s')
# plt.grid(True)
# plt.tight_layout()
# plt.legend()

# # Add a grid to the subplot
# ax.grid(True)

# # Show the plot
# plt.show()



##########################################   ##############################################
# Create an empty DataFrame to store the daily mean values
daily_values_df = pd.DataFrame(columns=['Date', 'Daily mean value', 'Daily max value'])

# Loop through all the files in the folder
for file in os.listdir(args.dirin):
    # Check if the file is a CSV file
    if file.endswith(".csv"):
        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv(os.path.join(args.dirin, file), delimiter='\t')

        # Combine the datetime columns into a single datetime object
        timestamp = [pd.Timestamp(int(row['YY']), int(row['MM']), int(row['DD']), int(row['HH']), int(row['MN'])) for i, row in df.iterrows()]

        # Convert the timestamp list to a DatetimeIndex object and set it as the new index
        df.index = pd.DatetimeIndex(timestamp)

        # Convert the DataFrame values to float
        df['Stat1'] = pd.to_numeric(df['Stat1'], errors='coerce')

        # Calculate the daily mean for the period between April 20th and October 20th each year (summer months)
        df_filtered = df[(df.index.month >= 4) & (df.index.month <= 10) | ((df.index.month == 4) & (df.index.day >= 20)) | ((df.index.month == 10) & (df.index.day <= 20))]
        daily_mean = df_filtered['Stat1'].resample('D').mean().round(2) 

        # Calculate the daily max value corresponding to the daily mean
        daily_max = df_filtered['Stat1'].resample('D').max().round(2) 

        # Calculate the daily discharge by multiplying the daily mean by 86400
        daily_discharge = (daily_mean * 86400).round(2) 

        # Create a DataFrame for daily_mean, daily_max, and daily_discharge with 'Date' and respective columns
        daily_values = pd.DataFrame({'Date': daily_mean.index, 'Daily mean value': daily_mean.values, 'Daily max value': daily_max.values, 'Daily discharge': daily_discharge})

        # Append the daily_values to the daily_values_df
        daily_values_df = pd.concat([daily_values_df, daily_values], axis=0)


## To sort after the daily Mean Use this:
# Sort the daily_values_df by 'Daily mean value' in descending order
daily_values_df_sorted = daily_values_df.sort_values(by='Daily mean value', ascending=False)

# Get the top 100 days with the highest mean values
top_100_days = daily_values_df_sorted.head(100)

# Sort the daily_values_df by 'Daily mean value' in descending order
top_100_days =top_100_days.sort_values(by='Date', ascending=True)

# Save the top 100 days to a new CSV file
output_top_100_path = os.path.join(args.dirout, "top_100_days_mean_max_discharge.csv")
top_100_days.to_csv(output_top_100_path, index=False)
print(f"Top 100 days with highest mean values saved to {output_top_100_path}")


### To sort after daily max use this:

# Sort the daily_values_df by 'Daily mean value' in descending order
daily_values_df_sorted = daily_values_df.sort_values(by='Daily max value', ascending=False)

# Get the top 100 days with the highest mean values
top_100_days = daily_values_df_sorted.head(100)

# Sort the top_100_days DataFrame by 'Daily max value' in descending order
top_100_days = top_100_days.sort_values(by='Date', ascending=True)

# Save the top 100 days to a new CSV file
output_top_100_path = os.path.join(args.dirout, "top_100_days_mean_max_discharge.csv")
top_100_days.to_csv(output_top_100_path, index=False)
print(f"Top 100 days with highest mean values and sorted by max value saved to {output_top_100_path}")