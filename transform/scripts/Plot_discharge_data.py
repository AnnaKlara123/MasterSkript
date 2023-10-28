import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Define the path to the folder containing the .csv file
folder_path_Discharge = 'C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/Meteo_Discharge/Pure_Discharge'

# Specify the dataset file name
dataset_file_name = 'Discharge.csv'  # Replace with the actual dataset file name

# Construct the full path to the dataset file
file_path_Discharge = os.path.join(folder_path_Discharge, dataset_file_name)

# Check if the file exists
if os.path.exists(file_path_Discharge):
    # Read the dataset
    file_data_Discharge = pd.read_csv(file_path_Discharge, delimiter='\t')

    # Combine the datetime columns into a single datetime object
    timestamp_Discharge = [pd.Timestamp(int(row['YY']), int(row['MM']), int(row['DD']), int(row['HH']), int(row['MN'])) for _, row in file_data_Discharge.iterrows()]

    # Extract the data column
    data_Discharge = file_data_Discharge['Stat1']

# Set the layout parameters for the entire plot
    plt.subplots_adjust(top=0.8, bottom=0.435, left=0.045, right=0.98, hspace=0.2, wspace=0.2)

    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.plot(timestamp_Discharge, data_Discharge, color='b', label=dataset_file_name, linewidth=0.2)
    plt.grid(True)
    plt.title(f'Plot of {dataset_file_name}')
    plt.xlabel('Timestamp')
    plt.ylabel('Data Value')
    plt.legend()
    plt.show()
    print("done")
else:
    print(f"Dataset file '{dataset_file_name}' not found in the specified folder.")

