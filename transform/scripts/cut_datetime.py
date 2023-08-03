import os
import argparse
import pandas as pd
import numpy as np

# Set the folder path where the CSV files are located
parser = argparse.ArgumentParser()
parser.add_argument('--dirin', type=str, help='The directory where the files are located', default="C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/GitHubMasterSkripts/MasterSkript/transform/output/convert_frequancy/10min_frequency_Neu/GH_filled/Humidity_LWD/cut")
parser.add_argument('--dirout', type=str, help='The directory where the files should be saved', default= "C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/GitHubMasterSkripts/MasterSkript/transform/output/convert_frequancy/10min_frequency_Neu/GH_filled/Humidity_LWD/cut")
parser.add_argument('--startdate', type=str, help='The startdate that the df shoud start',default='2014-09-01')
parser.add_argument('--enddate', type=str, help='The enddate of the dataset', default='2018-09-30')

args = parser.parse_args()

# Define the desired start / end date
start_date = pd.to_datetime(args.startdate)
end_date = pd.to_datetime(args.enddate)

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

        # Truncate the data to the desired start and end dates
        df = df.truncate(before=start_date, after=end_date)

        # Reset the index and drop the timestamp column
        df.reset_index(drop=True, inplace=True)

        # Save the modified DataFrame to a new CSV file
        new_file_name = os.path.splitext(file)[0] + "_cut.csv"
        df.to_csv(os.path.join(args.dirout, new_file_name), sep='\t', index=False)

# Print a message indicating that the script has finished running
print("Script completed!")