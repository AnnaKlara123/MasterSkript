import csv
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt


# csv file name
filename = "C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/GitHubMasterSkripts/dfCSVfile2013cut.csv"
data = pd.read_csv(filename, sep=' ', skiprows=5)
print(data)

########## Listen aus Panda Dataframe auslesen ############## --> Gibts da ne klügere Lösung?

year = data["YY"].tolist()
month = data["MM"].tolist()
day = data["DD"].tolist()
hour = data["HH"].tolist()
value = data["Stat1"].tolist()

print("value=",month[:100])



###### plot data Winter 2013/14 #######

plt.plot(month, value)	
#plt.plot(hh, Stat1)


plt.title("Plot Stat1 data")
plt.xlabel("Time")
plt.ylabel("Value")

plt.show()