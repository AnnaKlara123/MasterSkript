import pandas as pd
import argparse
import os


# Create the parser
# parser = argparse.ArgumentParser()
# parser.add_argument('--dir', type=str, help='The directory where the file is located', default= "C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/GitHubMasterSkripts/MasterSkript/transform/input")
# parser.add_argument('--filename', type=str, help='The filename to read', default="lwd_Tirol_15140917-T0-Basisganglinie.csv")
# args = parser.parse_args()

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
df['MM'] = df['datetime'].dt.strftime('%M')

# # remove the original date and time columns
# df = df.drop(["datetime"], axis=1)

# add the header row to the dataframe
header_df = pd.DataFrame([['YY', 'MM', 'DD', 'HH', 'MM', 'Stat1']], columns=['YY', 'MM', 'DD', 'HH', 'MM', 'Stat1'])

# set the file path for saving the output file
output_path = "C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/GitHubMasterSkripts/MasterSkript/transform/output/TransformLWD.txt"


# drop the original date and time columns
df = df.drop(["datetime"], axis=1)

# reorder the columns to match the desired output format
df = df[['YY', 'MM', 'DD', 'HH', 'MM', 'value']]

# save the dataframe as a tab-separated .txt file with the desired format
df.to_csv(output_path, sep='\t', index=False)



# import pandas as pd

# # set the file path
# file_path = "C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/GitHubMasterSkripts/MasterSkript/transform/input/lwd_Tirol_15140917-T0-BasisganglinieTest.csv"

# # read in the data as a pandas dataframe
# df = pd.read_csv(file_path, delimiter=";", names=["datetime", "value"])

# # split the datetime column into date and time columns
# date, time = df["datetime"].str.split(" ").str
# time = time.str.split(";").str[0]

# # combine the date and time columns into a single datetime column
# df["datetime"] = pd.to_datetime(date + " " + time, format="%d.%m.%Y %H:%M:%S")

# # remove the original date and time columns
# df = df.drop(["datetime"], axis=1)

# # format the value column as required
# df["value"] = df["value"].str.replace(",", ".")

# # add the header row to the dataframe
# header_df = pd.DataFrame(
#     [["YY", "MM", "DD", "HH", "MM", "Stat1"]],
#     columns=["YY", "MM", "DD", "HH", "MM", "Stat1"],)

# # concatenate the header row and the data rows
# result_df = pd.concat([header_df, df.reset_index(drop=True)])

# # save the dataframe as a tab-separated txt file
# result_df.to_csv("filename.txt", sep="\t", header=False, index=False)
