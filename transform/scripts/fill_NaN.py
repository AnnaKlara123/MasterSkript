# import pandas as pd
# import argparse 
# import os

# # Create the parser
# parser = argparse.ArgumentParser()
# parser.add_argument('--dir', type=str, help='The directory where the file is located', default="C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/GitHubMasterSkripts/MasterSkript/transform/output")
# parser.add_argument('--df1', type=str, help='The Dataframe 1 ', default="Airtemp_nan.csv")
# parser.add_argument('--hight1', type=str, help='The Dataframe 1 hight ', default="2141")
# parser.add_argument('--df2', type=str, help='The Dataframe 2 ', default= 'lwd_Tirol_1197091-LT-BasisganglinieNaN.csv')
# parser.add_argument('--hight2', type=str, help='The Dataframe 2 hight ', default="2997")
# parser.add_argument('--freq', type=str, help='The frequency for the datetime index of the merged dataframe', default="5T")  # not working yet!
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

# # # Create a new dataframe with a datetime index that spans the entire time range
# # idx = pd.date_range(start=min(dfhyd.index.min(), dflwd.index.min()), end=max(dfhyd.index.max(), dflwd.index.max()), freq=args.freq)
# # merged_df = pd.DataFrame(index=idx)
# # Create a new dataframe with a datetime index that spans the entire time range
# start_date = max(dfhyd.index.min(), dflwd.index.min())
# end_date = max(dfhyd.index.max(), dflwd.index.max())
# idx = pd.date_range(start=start_date, end=end_date, freq=args.freq)
# merged_df = pd.DataFrame(index=idx)


# # # Fill NaN values in dfhyd with values from dflwd
# # dfhyd_filled = dfhyd.combine_first(dflwd)
# # # Fill NaN values in dflwd with values from dfhyd
# # dflwd_filled = dflwd.combine_first(dfhyd)

# # Calculate the altitude difference between the two stations
# alt_diff = int(args.hight2) - int(args.hight1)

# # Calculate the lapse rate adjustment factor
# lapse_rate = 6.5  # degrees per 1000m
# adj_factor = 1 - (lapse_rate * alt_diff / 1000)

# # Fill NaN values in dfhyd with values from dflwd, adjusted for lapse rate
# dfhyd_filled = dfhyd.combine_first(dflwd * adj_factor)

# # Fill NaN values in dflwd with values from dfhyd, adjusted for lapse rate
# dflwd_filled = dflwd.combine_first(dfhyd * adj_factor)

# # Save the filled dfhyd to a new CSV file
# dfhyd_filled.to_csv(os.path.join(args.dir, f"filled_LR{args.freq}{file_namehyd}"), sep='\t', index=False)
# dflwd_filled.to_csv(os.path.join(args.dir, f"filled_LR{args.freq}{file_nameldw}"), sep='\t', index=False)


##################################################################################################################
import pandas as pd
import argparse 
import os

# Create the parser
parser = argparse.ArgumentParser()
parser.add_argument('--dir', type=str, help='The directory where the file is located', default="C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/GitHubMasterSkripts/MasterSkript/transform/output")
parser.add_argument('--df1', type=str, help='The Dataframe 1 ', default="Airtemp_nanTEST.csv")
parser.add_argument('--hight1', type=str, help='The Dataframe 1 hight ', default="2141")
parser.add_argument('--df2', type=str, help='The Dataframe 2 ', default= 'lwd_Tirol_1197091-LT-BasisganglinieNaN_Test.csv')
parser.add_argument('--hight2', type=str, help='The Dataframe 2 hight ', default="2997")
parser.add_argument('--freq', type=str, help='The frequency for the datetime index of the merged dataframe', default="5T")  # not working yet!
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
start_date = max(dfhyd.index.min(), dflwd.index.min())
end_date = max(dfhyd.index.max(), dflwd.index.max())
idx = pd.date_range(start=start_date, end=end_date, freq=args.freq)
merged_df = pd.DataFrame(index=idx)


# Calculate the altitude difference between the two stations
alt_diff = int(args.hight2) - int(args.hight1)

# Calculate the lapse rate adjustment factor
lapse_rate = 6.5  # degrees per 1000m
adj_factor = 1 - (lapse_rate * alt_diff / 1000)
print (adj_factor, "aF")

# Fill NaN values in dfhyd with values from dflwd, adjusted for lapse rate (only for "Stat1" column)
dfhyd_stat1 = dfhyd["Stat1"].combine_first(dflwd["Stat1"] - adj_factor)
dfhyd_filled = dfhyd.copy()  # create a copy of the original dataframe
dfhyd_filled["Stat1"] = dfhyd_stat1  # replace the "Stat1" column with the adjusted values

# Fill NaN values in dflwd with values from dfhyd, adjusted for lapse rate (only for "Stat1" column)
dflwd_stat1 = dflwd["Stat1"].combine_first(dfhyd["Stat1"] + adj_factor)
dflwd_filled = dflwd.copy()  # create a copy of the original dataframe
dflwd_filled["Stat1"] = dflwd_stat1  # replace the "Stat1" column with the adjusted values


# Save the filled dfhyd to a new CSV file
dfhyd_filled.to_csv(os.path.join(args.dir, f"filled_LR{args.freq}{file_namehyd}"), sep='\t', index=False)
dflwd_filled.to_csv(os.path.join(args.dir, f"filled_LR{args.freq}{file_nameldw}"), sep='\t', index=False)

