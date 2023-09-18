############################# Multiplot 
import os
import pandas as pd
import matplotlib.pyplot as plt
from itertools import cycle

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

# Create subplots for each dataset with increased spacing
num_datasets = len(column_names_Discharge)
fig, axs = plt.subplots(num_datasets, 1, figsize=(12, 6*num_datasets), sharex=True, gridspec_kw={'hspace': 0.3})

# Create a list of colors for plotting
colors = cycle(['b', 'g', 'c', 'c', 'm', 'y', 'y'])

# Plot each dataset on a separate subplot with a different color
for i, column in enumerate(column_names_Discharge):
    axs[i].plot(timestamps[i], data_Discharge[column], color=next(colors), label=column, linewidth=0.5)
    axs[i].set_ylabel(column, rotation=0, ha='right')  # Set y-axis label horizontally
    axs[i].grid(True)

# Set the title and x-axis label for the entire figure
fig.suptitle('Data from Discharge folder', fontsize=16)
axs[-1].set_xlabel('Timestamp', fontsize=14)

# Show the plot
plt.show()



####################################### NAN Plot################################################

# import os
# import pandas as pd
# import matplotlib.pyplot as plt

# # Define the path to the folder containing the .csv files
# folder_path_Discharge = 'C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/Meteo_Discharge/Filtered'

# # Get a list of all .csv files in the folder
# file_list_Discharge = [file for file in os.listdir(folder_path_Discharge) if file.endswith(".csv")]

# # Initialize lists to store data
# timestamps = []
# column_names_Discharge = []
# data_Discharge = {}

# # Loop through each file and read in the data
# for file_name in file_list_Discharge:
#     file_path_Discharge = os.path.join(folder_path_Discharge, file_name)
#     file_data_Discharge = pd.read_csv(file_path_Discharge, delimiter='\t')

#     # Extract the timestamp and data columns
#     timestamp_Discharge = pd.to_datetime(file_data_Discharge['YY'].astype(int).astype(str) + '-' +
#                                          file_data_Discharge['MM'].astype(int).astype(str) + '-' +
#                                          file_data_Discharge['DD'].astype(int).astype(str) + ' ' +
#                                          file_data_Discharge['HH'].astype(int).astype(str) + ':' +
#                                          file_data_Discharge['MN'].astype(int).astype(str))

#     # Extract the column name and data columns
#     column_name = os.path.splitext(file_name)[0]
#     column_names_Discharge.append(column_name)
#     data_Discharge[column_name] = file_data_Discharge['Stat1']

#     # Store timestamps for later use
#     timestamps.append(timestamp_Discharge)

# # Create a DataFrame for the timestamps
# timestamps_df = pd.concat(timestamps, axis=1)
# timestamps_df.columns = column_names_Discharge

# # Create a stacked plot
# plt.figure(figsize=(12, 6))

# for column in column_names_Discharge:
#     plt.plot(timestamps_df.index, data_Discharge[column], label=column)

# # Set the title and axis labels
# plt.title('Data from Discharge folder')
# plt.xlabel('Timestamp')

# # Create a scatter plot to visualize the occurrence of NaN values
# nan_matrix = timestamps_df.isna()

# # Create a new figure
# plt.figure(figsize=(12, 6))

# # Plot the NaN occurrences as a scatter plot
# for i, column in enumerate(column_names_Discharge):
#     nan_indices = nan_matrix.index[nan_matrix[column]].tolist()
#     plt.scatter(timestamps_df.index[nan_indices], [i] * len(nan_indices), marker='x', label=column)

# # Set y-axis ticks and labels
# plt.yticks(range(len(column_names_Discharge)), column_names_Discharge)

# # Set x-axis label and title
# plt.xlabel('Timestamp')
# plt.title('NaN Occurrences Visualization')

# # Invert y-axis for better visualization
# plt.gca().invert_yaxis()

# # Show legend
# plt.legend()

# # Show the plots
# plt.show()


# ## Plot shouing NAN und Multiplot in One ##################### 
# import os
# import pandas as pd
# import matplotlib.pyplot as plt

# # Define the path to the folder containing the .csv files
# folder_path_Discharge = 'C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/Meteo_Discharge/Filtered'

# # Get a list of all .csv files in the folder
# file_list_Discharge = [file for file in os.listdir(folder_path_Discharge) if file.endswith(".csv")]

# # Initialize lists to store data
# timestamps = []
# column_names_Discharge = []
# data_Discharge = {}

# # Loop through each file and read in the data
# for file_name in file_list_Discharge:
#     file_path_Discharge = os.path.join(folder_path_Discharge, file_name)
#     file_data_Discharge = pd.read_csv(file_path_Discharge, delimiter='\t')

#     # Extract the timestamp and data columns
#     timestamp_Discharge = pd.to_datetime(file_data_Discharge['YY'].astype(int).astype(str) + '-' +
#                                          file_data_Discharge['MM'].astype(int).astype(str) + '-' +
#                                          file_data_Discharge['DD'].astype(int).astype(str) + ' ' +
#                                          file_data_Discharge['HH'].astype(int).astype(str) + ':' +
#                                          file_data_Discharge['MN'].astype(int).astype(str))

#     # Extract the column name and data columns
#     column_name = os.path.splitext(file_name)[0]
#     column_names_Discharge.append(column_name)
#     data_Discharge[column_name] = file_data_Discharge['Stat1']

#     # Store timestamps for later use
#     timestamps.append(timestamp_Discharge)

# # Create a DataFrame for the timestamps
# timestamps_df = pd.concat(timestamps, axis=1)
# timestamps_df.columns = column_names_Discharge

# # Create a new figure with subplots
# fig, axs = plt.subplots(2, 1, figsize=(12, 8))

# # Plot the stacked plot in the first subplot
# axs[0].stackplot(timestamps_df.index, data_Discharge.values(), labels=column_names_Discharge)
# axs[0].set_title('Data from Discharge folder')
# axs[0].set_xlabel('Timestamp')
# axs[0].legend(loc='upper right')

# # Create a matrix indicating the locations of NaN values
# nan_matrix = timestamps_df.isna()

# # Plot the NaN occurrences as a scatter plot in the second subplot
# for i, column in enumerate(column_names_Discharge):
#     nan_indices = nan_matrix.index[nan_matrix[column]].tolist()
#     axs[1].scatter(timestamps_df.index[nan_indices], [i] * len(nan_indices), marker='x', label=column)

# # Set y-axis ticks and labels
# axs[1].set_yticks(range(len(column_names_Discharge)))
# axs[1].set_yticklabels(column_names_Discharge)

# # Set x-axis label and title
# axs[1].set_xlabel('Timestamp')
# axs[1].set_title('NaN Occurrences Visualization')

# # Invert y-axis for better visualization
# axs[1].invert_yaxis()

# # Show legend for the scatter plot
# axs[1].legend(loc='upper right')

# # Adjust spacing between subplots
# plt.tight_layout()

# # Show the plots
# plt.show()
