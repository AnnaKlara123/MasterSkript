import pandas as pd
import argparse 
import os

# Create the parser
parser = argparse.ArgumentParser()
parser.add_argument('--dir', type=str, help='The directory where the file is located', default="C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/GitHubMasterSkripts/MasterSkript/transform/output")
parser.add_argument('--df1', type=str, help='The Dataframe 1 ', default="197091_GS_CmdNaN_test.csv")
parser.add_argument('--df2', type=str, help='The Dataframe 2 ', default= 'lwd_Tirol_15140917-GS-BasisganglinieNaN_test.csv')
parser.add_argument('--freq', type=str, help='The frequency for the datetime index of the merged dataframe', default="10T")
args = parser.parse_args()

# Get the base filename
file_namehyd = os.path.basename(args.df1)
file_nameldw = os.path.basename(args.df2)

# Build the full filepath from the directory and filename arguments
file_pathhyd = os.path.join(args.dir, args.df1)
file_pathlwd = os.path.join(args.dir, args.df2)

# Read in the CSV file
dfhyd = pd.read_csv(file_pathhyd, sep='\t')
dflwd = pd.read_csv(file_pathlwd, sep='\t')

# Combine the datetime columns into a single datetime object
dateshyd = [pd.Timestamp(int(row['YY']), int(row['MM']), int(row['DD']), int(row['HH']), int(row['MN'])) for i, row in dfhyd.iterrows()]
dateslwd = [pd.Timestamp(int(row['YY']), int(row['MM']), int(row['DD']), int(row['HH']), int(row['MN'])) for i, row in dflwd.iterrows()]

# Set the datetime index for the dataframe
dfhyd.index = dateshyd
dflwd.index = dateslwd

# Create a new dataframe with a datetime index that spans the entire time range
idx = pd.date_range(start=min(dfhyd.index.min(), dflwd.index.min()), end=max(dfhyd.index.max(), dflwd.index.max()), freq=args.freq)
merged_df = pd.DataFrame(index=idx)

# Fill NaN values in dfhyd with values from dflwd
dfhyd_filled = dfhyd.combine_first(dflwd)
# Fill NaN values in dflwd with values from dfhyd
dflwd_filled = dflwd.combine_first(dfhyd)

# Save the filled dfhyd to a new CSV file
dfhyd_filled.to_csv(os.path.join(args.dir, f"filled_{args.freq}{file_namehyd}"), sep='\t', index=False)
# Save the filled dfhyd to a new CSV file
dflwd_filled.to_csv(os.path.join(args.dir, f"filled_{args.freq}{file_nameldw}"), sep='\t', index=False)


##################################################################################################################
# import pandas as pd
# import argparse 
# import os

# # Create the parser
# parser = argparse.ArgumentParser()
# parser.add_argument('--dir', type=str, help='The directory where the file is located', default="C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/GitHubMasterSkripts/MasterSkript/transform/output")
# parser.add_argument('--df1', type=str, help='The Dataframe 1 ', default="197091_GS_CmdNaN_test.csv")
# parser.add_argument('--df1_freq', type=str, help='The frequency of Dataframe 1', default="5T")
# parser.add_argument('--df2', type=str, help='The Dataframe 2 ', default= 'lwd_Tirol_15140917-GS-BasisganglinieNaN_test.csv')
# parser.add_argument('--df2_freq', type=str, help='The frequency of Dataframe 2', default="10T")
# parser.add_argument('--freq', type=str, help='The frequency for the datetime index of the merged dataframe', default="10T")
# args = parser.parse_args()

# # Get the base filename
# file_namehyd = os.path.basename(args.df1)
# file_nameldw = os.path.basename(args.df2)

# # Build the full filepath from the directory and filename arguments
# file_pathhyd = os.path.join(args.dir, args.df1)
# file_pathlwd = os.path.join(args.dir, args.df2)

# # Read in the CSV file
# dfhyd = pd.read_csv(file_pathhyd, sep='\t')
# dflwd = pd.read_csv(file_pathlwd, sep='\t')

# # Combine the datetime columns into a single datetime object
# dateshyd = [pd.Timestamp(int(row['YY']), int(row['MM']), int(row['DD']), int(row['HH']), int(row['MN'])) for i, row in dfhyd.iterrows()]
# dateslwd = [pd.Timestamp(int(row['YY']), int(row['MM']), int(row['DD']), int(row['HH']), int(row['MN'])) for i, row in dflwd.iterrows()]

# # Set the datetime index for the dataframe
# dfhyd.index = dateshyd
# dflwd.index = dateslwd

# # Resample the dataframes to the desired frequency
# dfhyd_resampled = dfhyd.resample(args.df1_freq).ffill().resample(args.freq).ffill()
# dflwd_resampled = dflwd.resample(args.df2_freq).ffill().resample(args.freq).ffill()

# # Create a new dataframe with a datetime index that spans the entire time range
# idx = pd.date_range(start=min(dfhyd.index.min(), dflwd.index.min()), end=max(dfhyd.index.max(), dflwd.index.max()), freq=args.freq)
# merged_df = pd.DataFrame(index=idx)

# # Fill NaN values in dfhyd with values from dflwd
# dfhyd_filled = dfhyd_resampled.combine_first(dflwd_resampled)
# # Fill NaN values in dflwd with values from dfhyd
# dflwd_filled = dflwd_resampled.combine_first(dfhyd_resampled)


# # Save the filled dfhyd to a new CSV file
# dfhyd_filled.to_csv(os.path.join(args.dir, f"filled_{args.freq}{file_namehyd}"), sep='\t', index=False)
# # Save the filled dfhyd to a new CSV file
# dflwd_filled.to_csv(os.path.join(args.dir, f"filled_{args.freq}{file_nameldw}"), sep='\t', index=False)
