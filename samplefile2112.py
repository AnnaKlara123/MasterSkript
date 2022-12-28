#Prepair
import numpy as np
import csv

#Read data

# datei= open('C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/Daten/Meteorologie/jamtalhütte_20200401/GS.csv', 'r')
# csv_reader = csv.reader(datei, delimiter=",")
# print(datei.readlines())


# for row in csv_reader:
#    print(row)
# datei.close()

n=100

with open('C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/Daten/Meteorologie/jamtalhütte_20200401/GS.csv', 'r') as datei:
   for i in range(n):
        line = next(datei).strip()
        print(line)
   
   
   
    # for line in datei:
    #  #   print(line[0:10]), # 0-1 bzw. 0-10 Ziffer JE ZEILE werden gedruckt
    #  print(line)