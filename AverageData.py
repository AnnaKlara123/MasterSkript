###### Import for Python #########

import csv
import pandas as pd
import numpy as np
import math

####### csv file name  #####
filename = "C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/Daten/Meteorologie/jamtalhütte_20200401/GS_test2.csv"
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

with open(filename, 'r') as csvfile:                            # file name vorher bestimmmt
    # creating a csv reader object
    csvreader = csv.reader(csvfile, delimiter = " ")
    for row in csvreader:
        rows.append(row)                                        # Raws werden der vorher erstellten Liste rows = [ ] nacheinander hinzugefügt

######## get Date & Time ###########

col = []

for row in rows: 
    # parsing each column of a row
    for col in row:
        col = col.replace(",", ".")                             # replace comma with points
        yy.append(col[:4])
        mm.append(col[4:6])
        dd.append(col[6:8])
        hh.append(col[8:12])                                    # WICHTIG: Hier nochmal genau schauen, wie ich das in Min umrechne!
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

# Replace Values in a List using For Loop
  
for i in range(len(Stat1)):
  
    # replace hardik with shardul
    if Stat1[i] == -8.81057:
        Stat1[i] = -9999
    if Stat1[i] == 8.81057:
        Stat1[i] = -9999

for i in range(len(Stat1)):
  
    # replace hardik with shardul
    if Stat1[i] == -9999:
        Stat1[i] = np.nan        
#print("Liste Stat1 = ", Stat1)  

######## Function for Average  #########
def Average(lst):
    return sum(lst) / len(lst) 

            ####### Steps for calulation ######

stepHour = 10
stepDay = 287
sub_lists = []
averages = []

##### Unterlisten für 10er Steps erstellen ########
for i, _ in enumerate(Stat1[::stepDay]):                                           # Sagt es soll von 0-9 über den Code laufen --> Anpassen
    sub_list = Stat1[i*10:] if (i+1)*10 > len(Stat1) else Stat1[i*10:(i+1)*10]  # Condition if the len(my_list) % step != 0
    #### quelle: https://stackoverflow.com/questions/39814034/how-do-i-get-the-average-of-every-10-numbers-in-list-in-python ###
    sub_lists.append(sub_list)
    #### Driver Code
    lst = sub_list
    #print("Liste ist:",lst)
    average = round(Average(lst), 1)
    #print("average ist:", average)
    averages.append(average)  
print("the average of GS per hour is:", averages)

print("Average length ist:", len(averages))

################# TO Dos #############################
####### ----> Next Step: csv file schreiben, welches nur den Durchschnittswert pro Stunde enthält. Liste wird hierdurch kürzer.
####### Falsche Messwerte durch NoData Werte ersetzen
####### Herausfinden wie WaSiM kürzere zeitabstände berechnet (S.282 im Skript). Schauen wieviel davon WaSim Selbst rechnen kann.
####### über mehrere Datensätze in Ordner iterieren (alle .csv  oder .ex. daten) mithife von If - loop
####### Niederschläge müssen summiert werden, daher formel für Sum erstellen
####### Auf 1 Nachkommeastelle Runden
########################################################