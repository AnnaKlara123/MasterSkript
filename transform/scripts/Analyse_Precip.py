import os
import argparse
import pandas as pd

# Set the folder path where the CSV files are located
parser = argparse.ArgumentParser()
parser.add_argument('--dirin', type=str, help='The directory where the files are located',
                    default="C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/Meteo_Discharge/AnalyseTest_0610")
parser.add_argument('--dirout', type=str, help='The directory where the files should be saved',
                    default="C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/Meteo_Discharge/AnalyseTest_0610")
parser.add_argument('--startdate', type=str, help='The startdate that the df should start', default='2019-6-26')
parser.add_argument('--enddate', type=str, help='The enddate of the dataset', default='2022-8-19')
args = parser.parse_args()

# Define the desired start / end date
start_date = pd.to_datetime(args.startdate)
end_date = pd.to_datetime(args.enddate)

count = 0

# Create an empty DataFrame to store the daily sum values
daily_sum_df = pd.DataFrame(columns=['Date', 'Sum'])

# Loop through all the files in the folder
for file in os.listdir(args.dirin):
    # Check if the file is a CSV file
    if file.endswith(".csv"):
        # Increment the counter variable
        count += 1

        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv(os.path.join(args.dirin, file), delimiter='\t')

        # Combine the datetime columns into a single datetime object
        timestamp = [pd.Timestamp(int(row['YY']), int(row['MM']), int(row['DD']), int(row['HH']), int(row['MN'])) for i, row in df.iterrows()]

        # Convert the timestamp list to a DatetimeIndex object and set it as the new index
        df.index = pd.DatetimeIndex(timestamp)

        # Convert the DataFrame values to float
        df['Stat1'] = pd.to_numeric(df['Stat1'], errors='coerce')

        # Calculate the daily sum
        daily_sum = df['Stat1'].resample('D').sum()

        # Create a DataFrame for daily_sum with 'Date' and 'Sum' columns
        daily_sum = daily_sum.reset_index()
        daily_sum.columns = ['Date', 'Sum']

        # Append the daily_sum to the daily_sum_df
        daily_sum_df = pd.concat([daily_sum_df, daily_sum], axis=0)


# Sort the daily_sum_df by the 'Sum' column in descending order
daily_sum_df_sorted = daily_sum_df.sort_values(by='Sum', ascending=False)

# Get the top 20 days with the highest sum values
top_20_days = daily_sum_df_sorted.head(20)

# Print the top 20 days
print("Top 20 days with the highest sum values:")
print(top_20_days)

# Save the top 20 days to a new CSV file
output_csv_path = os.path.join(args.dirout, "top_20_days.csv")
top_20_days.to_csv(output_csv_path)
print(f"Top 20 days saved to {output_csv_path}")
