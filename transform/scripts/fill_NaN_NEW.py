import pandas as pd
import argparse 
import os

# Create the parser
parser = argparse.ArgumentParser()
parser.add_argument('--dir', type=str, help='The directory where the file is located', default="C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/GitHubMasterSkripts/MasterSkript/transform/output")
parser.add_argument('--df1', type=str, help='The Dataframe 1 ', default="ZAMG_RR_20131023T0000_20230402T2350NaN_Test.csv")
parser.add_argument('--freq1', type=str, help='The frequency for measurement in Dataframe 1', default="10T") 
parser.add_argument('--hight1', type=str, help='The Dataframe 1 hight ', default="2141")
parser.add_argument('--df2', type=str, help='The Dataframe 2 ', default= 'Precipitation_NaN_Test.csv')
parser.add_argument('--hight2', type=str, help='The Dataframe 2 hight ', default="2997")
parser.add_argument('--freq2', type=str, help='The frequency for measurement in Dataframe 1', default="1T") 
parser.add_argument('--freq', type=str, help='The frequency for the datetime index of the merged dataframe', default="10T")  # not working yet!
parser.add_argument('--lapsrate', type=str, help='The lapsrate that should be used')  
args = parser.parse_args()

# Get the base filename
file_name1 = os.path.basename(args.df1)
file_name2 = os.path.basename(args.df2)

# Build the full filepath from the directory and filename arguments
file_path1 = os.path.join(args.dir, args.df1)
file_path2 = os.path.join(args.dir, args.df2)

# Read in the CSV file
df1 = pd.read_csv(file_path1, sep='\t')
df2 = pd.read_csv(file_path2, sep='\t')


# set the date-time index for both dataframes
df1['datetime'] = pd.to_datetime(df1['YY'].astype(str) + '-' + df1['MM'].astype(str) + '-' + df1['DD'].astype(str) + ' ' + df1['HH'].astype(str) + ':' + df1['MN'].astype(str) + ':00')
df1 = df1.set_index('datetime')

df2['datetime'] = pd.to_datetime(df2['YY'].astype(str) + '-' + df2['MM'].astype(str) + '-' + df2['DD'].astype(str) + ' ' + df2['HH'].astype(str) + ':' + df2['MN'].astype(str) + ':00')
df2 = df2.set_index('datetime')

if args.freq1 != args.freq2:
    print("Warning: The measurement frequency of the two dataframes is different.")

    # Calculate the frequency ratio (for converting between the two dataframes)
    freq_ratio = int(args.freq1[:-1]) // int(args.freq2[:-1])
    print(f"Frequency ratio: {args.freq1} / {args.freq2} = {freq_ratio}")

# check which dataframe has higher frequency
if  args.freq1 > args.freq2:
    high_freq = df1
    low_freq = df2
    freq_ratio = int(args.freq1[:-1]) // int(args.freq2[:-1])
else:
    high_freq = df2
    low_freq = df1
    freq_ratio = int(args.freq2[:-1]) // int(args.freq1[:-1])


# resample the high-frequency dataframe to the frequency of the low-frequency dataframe, and fill NaN values using forward filling
high_freq = high_freq.resample(args.freq1).sum()

# create a new datetime index with the 10-minute intervals
high_freq.index = pd.date_range(high_freq.index[0].floor('10T'), high_freq.index[-1], freq=args.freq1)

# fill NaN values in the low-frequency dataframe with values from the high-frequency dataframe
if freq_ratio > 0:
    low_freq['Stat1'].fillna(high_freq['Stat1'].resample('1T').ffill().astype(float)/freq_ratio, inplace=True)
else:
    low_freq['Stat1'].fillna(high_freq['Stat1'].resample('1T').ffill().astype(float), inplace=True)

# save the filled dataframe as a CSV file
low_freq.to_csv(os.path.join(args.dir, f"filled_NEW{args.freq}{file_name1}"), sep='\t', index=False)
