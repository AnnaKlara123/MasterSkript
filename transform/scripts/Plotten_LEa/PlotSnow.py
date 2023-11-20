import numpy as np
import pandas as pd
import datetime as dt

import matplotlib.pyplot as plt


def day_of_water_year(some_date):
    # Get the date of the previous October 1st
    water_year_start_date = dt.datetime(some_date.year + some_date.month // 10 - 1, 10, 1)
    
    # Return the number of days since then
    return (some_date - water_year_start_date).days + 1

data_path = "C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/GitHubMasterSkripts/MasterSkript/transform/scripts/Plotten_LEa/lwd_Tirol_15140917-HS-Basisganglinie.csv"

# read file: 
data = pd.read_csv(data_path, delimiter=';', na_values='---', skiprows=15, decimal=",",
                      names=['date', 'SH'], encoding='unicode_escape')



# # index to date time:
# data.index = pd.to_datetime(data.date, format='%d.%m.%Y %H:%M:%S')
# data.drop(columns='date', inplace=True)
# print(data)

# # Filter data for the years 2019, 2020, 2021, and 2022
# data = data['2018-10-01':'2022-09-30']

# # resample to daily mean:
# data_daily = data.resample('D').mean()


# data_daily['WY'] = data_daily.index.year
# data_daily['WY'].loc[data_daily.index.month >= 10] += 1
# data_daily['wday'] = data_daily.index.to_series().apply(day_of_water_year)


# # plot time series
# fig, ax = plt.subplots(1, 1, figsize=(10, 8))
# ax.plot(data_daily.index.values, data_daily.SH.values)
# ax.axvline(dt.datetime(2019, 6, 25), color='red', linestyle='--', label='June 25, 2019', linewidth=2)
# ax.axvline(dt.datetime(2020, 4, 19), color='red', linestyle='--', label='April 19, 2020', linewidth=2)
# ax.axvline(dt.datetime(2021, 5, 19), color='red', linestyle='--', label='May 19, 2021', linewidth=2)
# ax.axvline(dt.datetime(2022, 5, 13), color='red', linestyle='--', label='May 13, 2022', linewidth=2)
# ax.grid('both')
# ax.set_ylabel('Snow depth (daily average) in cm')
# fig.savefig('timeseries.png', bbox_inches='tight')


# # plot each year
# fig2, ax2 = plt.subplots(1, 1, figsize=(10, 8))
# for W in data_daily['WY'].unique():
#     tmp = data_daily.loc[data_daily.WY==W]
#     ax2.plot(tmp.wday.values, tmp.SH.values, label='hydr. year '+str(W))
# ax2.axvline(266, color='blue', linestyle='--', label='June 25, 2019', linewidth=1)
# ax2.axvline( 24, color='blue', linestyle='--', label='October 24, 2019', linewidth=1)  # October 24, 2019
# ax2.axvline( 201, color='orange', linestyle='--', label='April 19, 2020', linewidth=1)
# ax2.axvline(20, color='orange', linestyle='--', label='October 20, 2020', linewidth=1)  # October 20, 2020
# ax2.axvline(229, color='green', linestyle='--', label='May 19, 2021', linewidth=1)
# ax2.axvline(19, color='green', linestyle='--', label='October 19, 2021', linewidth=1)  # October 19, 2021
# ax2.axvline(224, color='red', linestyle='--', label='May 13, 2022', linewidth=1)
# ax2.axvline(291, color='red', linestyle='--', label='August 18, 2022', linewidth=1)  # August 18, 2022
# ax2.grid('both')
# ax2.set_ylabel('Snow depth (daily average) in cm')
# ax2.set_xlabel('Days since Oct 1')
# ax2.legend()
# fig2.savefig('wateryears.png', bbox_inches='tight')

# plt.show()



#### NEW TRY ALL SNOW YEARS AFTER EACH OTHER! ########
# Index to date time:
data.index = pd.to_datetime(data.date, format='%d.%m.%Y %H:%M:%S')
data.drop(columns='date', inplace=True)

# Filter data for the years 2019, 2020, 2021, and 2022
data = data['2018-10-01':'2022-09-30']

# Resample to daily mean:
data_daily = data.resample('D').mean()

data_daily['WY'] = data_daily.index.year
data_daily['WY'].loc[data_daily.index.month >= 10] += 1
data_daily['wday'] = data_daily.index.to_series().apply(day_of_water_year)

# Plot time series
fig, ax = plt.subplots(1, 1, figsize=(10, 8))
ax.plot(data_daily.index, data_daily.SH.values)
ax.axvline(dt.datetime(2019, 6, 25), color='red', linestyle='--', label='June 25, 2019', linewidth=2)
ax.axvline(dt.datetime(2020, 4, 19), color='red', linestyle='--', label='April 19, 2020', linewidth=2)
ax.axvline(dt.datetime(2021, 5, 19), color='red', linestyle='--', label='May 19, 2021', linewidth=2)
ax.axvline(dt.datetime(2022, 5, 13), color='red', linestyle='--', label='May 13, 2022', linewidth=2)
ax.grid('both')
ax.set_ylabel('Snow depth (daily average) in cm')
fig.autofmt_xdate()  # Automatically format the x-axis as timestamps
ax.set_title('Time Series Plot')
ax.annotate('Data Source: ' + data_path, xy=(0.5, -0.2), xycoords='axes fraction', fontsize=8, color='gray')
fig.savefig('timeseries.png', bbox_inches='tight')

# Plot each year
fig2, ax2 = plt.subplots(1, 1, figsize=(10, 8))
for W in data_daily['WY'].unique():
    tmp = data_daily.loc[data_daily.WY==W]
    ax2.plot(tmp.index, tmp.SH.values, label='hydr. year '+str(W))
ax2.axvline(dt.datetime(2019, 6, 25), color='blue', linestyle='--', label='June 25, 2019', linewidth=1)
ax2.axvline(dt.datetime(2019, 10, 24), color='blue', linestyle='--', label='October 24, 2019', linewidth=1)  # October 24, 2019
ax2.axvline(dt.datetime(2020, 4, 19), color='orange', linestyle='--', label='April 19, 2020', linewidth=1)
ax2.axvline(dt.datetime(2020, 10, 20), color='orange', linestyle='--', label='October 20, 2020', linewidth=1)  # October 20, 2020
ax2.axvline(dt.datetime(2021, 5, 19), color='green', linestyle='--', label='May 19, 2021', linewidth=1)
ax2.axvline(dt.datetime(2021, 10, 19), color='green', linestyle='--', label='October 19, 2021', linewidth=1)  # October 19, 2021
ax2.axvline(dt.datetime(2022, 5, 13), color='red', linestyle='--', label='May 13, 2022', linewidth=1)
ax2.axvline(dt.datetime(2022, 8, 18), color='red', linestyle='--', label='August 18, 2022', linewidth=1)  # August 18, 2022
ax2.grid('both')
ax2.set_ylabel('Snow depth (daily average) in cm')
fig2.autofmt_xdate()  # Automatically format the x-axis as timestamps
ax2.set_xlabel('Timestamp')
ax2.set_title('Snowhight')
ax2.legend()
ax2.annotate('Data Source: ' + data_path, xy=(0.5, -0.2), xycoords='axes fraction', fontsize=8, color='gray')
fig2.savefig('wateryears.png', bbox_inches='tight')

plt.show()