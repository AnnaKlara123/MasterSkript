import numpy as np
import pandas as pd
import argparse
import os
from termcolor import colored
from tqdm import tqdm


parser = argparse.ArgumentParser()
parser.add_argument('--dir', type=str, help='The directory where the file is located',
                    default="C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/GitHubMasterSkripts/MasterSkript/transform/output/WaSiM_Combined_files/WaSiM_Precipitaiton/")
parser.add_argument('--df_low', type=str, help='The Dataframe Valley',
                    default="filled_hd_Precipitation_NaN_10min.csv")
parser.add_argument('--df_high', type=str, help='The Dataframe Peak',
                    default='filled_ZAMG_Precipitation_NaN_cut.csv')
# parser.add_argument('--df3', type=str, help='The Dataframe 3 DF', default= 'ZAMG_Precipitation_NaN_10minTEST.csv')
# parser.add_argument('--lapsrate', type=str, help='The lapsrate that should be used. Use 1, if you want a 1:1 filling.', default= "6.5")
args = parser.parse_args()


def transform_time_row(row):
    # generate a pandas timestamp for resampling
    timestamp = pd.Timestamp(int(row['YY']), int(row['MM']), int(row['DD']), int(row['HH']), int(row['MN']))
    # create a pandas series
    # series = pd.Series(timestamp)
    return timestamp

# Get the base filename
file_name_low = os.path.basename(args.df_low)
file_name_high = os.path.basename(args.df_high)

# Build the full filepath from the directory and filename arguments
file_path_low = os.path.join(args.dir, args.df_low)
file_path_high = os.path.join(args.dir, args.df_high)


# Read the CSV files
df_low = pd.read_csv(file_path_low, sep='\t')
df_high = pd.read_csv(file_path_high, sep='\t')


# Merge the dataframes based on common timestamp columns
merged_df = pd.merge(df_low, df_high, on=['YY', 'MM', 'DD', 'HH', 'MN'])

# # Add a fictional column 'Stat4' filled with NaN values
# merged_df['Stat3'] = -9999
# # Add a fictional column 'Stat4' filled with NaN values
# merged_df['Stat4'] = -9999

# Round all numeric columns to 2 decimal places
merged_df = merged_df.round(2)
# Convert all NaN values to -9999
merged_df = merged_df.fillna(-9999)


# Save the merged DataFrame to a CSV file
output_filename = "multimerge_Airtemp.csv"
output_filepath = os.path.join(args.dir, output_filename)
merged_df.to_csv(output_filepath, sep='\t', index=False)

print(f"Merged DataFrame saved to {output_filepath}")

print("done")





