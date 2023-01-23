import csv
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt


# csv file name
filename = "C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/Daten/Meteorologie/Jamtalhuette_20131010_20221128/Precipitation_test.csv"
data = pd.read_csv(filename, sep=' ', skiprows=825)
print(data)

################ Zeilen in Pandas Einfügen##############
data.insert(1, 'Test', '22')

print(data)



# ########## Listen aus Panda Dataframe auslesen ############## --> Gibts da ne klügere Lösung?

# year = data["YY"].tolist()
# month = data["MM"].tolist()
# day = data["DD"].tolist()
# hour = data["HH"].tolist()
# value = data["Stat1"].tolist()

# print("value=",year[:100])
