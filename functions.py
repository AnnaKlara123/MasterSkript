# importing csv module 
# Vorlage: https://www.kdnuggets.com/2020/08/5-different-ways-load-data-python.html
import csv
import pandas as pd

def read_csv(filename):
    fields = []
    rows = []
    yy = []
    mm = []
    dd = []
    hh= []
    Stat1 = []
    checkcol = False
    with open(filename, 'r') as csvfile:
                # creating a csv reader object
        csvreader = csv.reader(csvfile, delimiter = " ")
 
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

        ########### CSV WRITE ################

        ############## Dataframe erstellen #########################

        ### Headerliste erstellen ####  -----> \ Als Zeilenumbruch im Code genutzt
        df  = pd.DataFrame(list(zip(yy,mm,dd,hh, Stat1)))           # Dataframe erstellen. 
        #df.columns = headerList  
        print(df)
        return df   