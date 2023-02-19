import csv
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt


# csv file einlesen als PD
filename = "C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/Daten/Meteorologie/Jamtalhuette_20131010_20221128/Precipitation_test.csv"
df = pd.read_csv(filename, sep=' ', skiprows=825)
print(df)

################ Zeilen in Pandas Einfügen##############
#data.insert(1, 'Test', '22')   # (Spalte, Header, Value)


indices = [0,4,6,8,10,14]
for i in df.index: 
    parts = [df.at[i:j] for i,j in zip(indices, indices[1:]+[None])]  # für jede Zeile stehen Parts(Datum/Zeit) für Jahr, Tag, monat, H, Min

print(df)



# ########## Listen aus Panda Dataframe auslesen ############## --> Gibts da ne klügere Lösung?

# year = data["YY"].tolist()
# month = data["MM"].tolist()
# day = data["DD"].tolist()
# hour = data["HH"].tolist()
# value = data["Stat1"].tolist()

# print("value=",year[:100])
