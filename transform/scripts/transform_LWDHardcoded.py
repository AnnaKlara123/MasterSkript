import pandas as pd
import os
import numpy as np


######################## Read in file ########################################################################
# set the file path
file_path = "C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/GitHubMasterSkripts/MasterSkript/transform/input/LWD_Inputs/lwd_Tirol_1197091-LF-Basisganglinie.csv"
# extract the filename without the extension
filename = os.path.splitext(os.path.basename(file_path))[0]

# read in the data as a pandas dataframe
df = pd.read_csv(file_path, delimiter=";", names=["datetime", "Stat1"], skiprows=98)

# split the datetime column into date and time columns
datetime_split = df["datetime"].str.split(" ")
date = datetime_split.str[0]
time = datetime_split.str[1].str.split(";").str[0]

# combine the date and time columns into a single datetime column
df["datetime"] = pd.to_datetime(date + " " + time, format="%d.%m.%Y %H:%M:%S")

######################## NaN Replacement & Exclude of irrational Values ################################

# format the value column as required
df["Stat1"] = df["Stat1"].str.replace(",", ".") # TUNR OFF at Global Radiation!!             

# replace missing values represented as "---" with NaN
df['Stat1'] = pd.to_numeric(df['Stat1'], errors='coerce')

# set all missing values and values above 100 to NaN
df['Stat1'] = np.where((df['Stat1'].isna()) | (df['Stat1'] > 100), np.nan, df['Stat1'])  ###### Change NAN HERE #############

################################################################################################################################

################################ Format the DF for the WaSiM output################################
# format the DateTime column as required
df['YY'] = df['datetime'].dt.strftime('%Y')
df['MM'] = df['datetime'].dt.strftime('%m')
df['DD'] = df['datetime'].dt.strftime('%d')
df['HH'] = df['datetime'].dt.strftime('%H')
df['MN'] = df['datetime'].dt.strftime('%M')

# remove the original date and time columns
df = df.drop(["datetime"], axis=1)

#####  create a header row CHANGE LAT, LONG & HIGHT FOR DIFFERENT STATIONS!#####################################
# IMPORTANT for Station with Station Number:  15140917
header_row = pd.DataFrame([['YY', 'MM', 'DD', 'HH', 'MN', 'LDW Jamtalhuette'], ['YY', 'MM', 'DD', 'HH', 'MN', '2172'], ['YY', 'MM', 'DD', 'HH', 'MN', '46.885912'], ['YY', 'MM', 'DD', 'HH', 'MN', '10.177635'], ['YY', 'MM', 'DD', 'HH', 'MN', 'Stat1']], columns=['YY', 'MM', 'DD', 'HH', 'MN', 'Stat1'])
# vs.  IMPORTANT for Station with Station Number:  1197091 ####################
#header_row = pd.DataFrame([['YY', 'MM', 'DD', 'HH', 'MN', 'LDW Gamshorn'], ['YY', 'MM', 'DD', 'HH', 'MN', '2997'], ['YY', 'MM', 'DD', 'HH', 'MN', '46.896034'], ['YY', 'MM', 'DD', 'HH', 'MN', '10.190435'], ['YY', 'MM', 'DD', 'HH', 'MN', 'Stat1']], columns=['YY', 'MM', 'DD', 'HH', 'MN', 'Stat1'])

# create a .csv copy for later calculations 
header_row_copy = pd.DataFrame(columns=['YY', 'MM', 'DD', 'HH', 'MN', 'Stat1'])

# concatenate the header row with the data frame
df = pd.concat([header_row, df], ignore_index=True)
df_csv =pd.concat([header_row_copy,df],ignore_index=True)

#############################################################################################################################

#################### Save Files ################################################################################
# set the file path for saving the CSV file
# IMPORTANT! NaN
csv_path = f"C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/GitHubMasterSkripts/MasterSkript/transform/output/{filename}NaN.csv"         ###### Change NAN HERE #############
# vs. IMPORTANT!-9999
#csv_path = f"C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/GitHubMasterSkripts/MasterSkript/transform/output/{filename}_9999.csv"


# save the new dataframe as a CSV file
df_csv.to_csv(csv_path,sep='\t', index=False)

# set the file path for saving the output.txt  file
#NaN
output_path = f"C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/GitHubMasterSkripts/MasterSkript/transform/output/{filename}NaN.txt"      ###### Change NAN HERE #############
#-9999
#output_path = f"C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/GitHubMasterSkripts/MasterSkript/transform/output/{filename}-9999.txt"

 # save the dataframe as a tab-separated .txt file with the desired format
df.to_csv(output_path, sep='\t', index=False)
#############################################################################################################################
print('done')