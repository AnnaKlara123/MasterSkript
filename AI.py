import matplotlib.pyplot as plt
import pandas as pd

# Read data from a CSV file
df = pd.read_csv("Precipitation_KItest.csv", delimiter=' ')

date = df['Date']
date_time = pd.to_datetime(date, format='%Y%m%d%H%M%S')
value = df['Value']
df.replace(-777, pd.NaT, inplace = True)

# print('date is:', date)
# print('datetime ist:', date_time)
# print('value is:', value)

df.insert(2, 'datetime', date_time)   # (Spalte, Header, Value)

print(df)


#data.insert(2, 'datetime', '22')   # (Spalte, Header, Value)

# Set the 'date' column as the index
df.set_index('datetime', inplace=True)

# Plot the values in the 'value' column over time
plt.plot(df['Value'])

# Add labels and a title to the plot
plt.xlabel('datetime')
plt.ylabel('Value')
plt.title('Values over Time')

# Show the plot
plt.show()


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