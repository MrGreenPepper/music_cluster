import pandas as pd
import analysis
import re
import os
import numpy as np
import math
import data_cscale_methods
from sklearn import preprocessing
import data_small_class


data_file = "fulldata_11_4-1_sorted_clean_zeroone_90.csv"
filename = re.sub("\.csv", "", data_file)
#datadir = "/home/nox/MEGAsync/BArbeit/MusicCluster/Data/rawData"
datadir = "D:/MEGAsync/BArbeit/Data/rawData/"

small = data_small_class.SmallData(data_file, datadir)


# für alle
small.norm = True                                 # normiert Zahlenreichweite zwischen 0 und 1
small.gross_weight = (True, 1, True)                    # die einzelnen Bereiche werden gleich gewichtet, 3.  if true -- jeder einzelne Eintrag false-> bereich

                                                    # 1. Zahl: auf wieviel jeder Abschnitt
# für normal und timeline                           # 2. Zahl:  0--> Gewichtung wie ein eintrag   1 --> keine Längen Skalierung
small.interval_scale = (False, 1, 1)                # jedes Intervall, egal welcher Länge, bekommt die Gewichtung von 5 (Durchschnitt-Std * 5)
small.tonal = (True, 1, 1)                         # Töme und ihre Akkorde gesonderst skalieren

# für specials
small.single_scale = (True, 1)                    # alle einzelnen Einträge bekommen die Gewichtung von [1]




small.create()

#print(small.origin_fulldata.keys())
small.filename = "full_see_data" + small.filename

small.save()