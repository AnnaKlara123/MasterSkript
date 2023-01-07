# importing csv module 
# Vorlage: https://www.geeksforgeeks.org/working-csv-files-python/
import csv
import pandas as pd

# csv file name
filename = "C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/Daten/Meteorologie/jamtalhütte_20200401/GS_test2.csv"

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
     
    ## extracting field names/Headers through first row 
    ##fields = next(csvreader)
 
    # extracting each data row one by one
    for row in csvreader:
        rows.append(row) 

######## get Date & Time ###########

col = []

for row in rows[:300]: 
    # parsing each column of a row
    for col in row:
        #yy= (col[:4]) ist nur für erste Zeile durch .append liste erzeugen
        col = col.replace(",", ".")  # replace comma with points
        yy.append(col[:4])
        mm.append(col[4:6])
        dd.append(col[6:8])
        hh.append(col[8:12]) # WICHTIG: Hier nochmal genau schauen, wie ich das in Min umrechne!
        Stat1.append(col[15:]) 



############## Dataframe erstellen #########################

headerList = ['YY',	'MM',	'DD',	'HH',	'Stat1' ]       # Überschriften festlegen
df  = pd.DataFrame(list(zip(yy,mm,dd,hh, Stat1)))           # Dataframe erstellen. 
df.columns = headerList                                     # Header df hinzufügen

#### ALternativ:  df  = pd.DataFrame(list(zip(yy,mm,dd,hh, Stat1)), columns = ['YY',	'MM',	'DD',	'HH',	'Stat1'])  ###
df.to_csv("dfCSVfile.csv", sep=' ', header=headerList, index=False)
 
print(df)