import pandas as pd

rows = pd.read_csv("D:/MEGASync/BArbeit/Data/expert_forcode.csv", sep=";")
rows = rows.iloc[: ,1]

data = pd.read_csv("D:/MEGASync/BArbeit/Data/data/small(single_normal_tonal)fulldata(so_cl_zo90)_split(2000_0-5).csv")

data_selected = data[rows, :]

data_selected.write_csv("D:/MEGASync/BArbeit/Data/to_analys.csv")