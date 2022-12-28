#Prepair
import numpy as np
import csv

#Read data

datei= open('C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/Daten/Meteorologie/jamtalhütte_20200401/GS.csv', 'r')
csv_reader = csv.reader(datei, delimiter=",")
print(datei.readlines())


# for row in csv_reader:
#    print(row)
# datei.close()
