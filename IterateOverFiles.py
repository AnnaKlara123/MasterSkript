import pandas as pd
import glob
import os, sys

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
        ######## Wie mache ich von hier aus weiter, dass ich nacheinander die Datein abarbeite? ##################### 

# for file in glob.iglob(os.path.join('C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/Daten/Meteorologie/Jamtalhuette_20131010_20221128', '*.zrx')):
#     os.rename(filename, filename[:-4] + '.csv')

folder = 'C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/Daten/Meteorologie/Jamtalhütte_20210824_20221004'
for filename in os.listdir(folder):
    infilename = os.path.join(folder,filename)
    if not os.path.isfile(infilename): continue
    oldbase = os.path.splitext(filename)
    newname = infilename.replace('.zrx', '.csv')
    output = os.rename(infilename, newname)

print("Output:",output)

print(directory) 
print('done')    