import pandas as pd
from datetime import datetime
from datetime import timedelta 

# Read the dataset from a CSV file
df = pd.read_csv('C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/GitHubMasterSkripts/MasterSkript/transform/output/WaSiM_Combined_files/WaSiM_Wind/cut/lwd_Tirol_GH_1197091-WG-BasisganglinieNaN_10min_cut.csv', sep='\t')

# Convert YY, MM, DD, HH, MN columns to a single datetime column

# Combine the datetime columns into a single datetime object
timestamp = [pd.Timestamp(int(row['YY']), int(row['MM']), int(row['DD']), int(row['HH']), int(row['MN'])) for i, row in df.iterrows()]

# Convert the timestamp list to a DatetimeIndex object and set it as the new index
df.index = pd.DatetimeIndex(timestamp)

print(df.columns)

# Set the desired end date for filling the dataset
end_date = datetime(2022, 9, 30, 0, 0, 0)

# Create a new DataFrame with the missing dates and NaN values
missing_dates = pd.date_range(start=df.index[-1] + timedelta(minutes=10), end=end_date, freq='10min')
missing_table = pd.DataFrame({'Stat1': float('nan')}, index=missing_dates)


# Concatenate the original DataFrame and the missing DataFrame
lwd_Tirol_GH_1197091_LF_BasisganglinieNaN_10min_2022 = pd.concat([df, missing_table])

# Extract the year, month, day, hour, minute from the Timestamp column
lwd_Tirol_GH_1197091_LF_BasisganglinieNaN_10min_2022['YY'] = lwd_Tirol_GH_1197091_LF_BasisganglinieNaN_10min_2022.index.year
lwd_Tirol_GH_1197091_LF_BasisganglinieNaN_10min_2022['MM'] = lwd_Tirol_GH_1197091_LF_BasisganglinieNaN_10min_2022.index.month
lwd_Tirol_GH_1197091_LF_BasisganglinieNaN_10min_2022['DD'] = lwd_Tirol_GH_1197091_LF_BasisganglinieNaN_10min_2022.index.day
lwd_Tirol_GH_1197091_LF_BasisganglinieNaN_10min_2022['HH'] = lwd_Tirol_GH_1197091_LF_BasisganglinieNaN_10min_2022.index.hour
lwd_Tirol_GH_1197091_LF_BasisganglinieNaN_10min_2022['MN'] = lwd_Tirol_GH_1197091_LF_BasisganglinieNaN_10min_2022.index.minute

# Rearrange the columns
# Reset the index and drop the timestamp column
lwd_Tirol_GH_1197091_LF_BasisganglinieNaN_10min_2022.reset_index(drop=True, inplace=True)

# Construct the output file path
output_file_path = 'C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/GitHubMasterSkripts/MasterSkript/transform/output/WaSiM_Combined_files/WaSiM_Wind/cut/lwd_Tirol_GH_1197091-WG-BasisganglinieNaN_10min_cut_fillup.csv'

# Save the DataFrame as a CSV file with custom formatting
lwd_Tirol_GH_1197091_LF_BasisganglinieNaN_10min_2022.to_csv(output_file_path, index=False, sep='\t')

print("saved")