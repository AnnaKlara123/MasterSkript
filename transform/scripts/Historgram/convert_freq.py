import os
import argparse
import pandas as pd

# Set the folder path where the CSV files are located
parser = argparse.ArgumentParser()
parser.add_argument('--dirin', type=str, help='The directory where the files are located', default="C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/GitHubMasterSkripts/MasterSkript/transform/output/convert_frequancy")
parser.add_argument('--dirout', type=str, help='The directory where the files should be saved', default="C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/GitHubMasterSkripts/MasterSkript/transform/output/10min_Frequancy")
args = parser.parse_args()


# # Loop through all the files in the folder
# for file in os.listdir(args.dirin):
#     # Check if the file is a CSV file
#     if file.endswith(".csv"):
#         # Read the CSV file into a pandas DataFrame
#         df = pd.read_csv(os.path.join(args.dirin, file), delimiter='\t')

#         # Combine the datetime columns into a single datetime object
#         timestamp = [pd.Timestamp(int(row['YY']), int(row['MM']), int(row['DD']), int(row['HH']), int(row['MN'])) for i, row in df.iterrows()]

#         # Set the date-time columns as a new pandas DatetimeIndex
#         # datetime_cols = ['YY', 'MM', 'DD', 'HH', 'MN']
#         df['timestamp'] = pd.to_datetime(df[timestamp])
#         df = df.set_index('timestamp')

#         # Convert the DataFrame values to float
#         df = df.apply(pd.to_numeric, errors='coerce')

#         # Use the rolling method to resample the DataFrame to a 10-minute frequency,
#         # using the average value of the previous, current, and next timesteps
#         df = df.rolling(3, min_periods=1).mean().iloc[2::3]

#         # Reset the index to columns and save the resampled DataFrame as a new CSV file
#         df = df.reset_index()
#         new_file_name = os.path.splitext(file)[0] + "_10min.csv"
#         df.to_csv(os.path.join(args.dirout, new_file_name), sep='\t', index=False)


# Loop through all the files in the folder
for file in os.listdir(args.dirin):
    # Check if the file is a CSV file
    if file.endswith(".csv"):
        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv(os.path.join(args.dirin, file), delimiter='\t')

        # Combine the datetime columns into a single datetime object
        timestamp = [pd.Timestamp(int(row['YY']), int(row['MM']), int(row['DD']), int(row['HH']), int(row['MN'])) for i, row in df.iterrows()]

        # Set the timestamp as the new DataFrame index
        # df = df.drop(['YY', 'MM', 'DD', 'HH', 'MN'], axis=1)
        df.index = timestamp

        # Convert the DataFrame values to float
        df = df.apply(pd.to_numeric, errors='coerce')

         # Shift the DataFrame forward by 10 minutes
        df = df.shift(periods=-1, freq='10T')

        # Resample the DataFrame to a 10-minute frequency starting from minute 0,
        # using the average value of the previous and current timesteps
        df = df.resample('10T', origin='start').mean()

        # Reset the index to columns and save the resampled DataFrame as a new CSV file
        df = df.reset_index()
        new_file_name = os.path.splitext(file)[0] + "_10min.csv"
        df.to_csv(os.path.join(args.dirout, new_file_name), sep='\t', index=False)
