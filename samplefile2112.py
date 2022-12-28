#Prepair
import numpy as np
import csv
import pandas as pd


#Read data

#datei= open('C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/Daten/Meteorologie/jamtalhütte_20200401/GS_test.csv', 'r')
# csv_reader = csv.reader(datei, delimiter=",")
# print(datei.readlines())

n=100

with open('C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/Daten/Meteorologie/jamtalhütte_20200401/GS_test.csv', 'r') as datei:
   for i in range(n):
        line = next(datei).strip()
        print(line)



####### Jetzt Datum in Jahr, Monat, Tag & Zeit unterteilen! ''#############


# datei['Dates'] = pd.to_datetime(datei['date']).dt.date
# datei['Time'] = pd.to_datetime(datei['date']).dt.time
   
    # for line in datei:
    #  #   print(line[0:10]), # 0-1 bzw. 0-10 Ziffer JE ZEILE werden gedruckt
    #  print(line)

datei.close()