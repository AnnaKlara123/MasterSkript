import pandas as pd
import argparse 
import os
from termcolor import colored

# Create the parser
parser = argparse.ArgumentParser()
parser.add_argument('--dir', type=str, help='The directory where the file is located', default="C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/GitHubMasterSkripts/MasterSkript/transform/output")
parser.add_argument('--df1', type=str, help='The Dataframe 1. DF with lower frequency ', default="ZAMG_RR_20131023T0000_20230402T2350NaN_Test.csv")
parser.add_argument('--hight1', type=str, help='The Dataframe 1 hight ', default="2141")
parser.add_argument('--df2', type=str, help='The Dataframe 2 DF with higher frequency', default= 'Precipitation_NaN_Test.csv')
parser.add_argument('--hight2', type=str, help='The Dataframe 2 hight ', default="2997")
parser.add_argument('--lapsrate', type=str, help='The lapsrate that should be used. Use 1, if you want a 1:1 filling.')  
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
freq1 = pd.infer_freq(df1.index)
if freq1 == 'T':
    freq1 = '1T'

df2['datetime'] = pd.to_datetime(df2['YY'].astype(str) + '-' + df2['MM'].astype(str) + '-' + df2['DD'].astype(str) + ' ' + df2['HH'].astype(str) + ':' + df2['MN'].astype(str) + ':00')
df2 = df2.set_index('datetime')
freq2= pd.infer_freq(df2.index)
if freq2 == 'T':
    freq2 = '1T'
print(f'frequcanies are:{freq1} and {freq2}')

if freq1 != freq2:
    print(colored("Warning: The measurement frequency of the two dataframes is different.", "yellow"))


    # Calculate the frequency ratio (for converting between the two dataframes)
    freq_ratio = int(freq1[:-1]) // int(freq2[:-1])
    print(colored("Frequency ratio:", "yellow"), colored(f"{freq1} / {freq2} = {freq_ratio}", "blue"))

# check which dataframe has higher frequency
if  freq1 > freq2:
    high_freq = df1
    low_freq = df2
    freq_ratio = int(freq1[:-1]) // int(freq2[:-1])
else: # 0 = freq_ration because no calculation is needed as the high freq. Value stays the same 
    high_freq = df2
    low_freq = df1
    freq_ratio = int(freq2[:-1]) // int(freq1[:-1])

#### Fill in low Frequencay DF #### WORKS!! 
# # resample the high-frequency dataframe to the frequency of the low-frequency dataframe, and fill NaN values using forward filling
# high_freq = high_freq.resample(freq1).sum()

# # create a new datetime index with the 10-minute intervals
# high_freq.index = pd.date_range(high_freq.index[0].floor('10T'), high_freq.index[-1], freq=args.freq1)

# # update the index of the new DataFrame to match the format of the original low-frequency DataFrame
# high_freq['YY'] = high_freq.index.year
# high_freq['MM'] = high_freq.index.month
# high_freq['DD'] = high_freq.index.day
# high_freq['HH'] = high_freq.index.hour
# high_freq['MN'] = high_freq.index.minute


# # fill NaN values in the low-frequency dataframe with values from the high-frequency dataframe
# if freq_ratio > 0:
#     low_freq['Stat1'].fillna(high_freq['Stat1'].resample('1T').ffill().astype(float)/freq_ratio, inplace=True)
# else:
#     low_freq['Stat1'].fillna(high_freq['Stat1'].resample('1T').ffill().astype(float), inplace=True)

# # save the filled dataframe as a CSV file
# low_freq.to_csv(os.path.join(args.dir, f"filled_NEW{args.freq}{file_name1}"), sep='\t', index=False)
# print(colored("Low-Frequancy Dataframe is filled and saved", "yellow"))

###########################################################################################################################

# create a new datetime index with 1-minute intervals
new_index = pd.date_range(low_freq.index[0], low_freq.index[-1], freq='1T')

# create a new DataFrame with the new index and fill it with NaN values
new_low_freq = pd.DataFrame(index=new_index, columns=low_freq.columns).fillna(method='ffill')

# update the values of the new DataFrame with values from the original low-frequency DataFrame
for i, row in low_freq.iterrows():
    new_val = row['Stat1'] / 10
    start_time = i
    end_time = start_time + pd.Timedelta(minutes=10)
    new_low_freq.loc[start_time:end_time, 'Stat1'] = new_val

# update the index of the new DataFrame to match the format of the original low-frequency DataFrame
new_low_freq['YY'] = new_low_freq.index.year
new_low_freq['MM'] = new_low_freq.index.month
new_low_freq['DD'] = new_low_freq.index.day
new_low_freq['HH'] = new_low_freq.index.hour
new_low_freq['MN'] = new_low_freq.index.minute

# fill NaN values in the high-frequency dataframe with values from the low-frequency dataframe
high_freq['Stat1'].fillna((new_low_freq['Stat1']/10).interpolate(method='time'), inplace=True)
# The interpolate() method uses linear interpolation to fill NaN values. By specifying the method='time' argument, it will interpolate based on the time index, so each minute will get the corresponding value of the other dataframe.


# save the filled dataframe as a CSV file
high_freq.to_csv(os.path.join(args.dir, f"filled_NEW{file_name2}"), sep='\t', index=False)
print(colored("High-Frequancy Dataframe is filled and saved", "yellow"))
