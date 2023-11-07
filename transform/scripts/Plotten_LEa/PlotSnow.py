import numpy as np
import pandas as pd
import datetime as dt

import matplotlib.pyplot as plt


def day_of_water_year(some_date):
    # Get the date of the previous October 1st
    water_year_start_date = dt.datetime(some_date.year + some_date.month // 10 - 1, 10, 1)
    
    # Return the number of days since then
    return (some_date - water_year_start_date).days + 1



# read file: 
data = pd.read_csv('lwd_Tirol_15140917-HS-Basisganglinie.csv', delimiter=';', na_values='---', skiprows=15, decimal=",",
                      names=['date', 'SH'], encoding='unicode_escape')
# index to date time:
data.index = pd.to_datetime(data.date, format='%d.%m.%Y %H:%M:%S')
data.drop(columns='date', inplace=True)
print(data)

# Filter data for the years 2019, 2020, 2021, and 2022
data = data['2018-10-01':'2022-09-30']

# resample to daily mean:
data_daily = data.resample('D').mean()


data_daily['WY'] = data_daily.index.year
data_daily['WY'].loc[data_daily.index.month >= 10] += 1
data_daily['wday'] = data_daily.index.to_series().apply(day_of_water_year)


# plot time series
fig, ax = plt.subplots(1, 1, figsize=(10, 8))
ax.plot(data_daily.index.values, data_daily.SH.values)
ax.grid('both')
ax.set_ylabel('Snow depth (daily average) in cm')
fig.savefig('timeseries.png', bbox_inches='tight')


# plot each year
fig2, ax2 = plt.subplots(1, 1, figsize=(10, 8))
for W in data_daily['WY'].unique():
    tmp = data_daily.loc[data_daily.WY==W]
    ax2.plot(tmp.wday.values, tmp.SH.values, label='hydr. year '+str(W))
ax2.grid('both')
ax2.set_ylabel('Snow depth (daily average) in cm')
ax2.set_xlabel('Days since Oct 1')
ax2.legend()
fig2.savefig('wateryears.png', bbox_inches='tight')

plt.show()

