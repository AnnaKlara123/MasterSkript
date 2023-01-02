# importing csv module 
# Vorlage: https://www.geeksforgeeks.org/working-csv-files-python/
import csv
 
# csv file name
filename = "C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/Daten/Meteorologie/jamtalhütte_20200401/GS_test.csv"

 # initializing the titles and rows list
fields = []
rows = []
yy = []
mm = []
dd = []
hh= []
 
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

for row in rows[:100]: 
    # parsing each column of a row
    for col in row:
                        #print(col)  # Hier wäre col und row das Selbe nur anders "verpackt"? WHY? 
                        # print(row)
                        #print("%10s"%col)  #Gibt die Liste ohne ' ' und [] aus
                        #print('\n') # Sorgt nur für Leerzeile 
        yy= (col[:4])
        mm = (col[4:6])
        dd = (col[6:8])
        hh = (col[8:12]) # WICHTIG: Hier nochmal genau schauen, wie ich das in Min umrechne!
        
        # print('yy=', yy,'mm=',mm,'dd=',dd, 'hh=',hh)

    