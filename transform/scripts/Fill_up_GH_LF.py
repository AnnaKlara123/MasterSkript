import pandas as pd
from datetime import datetime

# Read the dataset from a CSV file
df = pd.read_csv('C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/GitHubMasterSkripts/MasterSkript/transform/output/convert_frequancy/10min_frequency_Neu/GH/lwd_Tirol_GH_1197091-LF-BasisganglinieNaN_10min.csv', sep='\t')

# Convert YY, MM, DD, HH, MN columns to a single datetime column

# Combine the datetime columns into a single datetime object
timestamp = [pd.Timestamp(int(row['YY']), int(row['MM']), int(row['DD']), int(row['HH']), int(row['MN'])) for i, row in df.iterrows()]

# Convert the timestamp list to a DatetimeIndex object and set it as the new inde
df.index = pd.DatetimeIndex(timestamp)

print(df.columns)

# Set the desired end date for filling the dataset
end_date = datetime(2021, 9, 30)

# Generate the missing dates between the last date in the dataset and the end date
missing_dates = pd.date_range(df.index.max(), end_date, freq='10min')[1:]

# Create a new DataFrame to store the filled dataset
filled_df = pd.DataFrame(columns=df.columns)

# Iterate through the missing dates and append rows with NaN values to the filled DataFrame
for date in missing_dates:
    filled_df = filled_df.append(pd.Series({'index': date, 'Stat1': float('NaN')}), ignore_index=True)

# Concatenate the original dataset and the filled dataset
filled_dataset = pd.concat([df, filled_df], ignore_index=True)

# Save the filled dataset to a new CSV file
filled_dataset.to_csv('FILL2022_lwd_Tirol_GH_1197091-LF-BasisganglinieNaN_10min.csv', index=False, sep='\t')

print("done")