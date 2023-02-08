import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
from matplotlib.dates import date2num
import datetime

# Load data into a DataFrame
dfAir = pd.read_csv('C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/GitHubMasterSkripts/MasterSkript/transform/scripts/Historgram/Airtemp.csv',sep= "\t", engine='python', skiprows=4)
dfSoil = pd.read_csv('C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/GitHubMasterSkripts/MasterSkript/transform/scripts/Historgram/Soiltemp.csv',sep= "\t", engine='python', skiprows=4)


## Daten korrigieren vor Histogramm ###
dfAir["Stat1"] = dfAir["Stat1"].where(dfAir["Stat1"] >= -45, other=np.nan)
file_path = "C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/GitHubMasterSkripts/MasterSkript/transform/scripts/Historgram/Airtemp.csv"
file_name = os.path.basename(file_path).split('.')[0]

# Get the columns of interest
y = dfAir['Stat1'].values
x = dfSoil['Stat1'].values

# Combine the datetime columns into a single datetime object
# dates = [datetime.datetime(int(row['YY']), int(row['MM']), int(row['DD']), int(row['HH']), int(row['MM'])) for i, row in df.iterrows()]
# print("dates=", dates[:100])

# Convert datetime objects to numbers that can be plotted on the y-axis
# x = date2num(dates)
# print("x=", x)

# Plot scatter plot
plt.scatter(x, y, color='red')

# Add labels and title
plt.xlabel('X Soil')
plt.ylabel('y Air')
plt.title('Scatter Plot Example')

# Show plot
plt.show()