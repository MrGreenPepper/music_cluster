import pandas as pd
import os
import re
import random

# Speicherort
data_dictionary = "D:/MEGASync/BArbeit/MusicCluster/Data/rawData"
# data_dictionary = "/home/nox/MEGAsync/BArbeit/MusicCluster/Data/rawData"
os.chdir(data_dictionary)

# Ausgangs-Daten-Konfiguration
dataset = "fulldata"
dataname = "fulldata_11_4-1_sorted_clean_zeroone_90.csv"
test = False
sorted = True                                       # wurde vorsortiert?
clean = True                                       # Wurde er bereinigt?
zeroone = 90                                         # 0/1 ReinheitsMaß
info_rows = 13                                   # Zeilen die am Ende entfernt werden müssen


# Wie soll eingeteilt werden
rmd = True                                      # Daten werden zufällig aus der gesamten Menge gezogen
split_length = [True, 2000]                     # Wenn True wird anhand der Zahl der Datensatz in eben diese Größen aufgeteilt
split_parts = 2


# Namen zusammenfügen
sconfig = ""
origin_filename = dataset



config = ""
if test is True:
    origin_filename += "_test_"
if sorted is True:
    config += "(so"
if clean is True:
    config += "_cl"
if zeroone > 0:
    config += "_zo" + str(zeroone)
#load_filename = sconfig + origin_filename + config + ")"+  ".csv"
#load_filename = sconfig + dataname
load_filename = "fulldata_11_4-1_sorted_clean_zeroone_90.csv"

# Einlesen der Datei
fulldata = pd.read_csv(load_filename)
fulldata = pd.DataFrame(fulldata)

print(fulldata.shape, "davon Info-Zeilen: ", info_rows)
fulldata_rows, fulldata_columns = fulldata.shape
fulldata_rows -= info_rows

if split_length[0] is True:
    split_parts = fulldata_rows // split_length[1]
else:
    split_length[1] = fulldata_rows // split_parts

rest_length = fulldata_rows % split_length[1]


# Erstellt eine Liste mit der Länge = Zeilenanzahl der Original-Datei,
# jeder Eintrag symbolisiert die Nummer der Split Datei in die der jeweilige Eintrag dann eingeordnet wird
split_division = []
while len(split_division) < fulldata_rows:

    rmd_s = random.randint(0, (split_parts-1))
    if split_division.count(rmd_s) < split_length[1]:               # stellt sicher das alle Teile gleich groß werden
        split_division.append(rmd_s)                                # IndexNummer der Liste = Index Nummer Lied --> Eintrag bei der jeweiligen Indexnummer bestimmt dann zugewiesenen Split
    elif split_division.count(split_parts) < rest_length:           # solange der Rest noch nicht voll ist wird unter Umständen darauf ausgewichen
        split_division.append(split_parts)

splitname = str
splitname = "splitdata_" + "(" + str(split_length[1]) + "-" + str(fulldata_rows) + ")" + ".csv"
splitdata = pd.DataFrame(split_division)

# print(splitdata)
print(splitname)
splitdata.to_csv(splitname)