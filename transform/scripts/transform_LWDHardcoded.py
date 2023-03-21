import pandas as pd

# set the file path
file_path = "C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/GitHubMasterSkripts/MasterSkript/transform/input/lwd_Tirol_15140917-T0-BasisganglinieTest.csv"

# read in the data as a pandas dataframe
df = pd.read_csv(file_path, delimiter=";", names=["datetime", "value"], skiprows=15)

# split the datetime column into date and time columns
date, time = df["datetime"].str.split(" ").str
time = time.str.split(";").str[0]

# combine the date and time columns into a single datetime column
df["datetime"] = pd.to_datetime(date + " " + time, format="%d.%m.%Y %H:%M:%S")

# format the value column as required
df["value"] = df["value"].str.replace(",", ".")

# replace missing values with -9999
df['value'] = df['value'].fillna(-9999)

# format the DateTime column as required
df['YY'] = df['datetime'].dt.strftime('%Y')
df['MM'] = df['datetime'].dt.strftime('%m')
df['DD'] = df['datetime'].dt.strftime('%d')
df['HH'] = df['datetime'].dt.strftime('%H')
df['MN'] = df['datetime'].dt.strftime('%M')

# remove the original date and time columns
df = df.drop(["datetime"], axis=1)

# create a header row
header_row = pd.DataFrame([['YY', 'MM', 'DD', 'HH', 'MN', 'LDW'], ['YY', 'MM', 'DD', 'HH', 'MN', '2997'], ['YY', 'MM', 'DD', 'HH', 'MN', '46.896034'], ['YY', 'MM', 'DD', 'HH', 'MN', '10.190435'], ['YY', 'MM', 'DD', 'HH', 'MN', 'value']], columns=['YY', 'MM', 'DD', 'HH', 'MN', 'value'])

# concatenate the header row with the data frame
df = pd.concat([header_row, df], ignore_index=True)

# set the file path for saving the output file
output_path = "C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/GitHubMasterSkripts/MasterSkript/transform/output/TransformLWD.txt"

# save the dataframe as a tab-separated .txt file with the desired format
df.to_csv(output_path, sep='\t', index=False)

print('done')