import numpy as np
import pandas as pd
import argparse
import os
from termcolor import colored
from tqdm import tqdm


parser = argparse.ArgumentParser()
parser.add_argument('--dir', type=str, help='The directory where the file is located',
                    default="C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/GitHubMasterSkripts/MasterSkript/transform/output/convert_frequancy/10min_frequency_Neu/GH_filled/Humidity_LWD/cut")
parser.add_argument('--df_low', type=str, help='The Dataframe Valley',
                    default="lwd_Tirol_GH_1197091-LF-BasisganglinieNaN_10min_2022_cut_fill.csv")
parser.add_argument('--df_high', type=str, help='The Dataframe Peak',
                    default='filled_lwd_Tirol_JTH_15140917-LF-BasisganglinieNaN_cut.csv')
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


# method to calculate mean difference from tuple list
def calculate_mean_difference(tuples_list):
    if len(tuples_list) == 0:
        return 0
    diff_list = [t[2] - t[1] for t in tuples_list]
    mean_difference = sum(diff_list) / len(diff_list)
    return mean_difference


# method to fill values in df_high, will add mean difference
def fill_values_in_df_high(df_low_s, df_high_s):
    # Create a boolean mask for NaN values in 'Stat1' column in df_high
    nan_mask = df_high_s['Stat1'].isna()
    # Get the index positions of NaN values in df_high
    nan_indices = df_high_s.index[nan_mask]
    for index in tqdm(range(len(nan_indices)), desc="Filling df_high..."):
        tuples_list = get_tuples_for_same_timestamp(df_low_s, df_high_s, nan_indices[index])
        mean_diff = calculate_mean_difference(tuples_list)
        adjusted_value = df_low_s.loc[nan_indices[index], 'Stat1'] + mean_diff
        df_high_s.loc[nan_indices[index], 'Stat1'] = adjusted_value
    return df_high_s


# method to fill values in df_low, will subtract mean difference
def fill_values_in_df_low(df_low_s, df_high_s):
    nan_mask = df_low_s['Stat1'].isna()
    # Get the index positions of NaN values in df_low
    nan_indices = df_low_s.index[nan_mask]
    for index in tqdm(range(len(nan_indices)), desc="Filling df_low..."):
        tuples_list = get_tuples_for_same_timestamp(df_low_s, df_high_s, nan_indices[index])
        mean_diff = calculate_mean_difference(tuples_list)
        adjusted_value = df_high_s.loc[nan_indices[index], 'Stat1'] - mean_diff
        df_low_s.loc[nan_indices[index], 'Stat1'] = adjusted_value
    return df_low_s


# df_low = pd.DataFrame({
#     'Stat1': [17, 18, 16, np.NaN, 20],
#     'DateTime': pd.to_datetime(
#         ['2015-01-01 00:10', '2015-01-01 00:20', '2016-01-01 00:10', '2017-01-01 00:10', '2018-01-01 00:10'])
# })
#
# df_high = pd.DataFrame({
#     'Stat1': [13, 12, np.NaN, 15, 16],
#     'DateTime': pd.to_datetime(
#         ['2015-01-01 00:10', '2015-01-01 00:20', '2016-01-01 00:10', '2017-01-01 00:10', '2018-01-01 00:10'])
# })
#
# # set timestamps as indices for dataframes
# df_low.set_index('DateTime', inplace=True)
# df_high.set_index('DateTime', inplace=True)

# create a copy to avoid using calculated values to fill df_low
copy_df_high = df_high.copy()

# call methods to fill missing values for both dataframes
df_high = fill_values_in_df_high(df_low, df_high)
print('df_high filled')
df_low = fill_values_in_df_low(df_low, copy_df_high)
print('df_low filled')
# fill_values_in_df_low(df_low, copy_df_high)

# print both dataframes with filled values
print(df_high)
print(df_low)

df_low.to_csv(os.path.join(args.dir, f"filled_{file_name_low}"), sep='\t', index=False)
print(colored(" Dataframe 1 is filled and saved", "yellow"))

# save the filled dataframe as a CSV file
df_high.to_csv(os.path.join(args.dir, f"filled_{file_name_high}"), sep='\t', index=False)
# Print the number of NaN values per year
print(colored("Dataframe 2 is filled and saved", "yellow"))
