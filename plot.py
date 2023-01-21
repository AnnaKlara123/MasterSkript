import csv
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt


# csv file name
filename = "C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/GitHubMasterSkripts/dfCSVfile2013cut.csv"
data = pd.read_csv(filename, sep=' ', skiprows=5)

year = data["YY"].tolist()
value = data["Stat1"].tolist()

print("year=",year)

###### plot data Winter 2013/14 #######

plt.plot(year, value)	
#plt.plot(hh, Stat1)


plt.title("Plot Stat1 data")
plt.xlabel("Time")
plt.ylabel("Value")

plt.show()