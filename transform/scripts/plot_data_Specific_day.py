############################# Multiplot 
import os
import pandas as pd
import matplotlib.pyplot as plt
from itertools import cycle
import numpy as np
import matplotlib.dates as mdates

# Define the path to the folder containing the .csv files
folder_path_Discharge = 'C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/Meteo_Discharge/Filtered_OHNEGH'

# Get a list of all .csv files in the folder
file_list_Discharge = [file for file in os.listdir(folder_path_Discharge) if file.endswith(".csv")]

# Initialize lists to store data
timestamps = []
column_names_Discharge = []
data_Discharge = {}

# Loop through each file and read in the data
for file_name in file_list_Discharge:
    file_path_Discharge = os.path.join(folder_path_Discharge, file_name)
    file_data_Discharge = pd.read_csv(file_path_Discharge, delimiter='\t')

    # Combine the datetime columns into a single datetime object
    timestamp_Discharge = [pd.Timestamp(int(row['YY']), int(row['MM']), int(row['DD']), int(row['HH']), int(row['MN'])) for _, row in file_data_Discharge.iterrows()]

    # Extract the column name and data columns
    column_name = os.path.splitext(file_name)[0]
    column_names_Discharge.append(column_name)
    data_Discharge[column_name] = file_data_Discharge['Stat1']

    # Store timestamps for later use
    timestamps.append(timestamp_Discharge)

# Define the central date and the date range around it
central_date = pd.Timestamp('2022-05-31')
start_date = central_date - pd.Timedelta(days=10)
end_date = central_date + pd.Timedelta(days=10)

# Calculate the number of datasets based on the length of column_names_Discharge
num_datasets = len(column_names_Discharge)
# Define a list of colors to cycle through
#colors = cycle(['b', 'g', 'm', 'c', 'c', 'k', 'k'])
colors = cycle(['b', 'g', 'm', 'c', 'k'])


# Create subplots with adjusted spacing
fig, axs = plt.subplots(num_datasets, 1, figsize=(10, 6*num_datasets), sharex=True, 
                        gridspec_kw={'top': 0.85, 'bottom': 0.11, 'left': 0.45, 'right': 0.9, 'hspace': 0.10, 'wspace': 0.10},
                        constrained_layout=True)

# Plot each dataset on a separate subplot with a different color
for i, column in enumerate(column_names_Discharge):
    # Filter the timestamps and data based on the date range
    mask = (np.array(timestamps[i]) >= start_date) & (np.array(timestamps[i]) <= end_date)
    filtered_timestamps = np.array(timestamps[i])[mask]
    filtered_data = np.array(data_Discharge[column])[mask]
    
    axs[i].plot(filtered_timestamps, filtered_data, color=next(colors), label=column, linewidth=0.5)

     # Set the x-axis limits to the specified date range
    axs[i].set_xlim(start_date, end_date)

    # Find the index of the maximum value in the current dataset
    max_index = np.argmax(filtered_data)

    # Find the index of the maximum value in the current dataset
    max_index = np.argmax(filtered_data)

    # Get the timestamp and value at the peak
    peak_timestamp = filtered_timestamps[max_index]
    peak_value = filtered_data[max_index]

    # Annotate the peak value on the plot in black and smaller font size
    #axs[i].annotate(f'Peak Value: {peak_value:.2f}', xy=(peak_timestamp, peak_value), xytext=(peak_timestamp, peak_value + 1),
    #                fontsize=8, color='black', ha='center')

    # Set the y-axis limits for each subplot individually
    y_min = filtered_data.min()-0.5
    y_max = filtered_data.max()+0.5
    axs[i].set_ylim(y_min, y_max)
    
    # Add a grid to the subplot
    axs[i].grid(True)

# Save the figure as a .png file with the defined size
plt.savefig('output_plot.png')    

# Show the plot (optional)
plt.show()



print("done")
