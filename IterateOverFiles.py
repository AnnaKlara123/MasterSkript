import os
directory = 'C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/Daten/Meteorologie/jamtalhütte_20200401'

for filename in os.listdir(directory):
    if filename.endswith(".csv"):
     filename = os.path.join(directory, filename)

    if os.path.isfile (filename):
        print("files in path are:", filename)
        


# import os

# directory = os.path.join('C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/Daten/Meteorologie/jamtalhütte_20200401')
# for root,dirs,files in os.walk(directory):
#     for file in files:
#        if file.endswith(" "):
#            f=open(file, 'r')
#            #  perform calculation
#            print(f)
#            f.close()
