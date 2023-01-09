###### Import for Python #########

import csv
import pandas as pd
import numpy as np

####### csv file name  #####
filename = "C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/Daten/Meteorologie/jamtalhütte_20200401/N1m_test.csv"
###### Hier später über alle Files in einem Ordner iterieren lassen! ####### --> Siehe Python Kurs 

###### initializing the titles and rows list #####
fields = []
rows = []
yy = []
mm = []
dd = []
hh= []
Stat1 = []
 
###### reading csv file ########

with open(filename, 'r') as csvfile:                                       # file name vorher bestimmmt
    # creating a csv reader object
    csvreader = csv.reader(csvfile, delimiter = " ")
    for row in csvreader:
        rows.append(row)                                                   # Raws werden der vorher erstellten Liste rows = [ ] nacheinander hinzugefügt

######## get Date & Time ###########

col = []

for row in rows[:300]: 
    # parsing each column of a row
    for col in row:
        col = col.replace(",", ".")                                        # replace comma with points
        yy.append(col[:4])
        mm.append(col[4:6])
        dd.append(col[6:8])
        hh.append(col[8:12]) 
        Stat1.append(col[15:])


####### Aus Str. Int machen #######
yy = [int(x) for x in yy]
mm = [int(x) for x in mm]
dd = [int(x) for x in dd]
hh= [int(x) for x in hh]
Stat1 = [float(x) for x in Stat1]
 
                # print("type of dd element is:", type(Stat1[1])) ---> Elemente werden als String eingelesen
                # yyArray = np.array(yy, dtype=int)
                # Stat1Array = np.array(Stat1, dtype=float)


######## Summe berechnen  #########

step = 10
sub_lists = []
averages = []
sums = []

##### Unterlisten für 10er Steps erstellen ########
for i, _ in enumerate(Stat1[::step]):                                           # Sagt es soll von 0-9 über den Code laufen
    sub_list = Stat1[i*10:] if (i+1)*10 > len(Stat1) else Stat1[i*10:(i+1)*10]  # Condition if the len(my_list) % step != 0
    sub_lists.append(sub_list)
    lst = sub_list
    #print("Liste ist:",lst)
    Sum = sum(lst)                                                              # Use Sum Funcition  (implementiert in python)
    #print("sum is:", Sum)
    sums.append(Sum) 
     
# print("the average of GS per hour is:", averages)
print("the sum of NS1 per hour is:", sums)


####### ----> Next Step: csv file schreiben, welches nur den Durchschnittswert pro Stunde enthält. Liste wird hierdurch kürzer.
####### Falsche Messwerte durch NoData Werte ersetzen
####### Herausfinden wie WaSiM kürzere zeitabstände berechnet (S.282 im Skript). Schauen wieviel davon WaSim Selbst rechnen kann.
####### über mehrere Datensätze in Ordner iterieren (alle .csv  oder .ex. daten) mithife von If - loop
####### Niederschläge müssen summiert werden, daher formel für Sum erstellen
#######