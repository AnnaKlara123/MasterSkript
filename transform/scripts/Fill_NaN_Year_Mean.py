import numpy as np
import pandas as pd
import argparse
import os
from termcolor import colored

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


# Get the base filename
file_name_low = os.path.basename(args.df_low)
file_name_high = os.path.basename(args.df_high)


# Build the full filepath from the directory and filename arguments
file_path_low = os.path.join(args.dir, args.df_low)
file_path_high = os.path.join(args.dir, args.df_high)

df_low = pd.read_csv(file_path_low, sep='\t')
df_high = pd.read_csv(file_path_high, sep='\t')

timestamp_low = [pd.Timestamp(int(row['YY']), int(row['MM']), int(row['DD']), int(row['HH']), int(row['MN'])) for i, row in
              df_low.iterrows()]
# Convert the timestamp list to a DatetimeIndex object and set it as the new index
df_low.index = pd.DatetimeIndex(timestamp_low)


# Set the date-time index for all dataframes
timestamp_high = [pd.Timestamp(int(row['YY']), int(row['MM']), int(row['DD']), int(row['HH']), int(row['MN'])) for i, row in
              df_high.iterrows()]
# Convert the timestamp list to a DatetimeIndex object and set it as the new index
df_high.index = pd.DatetimeIndex(timestamp_high)
df_high.index.name='DateTime'
df_low.index.name='DateTime'
print(df_high)

if len(df_low) != len(df_high) or timestamp_low[0] != timestamp_high[0]:
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
    result_df = merged_df[(merged_df.index.date != date_only) & pd.notna(merged_df['Stat1_low']) & pd.notna(merged_df['Stat1_high'])]

    # create tuple list and remove all rows that do not match the exact time
    result_list = result_df[result_df.index.time == timestamp.time()].reset_index()[['DateTime', 'Stat1_low', 'Stat1_high']].values.tolist()
    return result_list


# method to calculate mean difference from tuple list
def calculate_mean_difference(tuples_list):
    if len(tuples_list) == 0:
        return 0
    diff_list = [t[2] - t[1] for t in tuples_list]
    mean_difference = sum(diff_list) / len(diff_list)
    return mean_difference


# method to fill values in df_low, will add mean difference
def fill_values_in_df_high(df_low, df_high):
    for index, row in df_high.iterrows():
        if pd.isna(row['Stat1']):
            selected_timestamp = index
            tuples_list = get_tuples_for_same_timestamp(df_low, df_high, selected_timestamp)
            mean_diff = calculate_mean_difference(tuples_list)
            adjusted_value = df_low.loc[selected_timestamp, 'Stat1'] + mean_diff
            df_high.loc[index, 'Stat1'] = adjusted_value


# method to fill values in df_low, will subtract mean difference
def fill_values_in_df_low(df_low, df_high):
    for index, row in df_low.iterrows():
        if pd.isna(row['Stat1']):
            selected_timestamp = index
            tuples_list = get_tuples_for_same_timestamp(df_low, df_high, selected_timestamp)
            mean_diff = calculate_mean_difference(tuples_list)
            adjusted_value = df_high.loc[selected_timestamp, 'Stat1'] - mean_diff
            df_low.loc[index, 'Stat1'] = adjusted_value



# df_low = pd.DataFrame({
#     'Stat1': [17, 18, 16, np.NaN, 20],
#     'DateTime': pd.to_datetime(['2015-01-01 00:10', '2015-01-01 00:20', '2016-01-01 00:10', '2017-01-01 00:10', '2018-01-01 00:10'])
# })
#
# df_high = pd.DataFrame({
#     'Stat1': [13, 12, np.NaN, 15, 16],
#     'DateTime': pd.to_datetime(['2015-01-01 00:10', '2015-01-01 00:20', '2016-01-01 00:10', '2017-01-01 00:10', '2018-01-01 00:10'])
# })

# set timestamps as indices for dataframes
# df_low.set_index('DateTime', inplace=True)
# df_high.set_index('DateTime', inplace=True)

# create a copy to avoid using calculated values to fill df_low
copy_df_high = df_high.copy()

# call methods to fill missing values for both dataframes
fill_values_in_df_high(df_low, df_high)
fill_values_in_df_low(df_low, copy_df_high)

# print both dataframes with filled values
print(df_high)
print(df_low)

df_low.to_csv(os.path.join(args.dir, f"filled_{file_name_low}"), sep='\t', index=False)
print(colored(" Dataframe 1 is filled and saved", "yellow"))


# save the filled dataframe as a CSV file
df_high.to_csv(os.path.join(args.dir, f"filled_{file_name_high}"), sep='\t', index=False)
# Print the number of NaN values per year
print(colored("Dataframe 2 is filled and saved", "yellow"))
