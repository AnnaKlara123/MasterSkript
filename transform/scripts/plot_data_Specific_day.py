############################# Multiplot 
import os
import pandas as pd
import matplotlib.pyplot as plt
from itertools import cycle
import numpy as np
import matplotlib.dates as mdates

# Define the path to the folder containing the .csv files
folder_path_Discharge = 'C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/Meteo_Discharge/Filtered'

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
central_date = pd.Timestamp('2018-06-15')
start_date = central_date - pd.Timedelta(days=10)
end_date = central_date + pd.Timedelta(days=90) # bei Jahr 80

# Calculate the number of datasets based on the length of column_names_Discharge
num_datasets = len(column_names_Discharge)
# Define a list of colors to cycle through
colors = cycle(['b', 'g', 'm', 'c', 'c', 'k', 'k'])
#colors = cycle(['b', 'g', 'm', 'c', 'k'])


# Define the labels for each dataset
labels = ["Discharge m³/s", "Precipitation mm/m²", "Global Radiation W/m²", "Temperature °C", "Relative Humidity %"]

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
    
    # Create arrays for x and y values without NaN
    x_values = []
    y_values = []
    for x, y in zip(filtered_timestamps, filtered_data):
        if not np.isnan(y):
            x_values.append(x)
            y_values.append(y)

    axs[i].plot(x_values, y_values, color=next(colors), label=column, linewidth=0.5)

    # Set the x-axis limits to the specified date range
    axs[i].set_xlim(start_date, end_date)

    # Find the index of the maximum value in the current dataset
    max_index = np.argmax(y_values)

    # Get the timestamp and value at the peak
    peak_timestamp = x_values[max_index]
    peak_value = y_values[max_index]

    # Set the y-axis limits for each subplot individually
    y_min = min(y_values) - 0.5
    y_max = max(y_values) + 0.5
    axs[i].set_ylim(y_min, y_max)

    # Add a grid to the subplot
    axs[i].grid(True)

    # Add labels to the subplots
    axs[i].set_ylabel(labels[i])

# # Set the x-axis limits to the specified date range
# for ax in axs:
#     ax.set_xlim(start_date, end_date)

#     # Add time labels every 3 hours
#     ax.xaxis.set_major_locator(mdates.HourLocator(interval=4))
#     ax.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m %H'))

# Save the figure as a .png file with the defined size
plt.savefig('output_plot.png')    

# Show the plot (optional)
plt.show()


print("done")
