# importing csv module 
# Vorlage: https://www.geeksforgeeks.org/working-csv-files-python/
import csv
import pandas as pd

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
     
    ## extracting field names/Headers through first row 
    ##fields = next(csvreader)
 
    # extracting each data row one by one
    for row in csvreader:
        rows.append(row) # Raws werden der vorher erstellten Liste rows = [ ] nacheinander hinzugefügt

                        #get total number of rows
                        #print("Total no. of rows: %d"%(csvreader.line_num))
 
                        #### printing the field names
                        # print('Field names are:' + ', '.join(field for field in fields))
                        
                        # printing first 5 rows
                        # print('\nFirst 100 rows are:\n') # \n benutzt man, um zur nächsten Zeile wechseln
                        # # print(rows[:100]) # gibt die die Werte ohne Zeilenabsatz aus!

######## get Date & Time ###########

col = []

for row in rows[:300]: 
    # parsing each column of a row
    for col in row:
                        #print(col)  # Hier wäre col und row das Selbe nur anders "verpackt"? WHY? 
                        # print(row)
                        #print("%10s"%col)  #Gibt die Liste ohne ' ' und [] aus
                        #print('\n') # Sorgt nur für Leerzeile 
        #yy= (col[:4]) ist nur für erste Zeile durch .append liste erzeugen
        col = col.replace(",", ".")  # replace comma with points
        yy.append(col[:4])
        mm.append(col[4:6])
        dd.append(col[6:8])
        hh.append(col[8:12]) # WICHTIG: Hier nochmal genau schauen, wie ich das in Min umrechne!
        Stat1.append(col[15:]) # Wie bekomme ich ";" weg?
        #print('stat1=',Stat1)
 

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



# initialise data dictionary.
data_dict = {'YY': yy,
              
             'MM': mm,
              
             'DD': dd,
              
             'HH': hh,
              
             'Stat1': Stat1}

# adding header
headerList = [['YY',	'MM',	'DD',	'HH',	'Stat1' ], ['YY',	'MM',	'DD',	'HH',  hight[0]], \
['YY',	'MM',	'DD',	'HH', Xcoord[0]], ['YY',	'MM',	'DD',	'HH',Ycoord[0] ] ,['YY',	'MM',	'DD',	'HH',  StatIdentefier[0]],\
['YY',	'MM',	'DD',	'HH',	'Stat1' ] ]      

# Create DataFrame
data = pd.DataFrame(data_dict)
data.columns =headerList
 
# Write to CSV file
data.to_csv("dpCSVfile.csv", sep=' ', index=False)
 
# Print the output.
print(data)