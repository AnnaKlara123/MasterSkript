import pandas as pd
import argparse 
import os
from termcolor import colored
from datetime import timedelta
from pandas import np

# # Create the parser
# parser = argparse.ArgumentParser()
# parser.add_argument('--dir', type=str, help='The directory where the file is located')
# parser.add_argument('--df1', type=str, help='The Dataframe 1. DF with lower frequency ')
# parser.add_argument('--height1', type=str, help='The height of the Station of Dataframe 1 in m. For example use "1587" for the Station in Galtuer')
# parser.add_argument('--df2', type=str, help='The Dataframe 2 DF with higher frequency')
# parser.add_argument('--height2', type=str, help='The height f the Station of Dataframe 1 in m.')
# parser.add_argument('--lapsrate', type=str, help='The lapsrate that should be used. Use 1, if you do not want to use a lapsrate.')  
# args = parser.parse_args()

parser = argparse.ArgumentParser()
parser.add_argument('--dir', type=str, help='The directory where the file is located', default="C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/GitHubMasterSkripts/MasterSkript/transform/output/convert_frequancy/20.4Testdatasets")
parser.add_argument('--df1', type=str, help='The Dataframe 1. DF', default="hd_Windspeed_NaN_10minTest.csv")
parser.add_argument('--df2', type=str, help='The Dataframe 2 DF', default= 'lwd_Tirol_GH_1197091-WG-BasisganglinieNaN_10minTest.csv')
#parser.add_argument('--df3', type=str, help='The Dataframe 3 DF', default= 'ZAMG_Precipitation_NaN_10minTEST.csv')
#parser.add_argument('--lapsrate', type=str, help='The lapsrate that should be used. Use 1, if you want a 1:1 filling.', default= "6.5")  
args = parser.parse_args()

# Get the base filename
file_name1 = os.path.basename(args.df1)
file_name2 = os.path.basename(args.df2)
#file_name3 = os.path.basename(args.df3)

# Build the full filepath from the directory and filename arguments
file_path1 = os.path.join(args.dir, args.df1)
file_path2 = os.path.join(args.dir, args.df2)
#file_path3 = os.path.join(args.dir, args.df3)

# Read in the CSV file
df1 = pd.read_csv(file_path1, sep='\t')
#df1.info()
df2 = pd.read_csv(file_path2, sep='\t')
#df2.info()
#df3 = pd.read_csv(file_path3, sep='\t')


# Set the date-time index for all dataframes
timestamp1 = [pd.Timestamp(int(row['YY']), int(row['MM']), int(row['DD']), int(row['HH']), int(row['MN'])) for i, row in df1.iterrows()]
# Convert the timestamp list to a DatetimeIndex object and set it as the new index
df1.index = pd.DatetimeIndex(timestamp1)

# Set the date-time index for all dataframes
timestamp2 = [pd.Timestamp(int(row['YY']), int(row['MM']), int(row['DD']), int(row['HH']), int(row['MN'])) for i, row in df2.iterrows()]
# Convert the timestamp list to a DatetimeIndex object and set it as the new index
df2.index = pd.DatetimeIndex(timestamp2)

################# Filling 1:1 #########################################
# # Combine the dataframes to fill in missing values in df1
# combined_df1 = df1.combine_first(df2)
# combined_df2 = df2.combine_first(df1)

# # Count the number of NaNs before and after filling
# nans_before_fill_df1 = df1.isna().sum().sum()
# nans_after_fill_df1 = combined_df1.isna().sum().sum()
# nans_before_fill_df2 = df2.isna().sum().sum()
# nans_after_fill_df2 = combined_df2.isna().sum().sum()

# # save the filled dataframe as a CSV file
# combined_df1.to_csv(os.path.join(args.dir, f"filled_{file_name1}"), sep='\t', index=False)
# print(colored(f"Dataframe 1 is filled and saved. NaNs before: {nans_before_fill_df1}, after: {nans_after_fill_df1}", "yellow"))

# # save the filled dataframe as a CSV file
# combined_df2.to_csv(os.path.join(args.dir, f"filled_{file_name2}"), sep='\t', index=False)
# print(colored(f"Dataframe 2 is filled and saved. NaNs before: {nans_before_fill_df2}, after: {nans_after_fill_df2}", "yellow"))

################# Filling t-1 ####################################################

# Fill NaN values using the difference calculation in df1
for col in df1.columns:
    for i, val in df1[col].items():
        if pd.isna(val):
            # Check if the timestamps exist in both dataframes
            if i - pd.Timedelta(minutes=10) in df1.index and i + pd.Timedelta(minutes=10) in df2.index:
                diff = (df1.loc[i - pd.Timedelta(minutes=10), col]) - (df2.loc[i - pd.Timedelta(minutes=10), col])
                if diff < 0:
                    df1.loc[i, col] = df2.loc[i, col] - np.abs(diff)
                else:
                    df1.loc[i, col] = df2.loc[i, col] + np.abs(diff)
                 # Ensure that the value is not negative
                if df1.loc[i, col] < 0:
                    df1.loc[i, col] = 0    

# Fill NaN values using the difference calculation in df2
for col in df2.columns:
    for i, val in df2[col].items():
        if pd.isna(val):
            # Check if the timestamps exist in both dataframes
            if i - pd.Timedelta(minutes=10) in df2.index and i - pd.Timedelta(minutes=10) in df1.index:
                diff = df2.loc[i - pd.Timedelta(minutes=10), col] - df1.loc[i - pd.Timedelta(minutes=10), col]
                if diff < 0:
                    df2.loc[i, col] = df1.loc[i, col] + np.abs(diff)
                else:
                    df2.loc[i, col] = df1.loc[i, col]  + np.abs(diff)
                # Ensure that the value is not negative
                if df2.loc[i, col] < 0:
                    df2.loc[i, col] = 0


# save the filled dataframe as a CSV file
df1.to_csv(os.path.join(args.dir, f"filled_{file_name1}"), sep='\t', index=False)
print(colored(" Dataframe 1 is filled and saved", "yellow"))

# save the filled dataframe as a CSV file
df2.to_csv(os.path.join(args.dir, f"filled_{file_name2}"), sep='\t', index=False)
print(colored("Dataframe 2 is filled and saved", "yellow"))
##############################################################################################

