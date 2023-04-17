import pandas as pd
import argparse 
import os
from termcolor import colored

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
parser.add_argument('--dir', type=str, help='The directory where the file is located', default="C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/GitHubMasterSkripts/MasterSkript/transform/output")
parser.add_argument('--df1', type=str, help='The Dataframe 1. DF', default="hd_Precipitation_NaN_10minTest.csv")
parser.add_argument('--df2', type=str, help='The Dataframe 2 DF', default= 'ZAMG_Precipitation_NaN_10minTest.csv')
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
df2 = pd.read_csv(file_path2, sep='\t')
#df3 = pd.read_csv(file_path3, sep='\t')


# Set the date-time index for all dataframes
timestamp1 = [pd.Timestamp(int(row['YY']), int(row['MM']), int(row['DD']), int(row['HH']), int(row['MN'])) for i, row in df1.iterrows()]
# Convert the timestamp list to a DatetimeIndex object and set it as the new index
df1.index = pd.DatetimeIndex(timestamp1)

# Set the date-time index for all dataframes
timestamp2 = [pd.Timestamp(int(row['YY']), int(row['MM']), int(row['DD']), int(row['HH']), int(row['MN'])) for i, row in df2.iterrows()]
# Convert the timestamp list to a DatetimeIndex object and set it as the new index
df2.index = pd.DatetimeIndex(timestamp2)

# Combine the dataframes to fill in missing values in df1
combined_df1 = df1.combine_first(df2)
combined_df2 =df2.combine_first(df1)

# save the filled dataframe as a CSV file
combined_df1.to_csv(os.path.join(args.dir, f"filled_{file_name1}"), sep='\t', index=False)
print(colored(" Dataframe 1 is filled and saved", "yellow"))
# save the filled dataframe as a CSV file
combined_df2.to_csv(os.path.join(args.dir, f"filled_{file_name2}"), sep='\t', index=False)
print(colored("Dataframe 2 is filled and saved", "yellow"))


# filled_low_freq = fill_low_freq(low_freq, high_freq, freq_ratio, adj_factor)
# # save the filled dataframe as a CSV file
# filled_low_freq.to_csv(os.path.join(args.dir, f"filled_{file_name1}"), sep='\t', index=False)
# print(colored("Low-Frequency Dataframe is filled and saved", "yellow"))


# # ### Fill in high Frequencay DF #### WORKS!! 
# def fill_high_freq(low_freq, high_freq):
#     import pandas as pd

#     # create a new datetime index with 1-minute intervals
#     new_index = pd.date_range(low_freq.index[0], low_freq.index[-1], freq='1T')

#     # create a new DataFrame with the new index and fill it with NaN values
#     new_low_freq = pd.DataFrame(index=new_index, columns=low_freq.columns).fillna(method='ffill')

#     # update the values of the new DataFrame with values from the original low-frequency DataFrame
#     for i, row in low_freq.iterrows():
#         new_val = row['Stat1'] / 10
#         start_time = i
#         end_time = start_time + pd.Timedelta(minutes=10)
#         new_low_freq.loc[start_time:end_time, 'Stat1'] = new_val

#     # update the index of the new DataFrame to match the format of the original low-frequency DataFrame
#     new_low_freq['YY'] = new_low_freq.index.year
#     new_low_freq['MM'] = new_low_freq.index.month
#     new_low_freq['DD'] = new_low_freq.index.day
#     new_low_freq['HH'] = new_low_freq.index.hour
#     new_low_freq['MN'] = new_low_freq.index.minute

#     # fill NaN values in the high-frequency dataframe with values from the low-frequency dataframe
#     high_freq['Stat1'].fillna((new_low_freq['Stat1']/10).interpolate(method='time'), inplace=True)
#     # The interpolate() method uses linear interpolation to fill NaN values. By specifying the method='time' argument, it will interpolate based on the time index, so each minute will get the corresponding value of the other dataframe.
    
#     #####  create a header row CHANGE LAT, LONG & height FOR DIFFERENT STATIONS!#####################################
#     header_row = pd.DataFrame([['YY', 'MM', 'DD', 'HH', 'MN', 'STATIONNAEME'], ['YY', 'MM', 'DD', 'HH', 'MN', args.height2], ['YY', 'MM', 'DD', 'HH', 'MN', 'LONGNITUDE'], ['YY', 'MM', 'DD', 'HH', 'MN', 'LATITUDE'], ['YY', 'MM', 'DD', 'HH', 'MN', 'Stat1']], columns=['YY', 'MM', 'DD', 'HH', 'MN', 'Stat1'])

#     # concatenate the header row with the data frame
#     high_freq = pd.concat([header_row, high_freq], ignore_index=True)
#     return high_freq

# filled_high_freq = fill_high_freq(low_freq, high_freq)

# # save the filled dataframe as a CSV file
# filled_high_freq.to_csv(os.path.join(args.dir, f"filled_{file_name2}"), sep='\t', index=False)
# print(colored("High-Frequency Dataframe is filled and saved", "yellow"))