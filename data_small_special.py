
import pandas as pd

data_file = pd.read_csv("D:/MEGASync/BArbeit/Data/rawData/fulldata(so_cl_zo90)_split(2000_1-5).csv")

selected_columns = pd.read_csv("D:/MEGASync/BArbeit/Data/columns_special/columns_special3.csv", header=None, sep=";")
selected_columns_o = selected_columns.values.tolist()
selected_columns = selected_columns_o[0]

# selected_columns = []
# for entry in selected_columns_o:
#     selected_columns.append(entry[1])

info_columns = data_file.iloc[:, 2:6]

data_selected = data_file[selected_columns]


data_selected = pd.concat([info_columns, data_selected], sort=False, axis=1)

data_selected.to_csv("D:/MEGASync/BArbeit/Data/data/special3-1.csv", encoding="UTF-8", sep=",")

print("test")