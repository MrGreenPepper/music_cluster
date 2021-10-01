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
sorted = True  # wurde vorsortiert?
clean = True  # Wurde er bereinigt?
zeroone = 90  # 0/1 ReinheitsMaß
info_rows = 0  # Zeilen die am Ende entfernt werden müssen

# Wie soll eingeteilt werden
rmd = True  # Daten werden zufällig aus der gesamten Menge gezogen
split_length = [True, 5000]  # Wenn True wird anhand der Zahl der Datensatz in eben diese Größen aufgeteilt
split_parts = 2

# Namen zusammenfügen
origin_filename = dataset

config = ""
if test is True:
    origin_filename += "_test_"
if sorted is True:
    config += "so"
if clean is True:
    config += "_cl"
if zeroone > 0:
    config += "_zo" + str(zeroone)
# load_filename = sconfig + origin_filename + config + ")"+  ".csv"
# load_filename = sconfig + dataname

filename_loader = ["small(timeline)fulldata_11_4-1_sorted_clean_zeroone_90.csv"
   ]

# ToDo: "small(single_timeline)fulldata_11_4-1_sorted_clean_zeroone_90.csv", ...
# Done:
# "fulldata_11_4-1_sorted_clean_zeroone_90.csv"
# "small(single)fulldata_11_4-1_sorted_clean_zeroone_90.csv",
#                    "small(tonal)fulldata_11_4-1_sorted_clean_zeroone_90.csv",
#                    "small(timeline)fulldata_11_4-1_sorted_clean_zeroone_90.csv",
#                    "small(normal)fulldata_11_4-1_sorted_clean_zeroone_90.csv",
#                    "small(string)fulldata_11_4-1_sorted_clean_zeroone_90.csv",
#                    "small(single_string)fulldata_11_4-1_sorted_clean_zeroone_90.csv",
#                    "small(single_normal)fulldata_11_4-1_sorted_clean_zeroone_90.csv",
#                    "small(single_tonal)fulldata_11_4-1_sorted_clean_zeroone_90.csv",
#                    "small(single_normal_tonal)fulldata_11_4-1_sorted_clean_zeroone_90.csv",
#                    "small(single_string_tonal)fulldata_11_4-1_sorted_clean_zeroone_90.csv"
# "small(normal_string)fulldata_11_4-1_sorted_clean_zeroone_90.csv"
#"small(single_string_normal)fulldata_11_4-1_sorted_clean_zeroone_90.csv"
for load_filename in filename_loader:

    # Einlesen der Datei
    fulldata = pd.read_csv(load_filename)
    fulldata = pd.DataFrame(fulldata)

    print(fulldata.shape, "davon Info-Zeilen: ", info_rows)
    fulldata_rows, fulldata_columns = fulldata.shape
    fulldata_rows -= info_rows

    # Lade Split-Einteilung
    splitname = str
    splitname = "splitdata_" + "(" + str(split_length[1]) + "-" + str(fulldata_rows) + ")" + ".csv"
    splitdata = pd.read_csv(splitname)
    split_division_raw = splitdata.values.tolist()

    if split_length[0] is True:
        split_parts = fulldata_rows // split_length[1]
    else:
        split_length[1] = fulldata_rows // split_parts

    rest_length = fulldata_rows % split_length[1]

    split_division = []
    for entry in split_division_raw:
        split_division.append(entry[1])

    filename = re.sub("_11_4-1_sorted_clean_zeroone_90.csv", "", load_filename)

    for x in range(0, split_parts + 1):

        split_allocation = []
        for n, splitnr in enumerate(split_division, 0):
            if splitnr == x:
                split_allocation.append(n)

        if x == split_parts:
            save_filename = filename + "(" + config + ")"
            save_filename += "_rsplit" + "(" + str(split_length[1]) + "_" + str(x) + "-" + str(
                split_parts) + ")" + ".csv"

            rest_data = pd.DataFrame(fulldata.iloc[split_allocation])
            rest_data.to_csv(save_filename)
            print(rest_data.shape, "-", save_filename)

        else:
            save_filename = filename + "(" + config + ")"
            save_filename += "_split" + "(" + str(split_length[1]) + "_" + str(x) + "-" + str(
                split_parts) + ")" + ".csv"

            split_data = pd.DataFrame(fulldata.iloc[split_allocation])
            split_data.to_csv(save_filename)
            print(split_data.shape, "-", save_filename)
