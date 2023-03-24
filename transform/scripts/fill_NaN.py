# import pandas as pd
# import argparse 
# import os

# # Create the parser
# parser = argparse.ArgumentParser()
# parser.add_argument('--dir', type=str, help='The directory where the file is located', default="C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/GitHubMasterSkripts/MasterSkript/transform/output")
# parser.add_argument('--df1', type=str, help='The Dataframe 1 ', default="Globalradiation_NaN_test.csv")
# parser.add_argument('--df2', type=str, help='The Dataframe 2 ', default= 'lwd_Tirol_15140917-GS-BasisganglinieNaN_test.csv')
# parser.add_argument('--mearge method', type=int, help='The method of mearging')
# args = parser.parse_args()

# # Get the base filename
# file_name1 = os.path.basename(args.df1)
# file_name2 = os.path.basename(args.df2)

# # Build the full filepath from the directory and filename arguments
# file_path1 = os.path.join(args.dir, args.df1)
# file_path2 = os.path.join(args.dir, args.df2)

# # Read in the CSV file
# df1 = pd.read_csv(file_path1, sep='\t', skiprows=4)
# # Read in the CSV file
# df2 = pd.read_csv(file_path2, sep='\t',  skiprows=5)

# # Combine the datetime columns into a single datetime object
# dates1 = [pd.Timestamp(int(row['YY']), int(row['MM']), int(row['DD']), int(row['HH']), int(row['MN'])) for i, row in df1.iterrows()]
# dates2 = [pd.Timestamp(int(row['YY']), int(row['MM']), int(row['DD']), int(row['HH']), int(row['MN'])) for i, row in df2.iterrows()]

# # Set the datetime index for the dataframe
# df1.index = dates1
# df2.index = dates2

# # merge two dataframes on index
# merged_df = pd.concat([df1, df2], axis=1)

# # sort by datetime index
# merged_df.sort_index(inplace=True)

# # fill NaN values using forward fill and backward fill
# merged_df.fillna(method='ffill', inplace=True)
# merged_df.fillna(method='bfill', inplace=True)

# # split merged dataframe into two separate dataframes
# df1_filled = merged_df.loc[df1.index]
# df2_filled = merged_df.loc[df2.index]

import pandas as pd
import argparse 
import os

# Create the parser
parser = argparse.ArgumentParser()
parser.add_argument('--dir', type=str, help='The directory where the file is located', default="C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/GitHubMasterSkripts/MasterSkript/transform/output")
parser.add_argument('--df1', type=str, help='The Dataframe 1 ', default="197091_GS_CmdNaN_test.csv")
parser.add_argument('--df2', type=str, help='The Dataframe 2 ', default= 'lwd_Tirol_15140917-GS-BasisganglinieNaN_test.csv')
parser.add_argument('--mearge method', type=int, help='The method of mearging')
args = parser.parse_args()

# Get the base filename
file_namehyd = os.path.basename(args.df1)
file_name2ldw = os.path.basename(args.df2)

# Build the full filepath from the directory and filename arguments
file_pathhyd = os.path.join(args.dir, args.df1)
file_pathlwd = os.path.join(args.dir, args.df2)

# Read in the CSV file
dfhyd = pd.read_csv(file_pathhyd, sep='\t')
# Read in the CSV file
dflwd = pd.read_csv(file_pathlwd, sep='\t')

# Combine the datetime columns into a single datetime object
dateshyd = [pd.Timestamp(int(row['YY']), int(row['MM']), int(row['DD']), int(row['HH']), int(row['MN'])) for i, row in dfhyd.iterrows()]
dateslwd = [pd.Timestamp(int(row['YY']), int(row['MM']), int(row['DD']), int(row['HH']), int(row['MN'])) for i, row in dflwd.iterrows()]

# Set the datetime index for the dataframe
dfhyd.index = dateshyd
dflwd.index = dateslwd

# Create a new dataframe with a datetime index that spans the entire time range
idx = pd.date_range(start=min(dfhyd.index.min(), dflwd.index.min()), end=max(dfhyd.index.max(), dflwd.index.max()), freq='5T')
merged_df = pd.DataFrame(index=idx)

# Fill NaN values in dfhyd with values from dflwd
dfhyd_filled = dfhyd.combine_first(dflwd)

# Save the filled dfhyd to a new CSV file
dfhyd_filled.to_csv(os.path.join(args.dir, f"filled_{file_namehyd}"), sep='\t', index=True)






# # Resample the two dataframes to 5 minute frequency
# dfhyd_resampled = df1.resample('5T').mean()
# dflwd_resampled = df2.resample('5T').mean()

# # Reindex the two dataframes to align the time columns
# dfhyd_aligned = dfhyd_resampled.reindex(merged_df.index, method='ffill')
# dflwd_aligned = dflwd_resampled.reindex(merged_df.index, method='ffill')

# # merge two dataframes on index
# merged_df = pd.concat([dfhyd_aligned, dflwd_aligned], axis=1)

# # fill NaN values using forward fill and backward fill
# merged_df.fillna(method='ffill', inplace=True)
# merged_df.fillna(method='bfill', inplace=True)

# # split merged dataframe into two separate dataframes
# dfhyd_filled = merged_df.iloc[:, :5]
# dflwd_filled = merged_df.iloc[:, 5:]
