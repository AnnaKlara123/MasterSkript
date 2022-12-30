#Prepair
import numpy as np
import csv
import pandas as pd


#Read data

datei= open('C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/Daten/Meteorologie/jamtalhütte_20200401/GS_test.csv', 'r')
csv_reader = csv.reader(datei, delimiter=" ")
for line in csv_reader:     # Hier wird CSV Datei als Liste aufgelistet: 
#Each line is a list of values. To access each value, you use the square bracket notation []. The first value has an index of 0. The second value has an index of 1, and so on.
        print(line)
  
# n=100

# with open('C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/Daten/Meteorologie/jamtalhütte_20200401/GS_test.csv', 'r') as datei:
#    for i in range(n):
#         line = next(datei).strip()
#         print(line)


####### Jetzt Datum in Jahr, Monat, Tag & Zeit unterteilen! ''#############


# datei['Dates'] = pd.to_datetime(datei['date']).dt.date
# datei['Time'] = pd.to_datetime(datei['date']).dt.time
   
    # for line in datei:
    #  #   print(line[0:10]), # 0-1 bzw. 0-10 Ziffer JE ZEILE werden gedruckt
    #  print(line)

datei.close()