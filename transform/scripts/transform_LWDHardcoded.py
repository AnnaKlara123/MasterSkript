import pandas as pd
import os



# set the file path
file_path = "C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/GitHubMasterSkripts/MasterSkript/transform/input/LWD_Inputs/lwd_Tirol_15140917-GS-Basisganglinie.csv"
# extract the filename without the extension
filename = os.path.splitext(os.path.basename(file_path))[0]

# read in the data as a pandas dataframe
df = pd.read_csv(file_path, delimiter=";", names=["datetime", "value"], skiprows=219)

# split the datetime column into date and time columns
datetime_split = df["datetime"].str.split(" ")
date = datetime_split.str[0]
time = datetime_split.str[1].str.split(";").str[0]

# combine the date and time columns into a single datetime column
df["datetime"] = pd.to_datetime(date + " " + time, format="%d.%m.%Y %H:%M:%S")

# format the value column as required
df["value"] = df["value"].str.replace(",", ".") # TUNR OFF at Global Radiation!!

# replace missing values represented as "---" with -9999
#df['value'] = pd.to_numeric(df['value'], errors='coerce').fillna("NaN")
df['value'] = pd.to_numeric(df['value'], errors='coerce').fillna(-9999)


# format the DateTime column as required
df['YY'] = df['datetime'].dt.strftime('%Y')
df['MM'] = df['datetime'].dt.strftime('%m')
df['DD'] = df['datetime'].dt.strftime('%d')
df['HH'] = df['datetime'].dt.strftime('%H')
df['MN'] = df['datetime'].dt.strftime('%M')

# remove the original date and time columns
df = df.drop(["datetime"], axis=1)

# create a header row CHANGE LAT, LONG & HIGHT FOR DIFFERENT STATIONS!
header_row = pd.DataFrame([['YY', 'MM', 'DD', 'HH', 'MN', 'LDW Jamtalhuette'], ['YY', 'MM', 'DD', 'HH', 'MN', '2172'], ['YY', 'MM', 'DD', 'HH', 'MN', '46.885912'], ['YY', 'MM', 'DD', 'HH', 'MN', '10.177635'], ['YY', 'MM', 'DD', 'HH', 'MN', 'value']], columns=['YY', 'MM', 'DD', 'HH', 'MN', 'value'])

# concatenate the header row with the data frame
df = pd.concat([header_row, df], ignore_index=True)

# set the file path for saving the output file
#NaN
#output_path = f"C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/GitHubMasterSkripts/MasterSkript/transform/output/{filename}NaN.txt"
#-9999
output_path = f"C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/GitHubMasterSkripts/MasterSkript/transform/output/{filename}-9999.txt"

# # save the dataframe as a tab-separated .txt file with the desired format
df.to_csv(output_path, sep='\t', index=False)

print('done')