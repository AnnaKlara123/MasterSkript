import os
import argparse
import pandas as pd
from multiprocessing import Pool

# Function to round 'Stat1' column
def round_stat1(df, decimal_places):
    df['Stat1'] = df['Stat1'].round(decimal_places)
    return df

# Set the folder path where the CSV files are located
parser = argparse.ArgumentParser()
parser.add_argument('--dirin', type=str, help='The directory where the files are located', default="C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/GitHubMasterSkripts/MasterSkript/transform/output/WaSiM_Combined_files/WaSiM_Airtemp/finale_bereinigten_datensätze")
parser.add_argument('--dirout', type=str, help='The directory where the files should be saved', default= "C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/GitHubMasterSkripts/MasterSkript/transform/output/WaSiM_Combined_files/WaSiM_Airtemp/finale_bereinigten_datensätze")
parser.add_argument('--decimal-places', type=int, help='Number of digits after the decimal point', default=2)
args = parser.parse_args()

count = 0

# Function to process a single file
def process_file(file):
    if file.endswith(".csv"):
        df = pd.read_csv(os.path.join(args.dirin, file), delimiter='\t')
        df = round_stat1(df, args.decimal_places)
        new_file_name = os.path.splitext(file)[0] + "_round.csv"
        df.to_csv(os.path.join(args.dirout, new_file_name), sep='\t', index=False)
        print("Saving:", new_file_name)

# Loop through all the files in the folder
if __name__ == '__main__':
    count = 0
    file_list = [file for file in os.listdir(args.dirin) if file.endswith(".csv")]

    # Parallel processing using Pool
    with Pool() as pool:
        pool.map(process_file, file_list)

    # Print the number of files found and converted
    print("All", len(file_list), "files converted")
