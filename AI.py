import matplotlib.pyplot as plt
import pandas as pd

# Read data from a CSV file
df = pd.read_csv("Precipitation_KItest.csv", delimiter=' ')

date = df['Date']
date_time = pd.to_datetime(date, format='%Y%m%d%H%M%S')
value = df['Value']

df.insert(2, 'datetime', date_time)   # (Spalte, Header, Value)

print(df)


# Set the 'date' column as the index
df.set_index(date_time, inplace=True)

# Replace all -9999 values with NaN
df.replace(-777, pd.NaT, inplace = True)

# # Convert the date column to a datetime object
# df['datetime'] = pd.to_datetime(df['datetime'])

# # Filter the dataframe to only include the past year
# df = df[df['datetime'] > (pd.datetime.now() - pd.DateOffset(years=1))]

# Plot the values
plt.plot(df['datetime'], df['Value'])

# Add labels to the x and y axes
plt.xlabel('datetime')
plt.ylabel('Value')

# Show the plot
plt.show()

# Plot the values in the 'value' column over time
# plt.plot(df['Value'])

# # Add labels and a title to the plot
# plt.xlabel('datetime')
# plt.ylabel('Value')
# plt.title('Values over Time')

# # Show the plot
# plt.show()


# import pandas as pd

# # Read the CSV file into a DataFrame
# df = pd.read_csv("Precipitation_KItest.csv")

# # Print the first 5 rows of the DataFrame
# print(df.head())

# # date = df['Date'].tolist()
# # value = df["Value"].tolist()

# date = df['Date']
# value = df['Value']

# # Convert the date column to a datetime object
# df['date'] = pd.to_datetime(df['date'])

# # Filter the dataframe to only include the past year
# df = df[df['date'] > (pd.datetime.now() - pd.DateOffset(years=1))]

# # Plot the values
# plt.plot(df['date'], df['value'])

# # Add labels to the x and y axes
# plt.xlabel('Date')
# plt.ylabel('Value')

# # Show the plot
# plt.show()