import numpy as np
import pandas as pd
import os
import analysis
import re

# gleicht Varianzen zwischen den Intervallen an und skaliert sie anhand ihrer Größe
def interval_scale(matrix, intervals, wfactor, lfactor):
    int_col = []
    start = 0

    for entry in intervals:
        lenght = entry[1] - entry[0] + 1    # + 1 da der erste Eintrag dazu gehören soll
        end = start + lenght
        int_col.append([start, end])
        start = end

    data_columns = np.ma.size(matrix, axis=1)

    for entry in int_col:
        if lfactor == 0:
            length = (entry[1] - entry[0])
        else:
            length = (entry[1] - entry[0]) / (1 + (lfactor * (entry[1] - entry[0]) - (1 * lfactor)))
        i_std = np.std(matrix[:, entry[0]:entry[1]], axis=0)
        i_std_mean = np.mean(i_std)

        # print("\nIntervall-Größe", np.ma.shape(matrix[:, entry[0]:entry[1]]))
        # print("Intervall std-mean:", i_std_mean)

        matrix[:, entry[0]:entry[1]] = (matrix[:, entry[0]:entry[1]])/((i_std_mean*length) / wfactor)

        i_std = np.std(matrix[:, entry[0]:entry[1]], axis=0)
        i_std_mean = np.mean(i_std)
        # print(i_std)
        # print("Intervall std-mean:", i_std_mean)
        # print("Intervall Einfluss:", i_std_mean*length)

    # print(np.std(matrix))

    return matrix

def single_scale(matrix, factor):

    s_cols = np.ma.size(matrix, axis=1)

    for x in range(0, s_cols):
        c_std = np.ma.std(matrix[:, x])
        matrix[:, x] = (matrix[:, x] / c_std) * factor

    return matrix

def gross_scale(matrix, factor, single):
    if single is False:
        matrix = matrix / np.ma.std(matrix) * factor
    if single is True:
        rows = np.ma.size(matrix, axis=1)
        for x in range(0,rows):
            s_std = np.std(matrix[:, x]) / factor
            matrix[:, x] = matrix[:, x] / s_std




    return matrix

def tonal_scale(matrix, intervals, wfactor, lfactor):
    int_col = []
    start = 0

    for entry in intervals:
        lenght = entry[1] - entry[0] + 1  # + 1 da der erste Eintrag dazu gehören soll
        end = start + lenght
        int_col.append([start, end])
        start = end

    data_columns = np.ma.size(matrix, axis=1)

    for entry in int_col:
        if lfactor == 0:
            length = (entry[1] - entry[0])
        else:
            length = (entry[1] - entry[0]) / (1 + (lfactor * (entry[1] - entry[0]) - (1 * lfactor)))
        i_std = np.std(matrix[:, entry[0]:entry[1]], axis=0)
        i_std_mean = np.mean(i_std)

        # print("\nIntervall-Größe", np.ma.shape(matrix[:, entry[0]:entry[1]]))
        # print("Intervall std-mean:", i_std_mean)

        matrix[:, entry[0]:entry[1]] = (matrix[:, entry[0]:entry[1]]) / ((i_std_mean * length) / wfactor)

        i_std = np.std(matrix[:, entry[0]:entry[1]], axis=0)
        i_std_mean = np.mean(i_std)
        # print(i_std)
        # print("Intervall std-mean:", i_std_mean)
        # print("Intervall Einfluss:", i_std_mean*length)

    # print(np.std(matrix))

    return matrix

def get_singles_and_timelines(data):

    single_columns = []
    timeline_intervals = []
    normal_intervals = []
    cols = len(data.keys())
    y = 0
    in_timeline = 0
    in_normal = 0
    old = 0
    old_name: str


    for columnr, entry in enumerate(data.keys(), 0):                # sortiert längere Werte-Abschnitte heraus (bezieht sich auf Werte die an veschiedenen Zeiten gemessen wurden)
        # if entry == 'tonal_chords_histogram-0':
        #     print("just wait")
        # if entry == 'tonal_thpcp-1':
        #     print("just wait")

        # Auslesen von Zeitreihen:
        if entry[-1].isdigit() is True:

            if in_normal == 1:
                normal_intervals.append([y, columnr - 1])
                in_normal = 0

            if entry[-2].isdigit() is True:
                old = int(entry[-1]) + (10*int(entry[-2]))

            else:
                if in_timeline == 1:
                    new = int(entry[-1])
                    if new <= old:
                        timeline_intervals.append([y, columnr - 1])
                        y = columnr
                        old = new
                else:
                    new = int(entry[-1])
                    y = columnr
                    old = new
                    in_timeline = 1


         # else:
        #     if entry.endswith('0') is True:
        #         if entry[-2].isdigit() is False:
        #             if in_timeline == 0:
        #                 in_timeline = 1
        #                 y = columnr
        #             else:
        #                 timeline_intervals.append([y, columnr - 1])
        #                 y = columnr
        #                 in_timeline = 1

        elif in_timeline == 1:
            timeline_intervals.append([y, columnr - 1])
            in_timeline = 0


        # Auslesen von einzelnen Einträgen:
        if entry[-1].isdigit() is False:
            if entry.endswith('max') is True:
                new_name = re.sub("max", "", entry)
                if in_normal == 1:
                    if new_name == old_name:
                        pass
                    else:
                        normal_intervals.append([y, columnr - 1])
                        old_name = new_name
                        y = columnr
                else:
                    y = columnr
                    in_normal = 1
                    old_name = new_name

            elif entry.endswith('mean') is True:
                new_name = re.sub("mean", "", entry)
                if in_normal == 1:
                    if new_name == old_name:
                        pass
                    else:
                        normal_intervals.append([y, columnr - 1])
                        old_name = new_name
                        y = columnr
                else:
                    y = columnr
                    in_normal = 1
                    old_name = new_name

            elif entry.endswith('median') is True:
                new_name = re.sub("median", "", entry)
                if in_normal == 1:
                    if new_name == old_name:
                        pass
                    else:
                        normal_intervals.append([y, columnr - 1])
                        old_name = new_name
                        y = columnr
                else:
                    y = columnr
                    in_normal = 1
                    old_name = new_name

            elif entry.endswith('min') is True:
                new_name = re.sub("min", "", entry)
                if in_normal == 1:
                    if new_name == old_name:
                        pass
                    else:
                        normal_intervals.append([y, columnr - 1])
                        old_name = new_name
                        y = columnr
                else:
                    y = columnr
                    in_normal = 1
                    old_name = new_name

            elif entry.endswith('var') is True:
                new_name = re.sub("var", "", entry)
                if in_normal == 1:
                    if new_name == old_name:
                        pass
                    else:
                        normal_intervals.append([y, columnr - 1])
                        old_name = new_name
                        y = columnr
                else:
                    y = columnr
                    in_normal = 1
                    old_name = new_name

            else:
                single_columns.append(columnr)
                if in_normal == 1:
                    normal_intervals.append([y, columnr - 1])
                    in_normal = 0

    if in_timeline == 1:
        timeline_intervals.append([y, columnr])


    return single_columns, normal_intervals, timeline_intervals

def string_to_int(data):

    rows = len(data.index)
    columns = len(data.keys())
    np_matrix = np.zeros([rows, columns])

    #np_matrix = data

    # print(np_matrix.shape)
    # all = []

    for colnr, column in enumerate(data, 0):
        for rownr, row in enumerate(data[column], 0):
            # if all.count(row) == 0:
            #     all.append(row)
            if row == "minor":
                np_matrix[rownr, colnr] = 1
            if row == "major":
                np_matrix[rownr, colnr] = 2

            if row == "C":
                np_matrix[rownr, colnr] = 1
            if row == "C#":
                np_matrix[rownr, colnr] = 2
            if row == "D":
                np_matrix[rownr, colnr] = 3
            if row == "Eb":
                np_matrix[rownr, colnr] = 4
            if row == "E":
                np_matrix[rownr, colnr] = 5
            if row == "F":
                np_matrix[rownr, colnr] = 6
            if row == "F#":
                np_matrix[rownr, colnr] = 7
            if row == "G":
                np_matrix[rownr, colnr] = 8
            if row == "Ab":
                np_matrix[rownr, colnr] = 9
            if row == "A":
                np_matrix[rownr, colnr] = 10
            if row == "Bb":
                np_matrix[rownr, colnr] = 11
            if row == "B":
                np_matrix[rownr, colnr] = 12

    return np_matrix

def normalize_matrix(matrix):

    mean_array = np.mean(matrix, axis=0)
    std_array = np.std(matrix, axis=0)

    columns = len(mean_array)

    for x in range(0, columns):
        matrix[:, x] = matrix[:, x] - mean_array[x]
        if std_array[x] != 0:
            matrix[:, x] = matrix[:, x] / std_array[x]
        # if std_array[x] == 0:
        #     print(matrix[:, x])
        #     print(np.mean(matrix[:, x]))
        #     print(x)
        # matrix[:, x] = matrix[:, x] / std_array[x]
    return matrix

def singles_scale():
    pass

class TimeLineInfo:
    def __init__(self, data, timeline_columns):

        self.data = data
        self.timeline_columns = timeline_columns

        self.timeline_data_mean_mean = []
        self.timeline_data_mean_var = []
        self.timeline_data_var_mean = []
        self.timeline_data_var_var = []

        self.timeline_entries_counter = 0

        self.var_array = np.var(self.data, axis=0)
        self.mean_array = np.mean(self.data, axis=0)

        self.var_var = np.var(self.var_array)
        self.var_mean = np.mean(self.var_array)
        self.mean_var = np.var(self.mean_array)
        self.mean_mean = np.var(self.mean_array)

        for entry in timeline_columns:  # Bildet Durchschnitt sowie Varianz der Abschnitte (einzelne Elemente sowie pro Abschnitt)

            self.timeline_entries_counter += entry[1] - entry[0] + 1

            timeline_data_colmean_all = []
            timeline_data_colvar_all = []

            for x in range(entry[0], (entry[1] + 1)):

                timeline_data_colmean_all.append(self.mean_array.item(x))
                timeline_data_colvar_all.append(self.var_array.item(x))

            timeline_data_mean_mean = analysis.average(timeline_data_colmean_all)
            timeline_data_mean_var, timeline_data_origin_numpy_mean_sd = analysis.variance(timeline_data_colmean_all)

            timeline_data_var_mean = analysis.average(timeline_data_colvar_all)
            timeline_data_var_var, timeline_data_var_sd = analysis.variance(timeline_data_colvar_all)

            self.timeline_data_mean_mean.append(timeline_data_mean_mean)
            self.timeline_data_mean_var.append(timeline_data_mean_var)
            self.timeline_data_var_mean.append(timeline_data_var_mean)
            self.timeline_data_var_var.append(timeline_data_var_var)

class DataInfo:
    def __init__(self, data):
        self.data = data

        self.mean_array = np.mean(self.data, axis=0)
        self.var_array = np.var(self.data, axis=0)
        self.std_array = np.std(self.data, axis=0)

        self.var_var = np.var(self.var_array)
        self.var_mean = np.mean(self.var_array)
        self.mean_var = np.var(self.mean_array)
        self.mean_mean = np.var(self.mean_array)
        self.std_mean = np.mean(self.std_array)
        self.std_std = np.std(self.std_array)

        self.data_columns = np.ma.size(self.data, axis=1)
        # print(np.ma.shape(self.data))
        self.mean_list = []
        self.var_list = []
        self.std_list = []


        for x in range(0, self.data_columns):  # Bildet Durchschnitt sowie Varianz der Abschnitte (einzelne Elemente sowie pro Abschnitt)
            self.mean_list.append(self.mean_array.item(x))
            self.var_list.append(self.var_array.item(x))
            self.std_list.append(self.std_array.item(x))

        self.boxplot_mean = analysis.Boxplot(self.mean_list)
        self.boxplot_var = analysis.Boxplot(self.var_list)
        self.boxplot_std = analysis.Boxplot(self.std_list)

'''data_file = "fulldata_11_4-1_test_sorted_clean_zeroone_90.csv"
# datadir = "/home/nox/MEGAsync/BArbeit/Essentia_try/Data/"
datadir = "D:/MEGAsync/BArbeit/Essentia_try/Data/"

os.chdir(datadir)


data = pd.read_csv(data_file)
rows = len(data.index) - 1
data_end = data.iloc[0:rows-13, 2835:2843]
print(data_end)
convert_to_int(data_end, 8, 1033)
'''


