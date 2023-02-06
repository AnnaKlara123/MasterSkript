import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
from matplotlib.dates import date2num
import datetime

# Load data into a DataFrame
df = pd.read_csv('C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/GitHubMasterSkripts/MasterSkript/transform/scripts/Historgram/Airtemp.csv',sep= "\t", engine='python', skiprows=4)

## Daten korrigieren vor Histogramm ###
df["Stat1"] = df["Stat1"].where(df["Stat1"] >= -45, other=np.nan)
file_path = "C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/GitHubMasterSkripts/MasterSkript/transform/scripts/Historgram/Airtemp.csv"
file_name = os.path.basename(file_path).split('.')[0]

# Get the columns of interest
y = df['Stat1'].values
print("y=", y)

# Combine the datetime columns into a single datetime object
dates = [datetime.datetime(int(row['YY']), int(row['MM']), int(row['DD']), int(row['HH']), int(row['MM'])) for i, row in df.iterrows()]
print("dates=", dates[:100])

# Convert datetime objects to numbers that can be plotted on the y-axis
x = date2num(dates)
print("x=", x)

# Plot scatter plot
plt.scatter(x, y, color='red')

# Add labels and title
plt.xlabel('X Values')
plt.ylabel('Datetime')
plt.title('Scatter Plot Example')

# Show plot
plt.show()