import pandas as pd
from termcolor import colored
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


# Read in the CSV file
df = pd.read_csv('C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/GitHubMasterSkripts/MasterSkript/transform/input/Abfluss/Dischargeanalyse/DischargeRQ30_data_20190625_20220818/NaNRQ30_data_20190625_20220818.csv', sep=';', parse_dates=['Date'], na_values=['NA','NaN', 'nan'], index_col='Date')

# Create a boolean mask indicating whether each value is NaN
mask = df.isna()

# Reduce the boolean mask to a boolean Series indicating whether each row contains NaN values
nan_mask = mask.any(axis=1)

# Index the DataFrame to get only the rows that contain NaN values
df_nan = df[nan_mask]           # Worls fine!
# df_nan.to_csv('C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/GitHubMasterSkripts/MasterSkript/transform/input/Abfluss/Dischargeanalyse/DischargeRQ30_data_20190625_20220818/nan_valuelist_discharge.csv')
# print('NaN outputlist saved')
# Extract the date column from the DataFrame
dates = df_nan.index
# df_nan.to_csv('C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/GitHubMasterSkripts/MasterSkript/transform/input/Abfluss/Dischargeanalyse/DischargeRQ30_data_20190625_20220818/nan_dates_discharge.csv')
# print('NaN Dates saved')

# Create a line plot where the x-axis represents the dates and the y-axis represents the occurrence of NaN values
fig, ax = plt.subplots(figsize=(20, 5))
plt.plot(dates, [1]*len(dates), '.')
plt.title('NaN Values over Time')
plt.xlabel('Date')
plt.ylabel('NaN Value Occurrence')

# Loop over each date and annotate the corresponding dot with the date
# Add a label to the plot for each NaN value
annotated_dates = set()
for i, date in enumerate(dates):
    if date.strftime('%d-%h-%Y') not in annotated_dates:
        y_pos = 1 - (0.03 * len(annotated_dates)) # Adjust the y position based on the index of the annotation
        ax.text(date, y_pos, f"{date.strftime('%d-%h-%Y')}", ha='center', fontsize=6)
        annotated_dates.add(date.strftime('%d-%h-%Y'))

# Set the x-axis ticks and tick labels
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%y'))
ax.xaxis.set_tick_params(labelsize=5)

# Set the y-axis tick labels
ax.set_yticks([0, 1])
ax.set_yticklabels(['No NaN', 'NaN'])

plt.show()
