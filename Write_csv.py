# importing csv module 
# Vorlage: https://www.geeksforgeeks.org/working-csv-files-python/
import csv

# csv file name
filename = "C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/Daten/Meteorologie/jamtalhütte_20200401/GS_test.csv"

 # initializing the titles and rows list
fields = []
rows = []
 
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
print(rows[:10])
 
# #### printing the field names
# # print('Field names are:' + ', '.join(field for field in fields))
 
# # printing first 5 rows
# # print('\nFirst 100 rows are:\n') # \n benutzt man, um zur nächsten Zeile wechseln
# # # print(rows[:100]) # gibt die die Werte ohne Zeilenabsatz aus!
# for row in rows[:100]: 
#     # parsing each column of a row
#     for col in row:
#         # print(col)  # Hier wäre col und row das Selbe nur anders "verpackt"? WHY? 
#         # print(row)
#         # print("%10s"%col), Gibt die Liste ohne ' ' und [] aus
#     #print('\n') # Sorgt nur für Leerzeile 


# ########### CSV WRITE ################

#     # field names
# fieldsout = ['YY',	'MM',	'DD',	'HH',	'Stat1']
 
# # data rows of csv file
# rowsout = [rows]

# # name of csv file
# csvOut = "csvOutputGS.csv"
 
 
# # writing to csv file
# with open(csvOut, 'w') as csvfile:
#     # creating a csv writer object
#     csvwriter = csv.writer(csvfile, delimiter = " ") # Tab angepasst 
     
#     # writing the fields
#     csvwriter.writerow(fieldsout) 
     
#     # writing the data rows
#     csvwriter.writerows(rowsout)


# #csvwriter.to_csv(r'"C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/Daten/Meteorologie/jamtalhütte_20200401/export_GS_test.csv', index=False, header=True)

# print(csvwriter)



    