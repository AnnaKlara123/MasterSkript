import os
import argparse
import pandas as pd

# Set the folder path where the CSV files are located
parser = argparse.ArgumentParser()
parser.add_argument('--dirin', type=str, help='The directory where the files are located', default="C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/GitHubMasterSkripts/MasterSkript/transform/output/convert_frequancy")
parser.add_argument('--dirout', type=str, help='The directory where the files should be saved', default="C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/GitHubMasterSkripts/MasterSkript/transform/output/convert_frequancy/10min_Frequancy")
parser.add_argument('--startdate', type=str, help='The startdate then the df shoud start', default='2014-09-01')
args = parser.parse_args()

# Define the desired start date
start_date = pd.to_datetime(args.startdate)

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
        df = df.apply(pd.to_numeric, errors='coerce')

        # Resample the DataFrame to a 10-minute frequency using mean
        df = df.resample('10T').mean()

        # Update the MN column with the minutes from the new index
        df['MN'] = df.index.minute
        # Convert the YY, MM, DD, and HH columns to integers and remove the .0
        df['YY'] = df.index.year.astype(int).astype(str)
        df['MM'] = df.index.month.astype(int).astype(str)
        df['DD'] = df.index.day.astype(int).astype(str)
        df['HH'] = df.index.hour.astype(int).astype(str)
        df['MN'] = df.index.minute.astype(int).astype(str)

       # Define the new index with the desired start date and frequency
        new_index = pd.date_range(start=start_date, periods=len(df), freq='10T')

        # Reindex the DataFrame using the new index
        df = df.reindex(new_index)

        # Reset the index and drop the timestamp column. Save the resampled DataFrame as a new CSV file
        df = df.reset_index().drop('index', axis=1)

        ## # #####  create a header row CHANGE LAT, LONG & height FOR DIFFERENT STATIONS!#####################################
        # # header_row = pd.DataFrame([['YY', 'MM', 'DD', 'HH', 'MN', 'STATIONNAEME'], ['YY', 'MM', 'DD', 'HH', 'MN', 'height'], ['YY', 'MM', 'DD', 'HH', 'MN', 'LONGNITUDE'], ['YY', 'MM', 'DD', 'HH', 'MN', 'LATITUDE'], ['YY', 'MM', 'DD', 'HH', 'MN', 'Stat1']], columns=['YY', 'MM', 'DD', 'HH', 'MN', 'Stat1'])
        # # # concatenate the header row with the data frame
        # # df = pd.concat([header_row, df], ignore_index=True)

        new_file_name = os.path.splitext(file)[0] + "_10min.csv"
        df.to_csv(os.path.join(args.dirout, new_file_name), sep='\t', index=False)
        print("Saving:",new_file_name)