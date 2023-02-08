import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import glob

# Load data into a DataFrame
df = pd.read_csv('C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/GitHubMasterSkripts/MasterSkript/transform/scripts/Historgram/Winddir.csv',sep= "\t", engine='python', skiprows=4)

## Daten korrigieren vor Histogramm ###
# df["Stat1"] = df["Stat1"].where((df["Stat1"] >= -45) & (df["Stat1"] <= 45), other=np.nan)     # Nur bei Temp. anwenden!
df["Stat1"] = df["Stat1"].where((df["Stat1"] > 0) & (df["Stat1"] <= 360), other=np.nan)
file_path = "C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/GitHubMasterSkripts/MasterSkript/transform/scripts/Historgram/Winddir.csv"
file_name = os.path.basename(file_path).split('.')[0]

# Get the column of interest
header = df.columns
data = df.loc[:,"Stat1"]


## Datenuntersuchung
                           
max_value = df["Stat1"].max()
top_100max = df["Stat1"].nlargest(100)
min_value = df["Stat1"].min()       
top_100min = df["Stat1"].nsmallest(100)
print("Max Value in Stat1=", max_value, "toptenmin=",top_100min, "toptenmax=", top_100max)

                    #print(df)
                    # print(header,"Header")

# Plot histogram with 15 bins
plt.hist(data, bins=200, color='red', edgecolor='black')

# Add labels and title
plt.xlabel('Data Values')
plt.ylabel('Frequency')
plt.title(file_name)

# Create the directory if it does not exist
plot_dir = "plots"
if not os.path.exists(plot_dir):
    os.makedirs(plot_dir)

# Save the plot to the directory
plot_path = os.path.join(plot_dir, file_name + ".png")
print("Plot will be saved to:", plot_path)
plt.savefig(plot_path)

# Show plot
plt.show()

print('done')





