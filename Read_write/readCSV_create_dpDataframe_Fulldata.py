# importing csv module 
# Vorlage: https://www.geeksforgeeks.org/working-csv-files-python/
import csv
import pandas as pd
import numpy as np

# csv file name
filename = "C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/Daten/Meteorologie/Jamtalhuette_20131010_20221128/Precipitation_test.csv"

# initializing the titles and rows list
fields = []
rows = []
date = []                                                     # Datetime 
yy = []
mm = []
dd = []
hh= []
minutes = []
Stat1 = []
 
# reading csv file
with open(filename, 'r') as csvfile:
    # creating a csv reader object
    csvreader = csv.reader(csvfile, delimiter = "\t")    # mit \t kann ich je Zeile die ersten 4 Zeichen einlesen, jedoch werden Datum & Sat.WErt nich getrennt eingelesen
 
    # extracting each data row one by one
    for row in csvreader:
        rows.append(row) 

#print(rows)

####### get Date & Time ###########
# def datetime(rows):
#     return [item[0] for item in rows]

# def value(rows):
#     return [item[1] for item in rows]

col = []

for row in rows[815:200000]: 
    #print(datetime(rows))
    #print(value(rows))
    # parsing each column of a row
    for col in row:
        #yy= (col[:4]) # ist nur für erste Zeile durch .append liste erzeugen
        #print(yy)
        date.append(col[:8])                               # Datetime vorbereiten 
        yy.append(col[:4])
        mm.append(col[4:6])
        dd.append(col[6:8])
        hh.append(col[8:12])                              # WICHTIG: Hier nochmal genau schauen, wie ich das in Min umrechne!
        Stat1.append(col[15:]) 
            ########### Ist es Sinnvoll die Listen in Arrays zu ändern? ############
            ## yy = np.array((yy))    
            ## Stat1 = np.array((Stat1))


####### Aus Str. Int machen #######
yy = [int(x) for x in yy]
mm = [int(x) for x in mm]
dd = [int(x) for x in dd]
hh= [int(x) for x in hh]

####### minuten aus hh berrechnen ############

Stat1 = [float(x) for x in Stat1]


########### Replace NoData Values in a List using For Loop ###########
  
for i in range(len(Stat1)):
  
    # replace hardik with shardul
    if Stat1[i] == -8.81057:
        Stat1[i] = -9999
    if Stat1[i] == -777:
        Stat1[i] = -9999    
    if Stat1[i] == 8.81057:
        Stat1[i] = -9999
#print("Liste Stat1 = ", Stat1)  

             
########### CSV WRITE ################

###### Infos zur Struktur:  ##########
            ## Row 1: comment
            ## Row 2: after „yy mm dd hh“: altitudes for each station (int or float ), basin area for hydrologic data
            ## Row 3: after „yy mm dd hh“: x-coordinates of the stations (integer or floating point values)
            ## Row 4: after „yy mm dd hh“: y-coordinates of the stations (integer or floating point values)
            ## Row 5: after „yy mm dd hh“: short identifier for each station e.g. 6-chars
            ## beginning with Row 6: actual date (e.g. 1984 01 01 24), then for each station one value (real
            ## or integer) separated by at least one space or tab stop.


hight = ('hight', 2, 3)      # Höhe einfügen
Xcoord= ('xcoord', 2, 3)    # Koordinaten einfügen! 
Ycoord=  ('ycoord', 2, 3) 
StatIdentefier = ('stationidentefyer',2,3) # Identefier vergeben
Stat = [Stat1, 'Stat2', 'Stat3' ]



############## Dataframe erstellen #########################

### Headerliste erstellen ####  -----> \ Als Zeilenumbruch im Code genutzt
headerList = [['YY',	'MM',	'DD',	'HH',	'Stat1' , 'date'], ['YY',	'MM',	'DD',	'HH',  hight[0], 'date'], \
['YY',	'MM',	'DD',	'HH', Xcoord[0],'date'], ['YY',	'MM',	'DD',	'HH',Ycoord[0],'date' ] ,['YY',	'MM',	'DD',	'HH',  StatIdentefier[0],'date'],\
['YY',	'MM',	'DD',	'HH',	'Stat1', 'date' ] ]       # Überschriften festlegen
df  = pd.DataFrame(list(zip(yy,mm,dd,hh, Stat1, date)), columns = ['YY',	'MM',	'DD',	'HH',	'Stat1', 'date'])          # Dataframe erstellen. (date durch: 'YY',	'MM',	'DD' ersetzen )    
df.columns = headerList                                                                       # Header df hinzufügen#
# df['date'] = pd.to_datetime(df['date'])                                                        # Date time hinzufügen
                                                                                                # False Werte durch -9999 NoData ersetzt                                                   

# df["YY"] = df['YY'].astype(int)
# df["MM"] = df['MM'].astype(int)
# df["DD"] = df['DD'].astype(int)
# df["HH"] = df['HH'].astype(int)
# df["Stat1"] = df['Stat1'].astype(float) ##### --> WaSiM nimmt nur Integers. Wie mache ich das dann hier?


############ sort after year ##############

# for year in yy:
#     if yy == 2013:
#        df.to_csv("dfCSVfilefullnew2013.csv", sep=' ', index=False)
#     elif yy == 2014:
#         df.to_csv("dfCSVfilefullnew2014.csv", sep=' ', index=False)
#     else:

#### ALternativ:  df  = pd.DataFrame(list(zip(yy,mm,dd,hh, Stat1)), columns = ['YY',	'MM',	'DD',	'HH',	'Stat1'])  ###
df.to_csv("dfCSVfile2013cut.csv", sep=' ', index=False)

print(df)
# print(df)


######   df.round(1) ----> Hier auf 1 Nachkommastelle Runden! ############