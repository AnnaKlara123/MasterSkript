import pandas as pd
import os
import numpy as np

######################## Read in file ########################################################################
# set the file path
file_path = "C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/GitHubMasterSkripts/MasterSkript/transform/input/ZAMG_RR_20131023T0000_20230402T2350TEST.csv"

# extract the filename without the extension
filename = os.path.splitext(os.path.basename(file_path))[0]

# read in the data as a pandas dataframe
df = pd.read_csv(file_path, delimiter="," , names=["time", "station", "RR"], header=0)

# extract year, month, day, hour, and minute from time column
df["YY"] = pd.to_datetime(df["time"], format="%Y-%m-%dT%H:%M:%S%z").dt.strftime("%Y")
df["MM"] = pd.to_datetime(df["time"], format="%Y-%m-%dT%H:%M:%S%z").dt.strftime("%m")
df["DD"] = pd.to_datetime(df["time"], format="%Y-%m-%dT%H:%M:%S%z").dt.strftime("%d")
df["HH"] = pd.to_datetime(df["time"], format="%Y-%m-%dT%H:%M:%S%z").dt.strftime("%H")
df["MN"] = pd.to_datetime(df["time"], format="%Y-%m-%dT%H:%M:%S%z").dt.strftime("%M")

# drop original time column
df = df.drop(["time"], axis=1)
df = df.drop(["station"], axis=1)
df = df.drop(["index"], axis=1)
######################## NaN Replacement & Exclude of irrational Values ################################

# format the value column as required
df["RR"] = df["RR"].astype(str).str.replace(",", ".")

# replace missing values represented as "---" with NaN
df["RR"] = pd.to_numeric(df["RR"], errors="coerce")

# replace all NaN values with -9999 TUNR ON IF -9999 is wished! 
df["RR"].fillna(-9999, inplace=True)

################################ Format the DF for the WaSiM output################################
# rename RR column to Stat1
df = df.rename(columns={"RR": "Stat1"})

#####  create a header row CHANGE LAT, LONG & HIGHT FOR DIFFERENT STATIONS!#####################################
header_row = pd.DataFrame([['YY', 'MM', 'DD', 'HH', 'MN', 'ZAMG Galtuer'], ['YY', 'MM', 'DD', 'HH', 'MN', '1587'], ['YY', 'MM', 'DD', 'HH', 'MN', '46.968056'], ['YY', 'MM', 'DD', 'HH', 'MN', '10.185555'], ['YY', 'MM', 'DD', 'HH', 'MN', 'Stat1']], columns=['YY', 'MM', 'DD', 'HH', 'MN', 'Stat1'])

# concatenate the header row with the data frame
df = pd.concat([header_row, df], ignore_index=True)


#################### Save Files ################################################################################
# set the file path for saving the CSV file
csv_path = f"C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/GitHubMasterSkripts/MasterSkript/transform/output/{filename}NaN.csv"

# save the new dataframe as a CSV file
df.to_csv(csv_path,sep='\t', index=False)

# set the file path for saving the output.txt file
output_path = f"{filename}.txt"

# save the dataframe as a tab-separated .txt
