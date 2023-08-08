import numpy as np
import pandas as pd
import argparse
import os
from termcolor import colored
from tqdm import tqdm


parser = argparse.ArgumentParser()
parser.add_argument('--dir', type=str, help='The directory where the file is located',
                    default="C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/GitHubMasterSkripts/MasterSkript/transform/output/WaSiM_Combined_files/WaSimfile_airtemp")
parser.add_argument('--df_low', type=str, help='The Dataframe Valley',
                    default="filled_df_low_short.csv")
parser.add_argument('--df_high', type=str, help='The Dataframe Peak',
                    default='filled_df_high_short.csv')
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

df_low = pd.read_csv(file_path_low, sep='\t')
df_high = pd.read_csv(file_path_high, sep='\t')

df_high['DateTime'] = df_high.apply((lambda x: transform_time_row(x)), axis=1)
df_high.set_index('DateTime', inplace=True)
print('Timestamps for df_high created')

df_low['DateTime'] = df_low.apply((lambda x: transform_time_row(x)), axis=1)
df_low.set_index('DateTime', inplace=True)
print('Timestamps for df_low created')

if len(df_low) != len(df_high) or df_low.first_valid_index() != df_high.first_valid_index():
    print("Error: Dataframes have different lengths. Please make sure both dataframes cover the same time period.")
    exit(1)

# method to generate tuple list consisting of all timestamps of all years matching the provides timestamp and
# have values in both dataframes and a tuple with both of these values
def get_tuples_for_same_timestamp(df_low, df_high, timestamp):
    # get date without time of the provided timestamp
    date_only = timestamp.date()

    # merge both dataframes
    merged_df = pd.merge(df_low, df_high, left_index=True, right_index=True, suffixes=('_low', '_high'))

    # remove all rows that do not match the exact date or have missing values
    result_df = merged_df[
        (merged_df.index.date != date_only) & pd.notna(merged_df['Stat1_low']) & pd.notna(merged_df['Stat1_high'])]

    # create tuple list and remove all rows that do not match the exact time
    result_list = result_df[result_df.index.time == timestamp.time()].reset_index()[
        ['DateTime', 'Stat1_low', 'Stat1_high']].values.tolist()
    return result_list

# Assuming both df_low and df_high have the same columns, you can concatenate them row-wise.
df_combined = pd.concat([df_low, df_high], axis=0)

# Optionally, you can sort the combined DataFrame by the index (DateTime) if required.
df_combined.sort_index(inplace=True)

# Group by the index (DateTime) and use the 'first' function to combine values for the same timestamp.
df_combined_grouped = df_combined.groupby('DateTime').first().reset_index()

# Drop the DateTime index column from the DataFrame.
df_combined_grouped = df_combined_grouped.drop(columns=['DateTime'])

# Save the merged DataFrame to a CSV file
output_filename = "merged_df.csv"
output_filepath = os.path.join(args.dir, output_filename)
df_combined_grouped.to_csv(output_filepath, sep='\t', index=False)

print(f"Merged DataFrame saved to {output_filepath}")

print("done")