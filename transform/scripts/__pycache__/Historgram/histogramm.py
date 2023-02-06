import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Load data into a DataFrame
df = pd.read_csv('C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/GitHubMasterSkripts/MasterSkript/transform/scripts/Historgram/Soiltemp.csv',sep= "\t", engine='python', skiprows=4)

# Get the column of interest

header = df.columns
# print(df)
# print(header,"Header")

df["Stat1"] = df["Stat1"].where(df["Stat1"] <= 45, other=np.nan)
data = df.loc[:,"Stat1"]

max_value = df["Stat1"].max()
top_100 = df["Stat1"].nlargest(100)
print("Max Value in Stat1=", max_value, "topten=",top_100)

# Plot histogram with 15 bins
plt.hist(data, bins=100, color='red', edgecolor='black')

# Add labels and title
plt.xlabel('Data Values')
plt.ylabel('Frequency')
plt.title('Histogram')

# Show plot
plt.show()


#df.to_csv("test.csv", sep=' ', index=False)