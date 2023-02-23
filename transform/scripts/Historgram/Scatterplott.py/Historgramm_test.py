import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.dates import date2num
import datetime

# Read the header row separately to get the column names
#header = pd.read_csv('C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/GitHubMasterSkripts/MasterSkript/transform/output/AirtempTest.csv', nrows=1).columns

# Load data into a DataFrame while skipping the first 5 lines
df = pd.read_csv('C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/GitHubMasterSkripts/MasterSkript/transform/output/AirtempTest.csv', sep='\t')

print(df)
# Get the columns of interest
x = df['Stat1'].values
print(x)

# Combine the datetime columns into a single datetime object
dates = [datetime.datetime(int(row['YY']), int(row['MM']), int(row['DD']), int(row['HH']), int(row['MM'])) for i, row in df.iterrows()]

# Convert datetime objects to numbers that can be plotted on the y-axis
y = date2num(dates)

# Plot scatter plot
plt.scatter(x, y, color='red')

# Add labels and title
plt.xlabel('X Values')
plt.ylabel('Datetime')
plt.title('Scatter Plot Example')

# Show plot
plt.show()
