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
     
    # extracting field names/Headers through first row 
    fields = next(csvreader)
 
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

for row in rows[:100]: 
    # parsing each column of a row
    for col in row:
                        #print(col)  # Hier wäre col und row das Selbe nur anders "verpackt"? WHY? 
                        # print(row)
                        #print("%10s"%col)  #Gibt die Liste ohne ' ' und [] aus
                        #print('\n') # Sorgt nur für Leerzeile 
        #yy= (col[:4]) ist nur für erste Zeile durch .append liste erzeugen
        yy.append(col[:4])
        mm.append(col[4:6])
        dd.append(col[6:8])
        hh.append(col[8:12]) # WICHTIG: Hier nochmal genau schauen, wie ich das in Min umrechne!
        Stat1.append(col[15:]) # Wie bekomme ich ";" weg?
        #print('stat1=',Stat1)



########### CSV WRITE ################

    # field names
fieldsout = ['YY',	'MM',	'DD',	'HH',	'Stat1']
 
# data rows of csv file
rowsout = [yy, mm, dd,hh, Stat1]

# name of csv file
csvOut = "csvOutputGS.csv"
 
 
# writing to csv file
with open(csvOut, 'w') as csvfile:
    # creating a csv writer object
    csvwriter = csv.writer(csvfile, delimiter = " ") # Tab angepasst 
     
    # writing the fields
    csvwriter.writerow(fieldsout)
     
    # writing the data rows
    csvwriter.writerows(list(zip(*[yy, mm, dd, hh, Stat1]))) # Setzt die Liste in richtiges Tabellenformat um "*" WICHTIG! 

########## converting csv file to data frame ################


df  = pd.DataFrame(list(zip(yy,mm,dd,hh, Stat1)), columns = ['YY',	'MM',	'DD',	'HH',	'Stat1'])



# lst = [list(zip(*[yy, mm, dd, hh, Stat1]))]
# columns = ['YY',	'MM',	'DD',	'HH',	'Stat1']
# df  = pd.DataFrame(lst,columns )
print(df)

#print(csvwriter)

##### NEXT: die Headerzeilen mit Koordinate & Höhe etc. hinzufügen! ######


    