# my_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
import csv
import pandas as pd
import numpy as np

# csv file name
filename = "C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/Daten/Meteorologie/jamtalhütte_20200401/GS_test2.csv"
###### Hier später über alle Files in einem Ordner iterieren lassen! ####### --> Siehe Python Kurs 

# initializing the titles and rows list
fields = []
rows = []
yy = []
mm = []
dd = []
hh= []
Stat1 = []
 
# reading csv file
with open(filename, 'r') as csvfile:
    # creating a csv reader object
    csvreader = csv.reader(csvfile, delimiter = " ")
    for row in csvreader:
        rows.append(row) # Raws werden der vorher erstellten Liste rows = [ ] nacheinander hinzugefügt

######## get Date & Time ###########

col = []

for row in rows[:300]: 
    # parsing each column of a row
    for col in row:
        col = col.replace(",", ".")  # replace comma with points
        yy.append(col[:4])
        mm.append(col[4:6])
        dd.append(col[6:8])
        hh.append(col[8:12]) # WICHTIG: Hier nochmal genau schauen, wie ich das in Min umrechne!
        Stat1.append(col[15:])

yy = [int(x) for x in yy]
mm = [int(x) for x in mm]
dd = [int(x) for x in dd]
hh= [int(x) for x in hh]
Stat1 = [float(x) for x in Stat1]
 
# print("type of dd element is:", type(Stat1[1])) ---> Elemente werden als String eingelesen
# yyArray = np.array(yy, dtype=int)
# Stat1Array = np.array(Stat1, dtype=float)

def Average(lst):
    return sum(lst) / len(lst) 

step = 10
sub_lists = []
averages = []

for i, _ in enumerate(Stat1[::step]):               # Sagt es soll von 0-9 über den Code laufen
    sub_list = Stat1[i*10:] if (i+1)*10 > len(Stat1) else Stat1[i*10:(i+1)*10]  # Condition if the len(my_list) % step != 0
    sub_lists.append(sub_list)
    #### Driver Code
    lst = sub_list
    print("Liste ist:",lst)
    average = Average(lst) 
    print("average ist:", average)
    averages.append(average)  
print("the average of GS per hour is:", averages)
#  sub_listsarray= np.array(sub_lists, dtype=float)





#print('Sublists = ', sub_lists)