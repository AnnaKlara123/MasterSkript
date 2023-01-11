import glob
import os, sys

##################### Skript um Datentyp zu verändern.################################
############## um dies zu tun den Pfard in Zeile 7 bez. 23 ändern. auf / vs. \ achten beim Kopieren aus Explorer! 
############## Jeweils gewünschten daten-Typ anpassen in Zeile 12 bzw. 29 

############## Schauen, welche .csv datein schon vorhanden sind und Directory Liste erstellen #############

directory = os.fsencode('C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/Daten/Meteorologie/Jamtalhütte_20210824_20221004')
    
for file in os.listdir(directory):
     filename = os.fsdecode(file)
     if filename.endswith(".csv"):                                  # or filename.endswith(".xlsx"): 
         # print(os.path.join(directory, filename))
         print(filename)
         continue
     else:
         continue
print(directory) 


######## Datentyp gewünscht verändern, Iteration über ganzen Ordner ##################### 

folder = 'C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/Daten/Meteorologie/Jamtalhütte_20210824_20221004'
for filename in os.listdir(folder):
    infilename = os.path.join(folder,filename)
    if not os.path.isfile(infilename): continue
    oldbase = os.path.splitext(filename)
    newname = infilename.replace('.zrx', '.csv')                    # WICHTIG: Wenn es .csv Datei schon in Ordner gibt läuft das Skript nicht!
    output = os.rename(infilename, newname)

print("Output:",output)

print(directory) 
print('done')    