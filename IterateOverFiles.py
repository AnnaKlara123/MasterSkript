import os
import pandas as pd
import glob
import os

# directory = 'C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/Daten/Meteorologie/jamtalhütte_20200401'

# for filename in os.listdir(directory):
#     if filename.endswith(".csv"):                       # Alternativ nach Excel daten suchen: (".xlsx")
#      filename = os.path.join(directory, filename)

#     if os.path.isfile (filename):
#         print("files in path are:", filename)
        



# Get CSV files list from a folder
path = 'C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/Daten/Meteorologie/jamtalhütte_20200401'
csv_files = glob.glob(path + "/*.csv")
print("csv Files are:'", csv_files)

# Read each CSV file into DataFrame
# This creates a list of dataframes
df_list = (pd.read_csv(file) for file in csv_files)
print("csvdfListe is:", df_list)

# # Concatenate all DataFrames
# big_df   = pd.concat(df_list, ignore_index=True)