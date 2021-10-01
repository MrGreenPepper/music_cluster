import pandas as pd


data = pd.read_csv("D:/MEGAsync/BArbeit/Data/data/small(special)fulldata(so_cl_zo90)_split(2000_0-5).csv", header=None, sep=",")

for entry in data:
    for char in entry:
        print(char)