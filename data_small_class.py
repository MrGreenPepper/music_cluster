import os
import numpy as np
import math
import data_cscale_methods
from sklearn import preprocessing
import re
import pandas as pd


class SmallData:

    def __init__(self, data_file, datadir):
        self.norm = True
        self.gross_weight = (True, 5)
        self.interval_scale = (True, 5)
        self.single_scale = (True, 5)
        self.tonal = (True, 2)

        self.positional_columns = 6
        self.string_columns = 8
        self.info_rows = 13

        self.data_file = data_file
        self.filename = self.data_file
        self.filename = re.sub("\.csv", "", self.data_file)
        self.filename = ")" + self.filename
        # datadir = "D:/MEGAsync/BArbeit/Essentia_try/Data/rawData/"
        self.datadir = datadir


    def create(self):
        os.chdir(self.datadir)

        self.origin_fulldata = pd.read_csv(self.data_file)
        self.fulldata_rows = len(self.origin_fulldata.index)

        self.fulldata_columns = len(self.origin_fulldata.keys())
        self.justdata_columns = self.fulldata_columns - self.positional_columns

        # erstellen der verschiedenen Databasen

        # analisieren der Spalten-Zusammenstellung nach einfach vorhanden Spalten und mehreren Spalten welche Zeitintervalle abbilden

        self.origin_justdata_pandas = self.origin_fulldata.iloc[0:(self.fulldata_rows - self.info_rows),
                                      self.positional_columns:(self.fulldata_columns - self.string_columns)]

        self.single_columns, self.normal_intervals, self.timeline_intervals = data_cscale_methods.get_singles_and_timelines(
            self.origin_justdata_pandas)

        self.timeline_columns = []
        self.tonal_columns = []
        self.tonal_intervals = []
        for i_nr, interval in enumerate(self.timeline_intervals, 0):

            if self.tonal[0] == False:
                for x in range(interval[0], (interval[1] + 1)):
                    self.timeline_columns.append(x)
            else:
                l = len(self.timeline_intervals) - 5
                if i_nr < l:
                    for x in range(interval[0], (interval[1] + 1)):
                        self.timeline_columns.append(x)
                else:
                    self.tonal_intervals.append([interval[0], interval[1]])
                    for x in range(interval[0], (interval[1] + 1)):
                        self.tonal_columns.append(x)

        self.normal_columns = []

        for interval in self.normal_intervals:
            for x in range(interval[0], (interval[1] + 1)):
                self.normal_columns.append(x)

        if self.tonal[0] == True:
            self.timeline_intervals.pop(-1)
            self.timeline_intervals.pop(-1)
            self.timeline_intervals.pop(-1)
            self.timeline_intervals.pop(-1)
            self.timeline_intervals.pop(-1)

        self.origin_single_data_pandas = pd.DataFrame(self.origin_justdata_pandas.iloc[:, self.single_columns])
        self.origin_normal_data_pandas = pd.DataFrame(self.origin_justdata_pandas.iloc[:, self.normal_columns])
        self.origin_timeline_data_pandas = pd.DataFrame(self.origin_justdata_pandas.iloc[:, self.timeline_columns])
        self.origin_tonal_data_pandas = pd.DataFrame(self.origin_justdata_pandas.iloc[:, self.tonal_columns])

        # print("\nsingle:")
        # for entry in origin_single_data_pandas.keys():
        #     print(entry)
        #
        # print("\nnormal")
        # for entry in origin_normal_data_pandas.keys():
        #     print(entry)
        #
        # print("\ntimeline")
        # for entry in timeline_intervals:
        #     x = int(entry[0])
        #     print(origin_justdata_pandas.columns[x])
        #     print(entry[1] - entry[0])
        #
        # for x in range(0, fulldata_columns):
        #     if origin_fulldata.columns[x] == 'tonal_chords_histogram-0':
        #         print(x)
        #     if origin_fulldata.columns[x] == 'tonal_thpcp-1':
        #         print(x)

        # Daten Matrizen zum bearbeiten erstellen

        'Daten in numpy umwandeln - Matrizen überführen + strings in int umwandeln'
        self.normal_data_numpy = self.origin_normal_data_pandas.to_numpy()
        self.tonal_data_numpy = self.origin_tonal_data_pandas.to_numpy()
        # String Daten umwandeln
        self.origin_string_data_pandas = self.origin_fulldata.iloc[0:(self.fulldata_rows - self.info_rows),
                                         (self.fulldata_columns - self.string_columns):self.fulldata_columns]
        self.string_data_numpy = data_cscale_methods.string_to_int(self.origin_string_data_pandas)

        self.single_data_numpy = self.origin_single_data_pandas.to_numpy()
        print("\nsingle", np.ma.shape(self.single_data_numpy))
        print("normal", np.ma.shape(self.normal_data_numpy))
        self.timeline_data_numpy = self.origin_timeline_data_pandas.to_numpy()
        print("timeline", np.ma.shape(self.timeline_data_numpy))
        if self.tonal[0] == True:
            print("tonal", np.ma.shape(self.tonal_data_numpy))
        print("string", np.ma.shape(self.string_data_numpy))

        for entry in self.origin_single_data_pandas.keys():
            print("Single: \t", entry)

        for entry in self.origin_normal_data_pandas.keys():
            print("normal: \t", entry)

        for entry in self.origin_timeline_data_pandas.keys():
            print("timeline: \t", entry)

        for entry in self.origin_tonal_data_pandas.keys():
            print("tonal: \t", entry)

        for entry in self.origin_string_data_pandas.keys():
            print("string: \t", entry)
        # todo option erklären hier die langen Variablen-Reihen zu normalisieren und ob das überhaupt einen effekt hat !!! normalisiert alle Werte im mittel Teil!!!
        # data_matrix = scale(data_matrix, 0, 1)
        # matrix_max, matrix_min = data_matrix.max(), data_matrix.min()
        # data_matrix = data_convert.normalize_matrix(data_matrix)

    def save(self):

        single_index_names = list(self.origin_single_data_pandas.index)
        single_column_names = list(self.origin_single_data_pandas.keys())
        final_single_data_pandas = pd.DataFrame(data=self.single_data_numpy, index=single_index_names,
                                                columns=single_column_names)

        normal_index_names = list(self.origin_normal_data_pandas.index)
        normal_column_names = list(self.origin_normal_data_pandas.keys())
        final_normal_data_pandas = pd.DataFrame(data=self.normal_data_numpy, index=normal_index_names,
                                                columns=normal_column_names)

        timeline_index_names = list(self.origin_timeline_data_pandas.index)
        timeline_column_names = list(self.origin_timeline_data_pandas.keys())
        final_timeline_data_pandas = pd.DataFrame(data=self.timeline_data_numpy, index=timeline_index_names,
                                                  columns=timeline_column_names)

        string_index_names = list(self.origin_string_data_pandas.index)
        string_column_names = list(self.origin_string_data_pandas.keys())
        final_string_data_pandas = pd.DataFrame(data=self.string_data_numpy, index=string_index_names,
                                                columns=string_column_names)

        tonal_index_names = list(self.origin_tonal_data_pandas.index)
        tonal_column_names = list(self.origin_tonal_data_pandas.keys())
        final_tonal_data_pandas = pd.DataFrame(data=self.tonal_data_numpy, index=tonal_index_names,
                                               columns=tonal_column_names)

        self.positional_data = self.origin_fulldata.iloc[0:(self.fulldata_rows - self.info_rows),
                               0:self.positional_columns]
        converted_data_pandas = pd.concat(
            [self.positional_data, final_single_data_pandas, final_timeline_data_pandas, final_tonal_data_pandas, final_normal_data_pandas, final_string_data_pandas], sort=False, axis=1)

        print("\nInput Matrix Form:\t", self.origin_fulldata.shape)
        print("Output Matrix Form:\t", converted_data_pandas.shape)

        self.filename = "small(" + self.filename + ".csv"
        converted_data_pandas.to_csv(self.filename)
        print(self.filename)