import os
import argparse
import pandas as pd
import numpy as np

# Set the folder path where the CSV files are located
parser = argparse.ArgumentParser()
parser.add_argument('--dirin', type=str, help='The directory where the files are located', default="C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/WaSiM_Execution0908/Input/hyd")
parser.add_argument('--dirout', type=str, help='The directory where the files should be saved', default= "C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/WaSiM_Execution0908/Input/hyd")
parser.add_argument('--startdate', type=str, help='The startdate that the df shoud start',default='2019-6-26')
parser.add_argument('--enddate', type=str, help='The enddate of the dataset', default='2022-8-19')
args = parser.parse_args()

# Define the desired start / end date
start_date = pd.to_datetime(args.startdate)
# Define the desired start date
end_date = pd.to_datetime(args.enddate)

count = 0

# Loop through all the files in the folder
for file in os.listdir(args.dirin):
    # Check if the file is a CSV file
    if file.endswith(".csv"):
        # Increment the counter variable
        count += 1
        
        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv(os.path.join(args.dirin, file), delimiter='\t')
        df.info()
        


        # Combine the datetime columns into a single datetime object
        timestamp = [pd.Timestamp(int(row['YY']), int(row['MM']), int(row['DD']), int(row['HH']), int(row['MN'])) for i, row in df.iterrows()]

        # Convert the timestamp list to a DatetimeIndex object and set it as the new index
        df.index = pd.DatetimeIndex(timestamp)

        # Convert the DataFrame values to float
        df['Stat1'] = pd.to_numeric(df['Stat1'], errors='coerce') # convert any non-numeric values in the 'Stat1' column to NaN values
        df.info()
         # Print the number of NaN values per year
        nan_count = df['Stat1'].isna().groupby(df.index.year).sum()
        print('Number of NaN values per year are:',nan_count)

     # Resample the Stat1 column to a 10-minute frequency using mean for non-Precipitation files, and sum for Precipitation files
        if "Precipitation" or "disch" in file:
             df['Stat1'] = df['Stat1'].resample('10T').apply(lambda x: np.nan if x.isnull().sum() > 5 else x.sum())
             # Wenn mehr als 5 Werte NaN sind wird das Ergebnis auch NaN sein
        else:
            df['Stat1'] = df['Stat1'].resample('10T').mean()
     # ACHTUNG! Wenn ein NaN Value im Original vorhanden ist, so wird der neue Wert beim resampling auch weiterhin NaN sein! 

     # Round the 'Stat1' values to a certain number of decimal places (e.g., 2 decimal places)
        df['Stat1'] = df['Stat1'].round(3)
 
       # Define new index and the desired start and end date and frequency
        new_index = pd.date_range(start=start_date,end=end_date, freq='10T')

        # Reindex the DataFrame using the new index
        df = df.reindex(new_index)

        df['YY'] = df.index.year
        df['MM'] = df.index.month
        df['DD'] = df.index.day
        df['HH'] = df.index.hour
        df['MN'] = df.index.minute
        df.info()
        
        df = df.truncate(before=start_date, after=end_date)  # Truncate the data to the desired start and end dates
        # Reset the index and drop the timestamp column
        df.reset_index(drop=True, inplace=True)
        # Print the number of NaN values per year
        nan_count = df['Stat1'].isna().sum()
        print('Number of NaN in total are:',nan_count)


        ## # #####  create a header row CHANGE LAT, LONG & height FOR DIFFERENT STATIONS!#####################################
        # # header_row = pd.DataFrame([['YY', 'MM', 'DD', 'HH', 'MN', 'STATIONNAEME'], ['YY', 'MM', 'DD', 'HH', 'MN', 'height'], ['YY', 'MM', 'DD', 'HH', 'MN', 'LONGNITUDE'], ['YY', 'MM', 'DD', 'HH', 'MN', 'LATITUDE'], ['YY', 'MM', 'DD', 'HH', 'MN', 'Stat1']], columns=['YY', 'MM', 'DD', 'HH', 'MN', 'Stat1'])
        # # # concatenate the header row with the data frame
        # # df = pd.concat([header_row, df], ignore_index=True)

        new_file_name = os.path.splitext(file)[0] + "_10min.csv"
        df.to_csv(os.path.join(args.dirout, new_file_name), sep='\t', index=False)
        print("Saving:",new_file_name)

# Print the number of files found and converted
print("all", count, "files converted")