import os
import re
import csv
import sys
from typing import List

import pandas as pd
import opperations as opp
import gc
import math
import time
import analysis


# todo: zitat: https://stackoverflow.com/questions/354038/how-do-i-check-if-a-string-is-a-number-float

def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def is_str(s):
    try:
        str(s)
        return True
    except ValueError:
        return False


def average(data: list):
    g = 0
    for n, entry in enumerate(data, 1):
        g += float(entry)
    average = g / n
    return average

# todo entscheiden was mit dem Wert der Standardabweichung geschehen soll, eventuell extra methode?
def variance(data: list):
    g = 0
    for n, entry in enumerate(data, 1):
        g += entry
    average = g / n

    var: float
    var = 0
    for n, entry in enumerate(data, 1):
        var += (entry - average) ** 2

    var = var / n
    sd = math.sqrt(var)

    return var, sd


class GetData():

    def __init__(self, data_file):

        self.info = True
        self.row_info = True
        self.col_info = True

        self.data = []
        self.header = []

        self.positions_int = []
        self.positions_float = []
        self.positions_str = []

        self.counter_r_int = []  # Position in der Liste entspricht Nummer der Zeile, Wert der Position entspricht der Anzahl an int/float/string/0/1-Werten
        self.counter_r_float = []
        self.counter_r_string = []
        self.counter_r_zero = []
        self.counter_r_one = []

        self.counter_c_int = []  # Position in der Liste entspricht Nummer der Spalte, Wert der Position entspricht der Anzahl an int/float/string/0/1-Werten
        self.counter_c_float = []
        self.counter_c_string = []
        self.counter_c_zero = []
        self.counter_c_one = []

        # Wie oft kommen Integer/String/Float Werte pro Spalte vor? -->

        self.column_counter = []
        self.column_counter_clean = []
        self.column_counter_unclean = []
        self.column_extraordinary_int = []
        self.column_extraordinary_float = []
        self.column_extraordinary_string = []

        self.index_one = []
        self.index_zero = []

        self.many_ones_90 = []
        self.many_ones_95 = []
        self.many_ones_99 = []
        self.many_ones_100 = []
        self.many_zeros_90 = []
        self.many_zeros_95 = []
        self.many_zeros_99 = []
        self.many_zeros_100 = []

        self.columns_extraordinary = []
        self.extraordinary_coords = []

        self.int_columns_clean = []
        self.string_columns_clean = []
        self.float_columns_clean = []
        self.int_columns_99 = []
        self.string_columns_99= []
        self.float_columns_99 = []
        self.int_columns_95 = []
        self.string_columns_95= []
        self.float_columns_95 = []
        self.int_columns_90 = []
        self.string_columns_90 = []
        self.float_columns_90 = []
        self.int_columns_all = []
        self.float_columns_all = []
        self.string_columns_all = []
        '''
        with open(data_file, "r", encoding="utf8") as read_file:
            # todo: beschreiben das die csv datei in utf8 geschrieben ist (weil vermutlich von linux)
            reader = csv.reader(read_file)

            for csv_entry in reader:

                try:
                    self.data.append(csv_entry)

                except:
                    print("Error: ", sys.exc_info())
        '''
        data = pd.read_csv(data_file)
        self.data = pd.DataFrame(data)

        print(self.data.shape)

        self.header = self.data.keys()
        # print(self.header)
        # print(self.data)


        self.rows = len(self.data.index)
        self.columns = len(self.data.keys())

        print("\n Zeilen:\t", self.rows)
        print("Spalten:\t", self.columns)

        # erzeugt die Zeilenpositionen innerhalb der Listen und füllt sie gleichzeitig mit 0 als Startwert
        for n in range(0, self.rows):
            self.counter_r_int.insert(n, 0)
            self.counter_r_float.insert(n, 0)
            self.counter_r_string.insert(n, 0)
            self.counter_r_zero.insert(n, 0)
            self.counter_r_one.insert(n, 0)

        # erzeugt die Spaltenpositionen innerhalb der Listen und füllt sie gleichzeitig mit 0 als Startwert
        for n in range(0, self.columns):
            self.counter_c_int.insert(n, 0)
            self.counter_c_float.insert(n, 0)
            self.counter_c_string.insert(n, 0)
            self.counter_c_zero.insert(n, 0)
            self.counter_c_one.insert(n, 0)

        # schlüsselt Spalten nach Eintrags-Format (Integer, Float, String) auf
        for columnnr, column_entry in enumerate(self.data.keys(), 0):
                for rownr, row_entry in enumerate(self.data[column_entry], 0):
                    # zuerst auf integer dann auf float testen

                    if isinstance(row_entry, int) is True:
                        # print("Index-Nr:   ", rownr, " - ", columnnr, "int: ", row_entry)
                        self.positions_int.append([rownr, columnnr])
                        self.counter_r_int[rownr] += 1
                        self.counter_c_int[columnnr] += 1
                        try:
                            number = int(row_entry)
                            if number == 0:
                                self.index_zero.append([rownr, columnnr])
                                self.counter_r_zero[rownr] += 1
                                self.counter_c_zero[columnnr] += 1
                            if number == 1:
                                self.index_one.append([rownr, columnnr])
                                self.counter_r_one[rownr] += 1
                                self.counter_c_one[columnnr] += 1
                        except:
                            pass

                    elif analysis.is_float(row_entry) is True:
                        # print("Index-Nr:   ", rownr, " - ", columnnr, "float: ", row_entry)
                        self.positions_float.append([rownr, columnnr])
                        self.counter_r_float[rownr] += 1
                        self.counter_c_float[columnnr] += 1
                        try:
                            number = float(row_entry)
                            if number == 0:
                                self.index_zero.append([rownr, columnnr])
                                self.counter_r_zero[rownr] += 1
                                self.counter_c_zero[columnnr] += 1
                            if number == 1:
                                self.index_one.append([rownr, columnnr])
                                self.counter_r_one[rownr] += 1
                                self.counter_c_one[columnnr] += 1
                        except:
                            pass


                    elif analysis.is_str(row_entry) is True:
                        # print("Index-Nr:   ", rownr, " - ", columnnr, "str: ", row_entry)
                        self.positions_str.append([rownr, columnnr])
                        self.counter_r_string[rownr] += 1
                        self.counter_c_string[columnnr] += 1
                        try:
                            number = int(row_entry)
                            if number == 0:
                                self.index_zero.append([rownr, columnnr])
                                self.counter_r_zero[rownr] += 1
                                self.counter_c_zero[columnnr] += 1
                            if number == 1:
                                self.index_one.append([rownr, columnnr])
                                self.counter_r_one[rownr] += 1
                                self.counter_c_one[columnnr] += 1
                        except:
                            pass

                # print(time.strftime("%H:%M:%S"),
                #       "\t Spalte gelesen \t Interger/Float/String-Werte sowie 0&1 indexiert \t Spalten-Nr.:", columnnr)

        """

        :param data_file: Aus zu wertende Tabelle
        :return: header: Tabellen-Kopf
                 index_int: Liste mit Spaltennummern in denen Integer-Werte stehen
                 index_float: Liste mit Spaltennummern in denen Float-Werte stehen
                 index_str: Liste mit Spaltennummern in denen String-Werte stehen
                 index_zero: Liste mit Spaltennummern in denen 0 steht
                 index_one: Liste mit Spaltennummern in denen 1 steht
        """

    def column_structure(self):

        """

        :param index_int:
        :param index_float:
        :param index_str:
        :param index_one:
        param index_zero:
        :return: counter: Liste mit wievielen Integer, Float bzw. String Variablen pro Reihe vorkommen, ihren Anteilen sowie
                        wieviele 0 bzw. 1 vorkommen (wenn Eintrag -1 -> nur 0 bzw. 1 in der jeweiligen Spalte)
                [[Reihen-Nr., Integer-Elemente, Float-Elemente, String-Elemente, Integer Anteil, Float Anteil, String Anteil]]
                 count_clean: Reihen mit nur Integer/Float/String werten
                 count_unclean: Reihen mit unterschiedlichen Einträgen
        """
        '''
        # Anzahl der Zeilen ergibt sich aus Anzehl der 0. Spalten Einträge, welcher immer vorhanden ist da er automatisch
        # pro Eintrag erzeugt wurde und nicht vom Musikstück ausgelesen werden musste

        rows = sum(x.count(0) for x in self.index_int) + sum(x.count(0) for x in self.index_float) + sum(
            x.count(0) for x in self.index_str)
        '''
        min: int
        sec: int

        if self.col_info is True:
            time_stamp_sum = []
            time_stamp_sum.append([int(time.strftime("%M")), int(time.strftime("%S"))])
            print(time.strftime("%M:%S"))


        '''
        for colnr in range(0, self.columns):
            data = self.data.iloc[, colnr]
        '''

        # Erstelle jetzt schon die Zeilen um später mit den Index Werten navigieren zu können anstatt nach den Namen der Zeilen&Spalten zu suchen
        columns = []
        for x in range(self.columns):
            columns.append(0)

        self.data.loc["Interger Werte"] = columns
        self.data.loc["Interger Anteil"] = columns
        self.data.loc["Float Werte"] = columns
        self.data.loc["Float Anteil"] = columns
        self.data.loc["String Werte"] = columns
        self.data.loc["String Anteil"] = columns
        self.data.loc["Clean"] = columns                # besser keine boolean werte verwenden da diese Zeitintensiver sind ... diese nimmt mit steigender Iteration auch noch irgendwie zu
        self.data.loc["Anzahl 0:"] = columns
        self.data.loc["Anteil 0:"] = columns
        self.data.loc["Anzahl 1:"] = columns
        self.data.loc["Anteil 1:"] = columns
        self.data.loc["Durchschnitt:"] = columns
        self.data.loc["Varianz:"] = columns
        self.data.loc["Standardabweichung:"] = columns

        duration_for = []




        for colnr in range(0, self.columns):

            if self.col_info is True:
                print(time.strftime("%H:%M:%S"), "\t Spalte ausgewertet \t Spalten-Nr.:", colnr)

            # time_stamp_for = []
            # time_stamp_for.append(int(round(time.time() * 1000000)))

            cint = self.counter_c_int[colnr]
            cfloat = self.counter_c_float[colnr]
            cstr = self.counter_c_string[colnr]
            czero = self.counter_c_zero[colnr]
            cone = self.counter_c_one[colnr]

            # Test ob in allen Spalten gleich viele Einträge vorkommen oder ob in einer Spalte Einträge fehlen
            test = cint + cfloat + cstr
            if test != self.rows:
                print("Fehlende Einträge in Spalte-Nr.:", colnr)

            else:
                # Test ob in einer Spalte nur 0 bzw. 1 vorkommen, was auf fehlerhafte Einträge hin deuten würde
                if czero == self.rows:
                    czero = -1
                    # print("Spalte mit nur 0 - Spalten-Nr.:\t", colnr)

                if cone == self.rows:
                    cone = -1
                    # print("Spalte mit nur 1 - Spalten-Nr.:\t", colnr)

                g = cint + cfloat + cstr
                gi = cint / g
                gf = cfloat / g
                gs = cstr / g
                gz = self.counter_c_zero[colnr] / self.rows
                go = self.counter_c_one[colnr] / self.rows

                if go >= 0.90:
                    self.many_ones_90.append(colnr)
                if gz >= 0.90:
                    self.many_zeros_90.append(colnr)

                if go >= 0.95:
                    self.many_ones_95.append(colnr)
                if gz >= 0.95:
                    self.many_zeros_95.append(colnr)

                if go >= 0.99:
                    self.many_ones_99.append(colnr)
                if gz >= 0.99:
                    self.many_zeros_99.append(colnr)

                if go == 1:
                    self.many_ones_100.append(colnr)
                if gz == 1:
                    self.many_zeros_100.append(colnr)

                # time_stamp_for.append(int(round(time.time() * 1000000)))

                self.column_counter.append([colnr, cint, cfloat, cstr, gi, gf, gs, czero, cone])

                # time_stamp_for.append(int(round(time.time() * 1000000)))

                self.data.iloc[self.rows, colnr] = cint
                self.data.iloc[self.rows + 1, colnr] = gi
                self.data.iloc[self.rows + 2, colnr] = cfloat
                self.data.iloc[self.rows + 3, colnr] = gf
                self.data.iloc[self.rows + 4, colnr] = cstr
                self.data.iloc[self.rows + 5, colnr] = gs
                self.data.iloc[self.rows + 6, colnr] = 0
                self.data.iloc[self.rows + 7, colnr] = self.counter_c_zero[colnr]
                self.data.iloc[self.rows + 8, colnr] = gz
                self.data.iloc[self.rows + 9, colnr] = self.counter_c_one[colnr]
                self.data.iloc[self.rows + 10, colnr] = go


                ''' dauert viel länger: 
                self.data[self.header[colnr]]["Integer Anteil"] = gi
                self.data[self.header[colnr]]["Float Werte"] = cfloat
                self.data[self.header[colnr]]["Float Anteil"] = gf
                self.data[self.header[colnr]]["String Werte"] = cstr
                self.data[self.header[colnr]]["String Anteil"] = gs
                self.data[self.header[colnr]]["Clean"] = False
                '''

                # time_stamp_for.append(int(round(time.time() * 1000000)))

                if gi == 1 or gf == 1 or gs == 1:
                    self.column_counter_clean.append(colnr)
                    self.data.iloc[self.rows + 6, colnr] = 1

                if gi == 1:
                    self.int_columns_clean.append(colnr)
                    self.data.iloc[self.rows + 11, colnr] = analysis.average(self.data.iloc[0:self.rows, colnr])
                    self.data.iloc[self.rows + 12, colnr], self.data.iloc[self.rows + 13, colnr] = analysis.variance(self.data.iloc[0:self.rows, colnr])
                elif gs == 1:
                    self.string_columns_clean.append(colnr)
                elif gf == 1:
                    self.float_columns_clean.append(colnr)
                    self.data.iloc[self.rows + 11, colnr] = analysis.average(self.data.iloc[0:self.rows, colnr])
                    self.data.iloc[self.rows + 12, colnr], self.data.iloc[self.rows + 13, colnr] = analysis.variance(self.data.iloc[0:self.rows, colnr])



                if 1 > gi >= 0.99:
                    self.columns_extraordinary.append(colnr)

                    if 0.01 >= gs > 0:
                        for str_coord in self.positions_str:
                            if str_coord[1] == colnr:
                                self.column_extraordinary_string.append(["string", str_coord, cint, cfloat, cstr, gi, gf, gs, czero, cone])
                               # self.data[self.header[colnr]]["Außergewöhnlicher String Eintrag"] = str_coord
                                self.extraordinary_coords.append(str_coord)
                    if 0.01 >= gf > 0:
                        for float_coord in self.positions_float:
                            if float_coord[1] == colnr:
                                self.column_extraordinary_float.append(["float", float_coord, cint, cfloat, cstr, gi, gf, gs, czero, cone])
                               # self.data[self.header[colnr]]["Außergewöhnlicher Float Eintrag"] = float_coord
                                self.extraordinary_coords.append(float_coord)

                elif 1 > gf >= 0.99:
                    self.columns_extraordinary.append(colnr)
                    if 0.01 >= gs > 0:
                        for str_coord in self.positions_str:
                            if str_coord[1] == colnr:
                                self.column_extraordinary_string.append(["string", str_coord, cint, cfloat, cstr, gi, gf, gs, czero, cone])
                               # self.data[self.header[colnr]]["Außergewöhnlicher String Eintrag"] = str_coord
                                self.extraordinary_coords.append(str_coord)
                    if 0.01 >= gi > 0:
                        for int_coord in self.positions_int:
                            if int_coord[1] == colnr:
                                self.column_extraordinary_int.append(["int", int_coord, cint, cfloat, cstr, gi, gf, gs, czero, cone])
                              #  self.data[self.header[colnr]]["Außergewöhnlicher Integer Eintrag"] = int_coord
                                self.extraordinary_coords.append(int_coord)

                elif 1 > gs >= 0.99:
                    self.columns_extraordinary.append(colnr)
                    if 0.01 >= gf > 0:
                        for float_coord in self.positions_float:
                            if float_coord[1] == colnr:
                                self.column_extraordinary_float.append(["float", float_coord, cint, cfloat, cstr, gi, gf, gs, czero, cone])
                              #  self.data[self.header[colnr]]["Außergewöhnlicher Float Eintrag"] = float_coord
                                self.extraordinary_coords.append(float_coord)
                    if 0.01 >= gi > 0:
                        for int_coord in self.positions_int:
                            if int_coord[1] == colnr:
                                self.column_extraordinary_int.append(["int", int_coord, cint, cfloat, cstr, gi, gf, gs, czero, cone])
                              #  self.data[self.header[colnr]]["Außergewöhnlicher Integer Eintrag"] = int_coord
                                self.extraordinary_coords.append(int_coord)

                if gi >= 0.99:
                    self.int_columns_99.append(colnr)
                elif gf >= 0.99:
                    self.float_columns_99.append(colnr)
                elif gs >= 0.99:
                    self.string_columns_99.append(colnr)

                if gi >= 0.95:
                    self.int_columns_95.append(colnr)
                elif gf >= 0.95:
                    self.float_columns_95.append(colnr)
                elif gs >= 0.95:
                    self.string_columns_95.append(colnr)

                if gi >= 0.9:
                    self.int_columns_90.append(colnr)
                elif gf >= 0.9:
                    self.float_columns_90.append(colnr)
                elif gs >= 0.9:
                    self.string_columns_90.append(colnr)

                if gi > 0.50:
                    self.int_columns_all.append(colnr)
                elif gf > 0.50:
                    self.float_columns_all.append(colnr)
                elif gs > 0.50:
                    self.string_columns_all.append(colnr)
                '''
                time_stamp_for.append(int(round(time.time() * 1000000)))

                for n, stamp in enumerate(time_stamp_for, 0):
                    if 0 < n < len(time_stamp_for):
                        duration = (stamp - time_stamp_for[n-1])
                        print(n, ". Zeitfenster", duration)
                '''

        if self.col_info is True:
            time_stamp_sum.append([int(time.strftime("%M")), int(time.strftime("%S"))])
            print(time.strftime("%M:%S"))

            # for n, stamp in enumerate(time_stamp_sum, 1):
            #     if n < len(time_stamp_sum):
            #         duration = (stamp[0] - time_stamp_sum[n-1][0])*60 + (stamp[1] - time_stamp_sum[n-1][1])
            #         print(n, ". Zeitfenster", duration)

    def row_structure(self):
        # todo: rows nach boxplot auswerten

        # Anzahl der Zeilen ergibt sich aus Anzehl der 0. Spalten Einträge, welcher immer vorhanden ist da er automatisch
        # pro Eintrag erzeugt wurde und nicht vom Musikstück ausgelesen werden musste

        self.row_counter = []

        for rownr in range(0, self.rows):

            row_counter_int = self.counter_r_int[rownr]
            row_counter_float = self.counter_r_float[rownr]
            row_counter_string = self.counter_r_string[rownr]
            row_counter_zero = self.counter_r_zero[rownr]
            row_counter_one = self.counter_r_one[rownr]

            # Test ob in allen Zeilen gleich viele Einträge vorkommen oder ob in einer Zeile Einträge fehlen
            test = row_counter_int + row_counter_float + row_counter_string
            if test != self.columns:
                print("Fehlende Einträge in Zeile-Nr.:", rownr)

            else:
                # Test ob in einer Zeile nur 0 bzw. 1 vorkommen, was auf fehlerhafte Einträge hin deuten würde
                if row_counter_zero == self.columns:
                    row_counter_zero = -1
                    print("0:", rownr)

                if row_counter_one == self.columns:
                    row_counter_one = -1
                    print("1:", rownr)

                g = row_counter_int + row_counter_float + row_counter_string
                gi = row_counter_int / g
                gf = row_counter_float / g
                gs = row_counter_string / g
                self.row_counter.append([rownr, row_counter_int, row_counter_float, row_counter_string, gi, gf, gs, row_counter_zero, row_counter_one])

                if self.row_info is True:
                    print(time.strftime("%H:%M:%S"),
                          "\t Zeilen-Daten zusammengefasst, Int/Float/String/0/1-Werte gezählt \t Zeilen-Nr.:", rownr)

        '''
        for rownr, entry in enumerate(self.row_counter, 0):
            if entry[4] == 1 or entry[5] == 1 or entry[6] == 1:

                self.row_counter_clean.append(entry)

            else:

                self.row_counter_unclean.append(entry)
        '''

        self.zeros_per_row = []
        self.ones_per_row = []
        gzero = 0
        gone = 0
        for rownr, row in enumerate(self.row_counter, 1):
            gzero = gzero + row[7]
            gone = gone + row[8]

            self.zeros_per_row.append(row[7])
            self.ones_per_row.append(row[8])

        self.zeros_per_row.sort()
        self.ones_per_row.sort()

        m_zero = Boxplot(self.zeros_per_row)
        m_ones = Boxplot(self.ones_per_row)

        self.r_var_zero, self.r_sd_zero = analysis.variance(self.zeros_per_row)
        self.r_var_one, self.r_sd_one = analysis.variance(self.ones_per_row)

        self.r_average_zero = analysis.average(self.zeros_per_row)
        self.r_average_one = analysis.average(self.ones_per_row)

    def information(data_file: str):
        """
        :param data_file: Position der zu analysierenden CSV-Datei
        :return: index

        Ließt CSV-Tabelle ein und ließt Informationen wie die Zusammensetzung der Daten aus
        """

        '''
            # bei allen restlichen Durchläufen soll geprüft werden,
            # ob beinhaltende Elemente mit denen der Reihe vom Typ her übereinstimmen
            else:

                for n2, entry2 in enumerate(entry1, 0):
                    if is_int(entry2) is True:
                        print("Index-Nr:   ", n1, " - ", n2, "int: ", entry2)
                        if (n2 in index_int) is False:
                            print("Index Integer Error:", n1, " - ", n2)

                    elif is_float(entry2) is True:
                        print("Index-Nr:   ", n1, " - ", n2, "float: ", entry2)
                        if (n2 in index_float) is False:
                            print("Index Float Error:", n1, " - ", n2)

                    elif is_str(entry2) is True:
                        print("Index-Nr:   ", n1, " - ", n2, "str: ", entry2)
                        if (n2 in index_str) is False:
                            print("Index String Error:", n1, " - ", n2)
            '''

        # Längen test: wenn die Summe aller Elemente der Index Listen gleich
        # der größten eingelesenen Index-Zahl ist wurde kein Element aus gelassen

        anzahl_elemente = len(index_float) + len(index_int) + len(index_str)
        anzahl_header = len(header[0])

        if anzahl_elemente == anzahl_header:
            # 0 abziehen zum Vergleich, da 0 als Index Element vorhanden,
            # dann aber schon als ein Element bei der Laenge gezählt wird
            # --> der größte gefundene Indize ist immer um 1 kleiner als die gesamte Laenge

            anzahl_elemente = anzahl_elemente - 1

            # todo: evenuell doppelte überprüfung entfernen,
            # normalerweise sollte die anzahl_elemente == anzahl_header prüfung reichen um zu schauen
            # ob alle elemente eingelesen wurden

            if index_str[-1] < index_int[-1]:

                if index_int[-1] < index_float[-1]:
                    if anzahl_elemente == index_float[-1]:
                        print("\nLängen test OK --> alle Werte indexiert")

                else:
                    if anzahl_elemente == index_int[-1]:
                        print("\nLängen test OK --> alle Werte indexiert")

            else:

                if index_str[-1] < index_float[-1]:
                    if anzahl_elemente == index_float[-1]:
                        print("\nLängen test OK --> alle Werte indexiert")

                else:
                    if anzahl_elemente == index_str[-1]:
                        print("\nLängen test OK --> alle Werte indexiert")

        # zählt wieoft in einer Spalte ein bestimmtes Eintrags Format vorkommt

        pdfile = pd.read_csv(data_file)

        ''''
        data_col = []

        for n, entry in enumerate(header, 0):
            data_col.append(pdfile[[entry]])

        print(data_col[0])
        print(data_col[1])
        '''

        numbers = []
        '''
        for n1, entry1 in enumerate(pdfile, 0):

            n2 = len(pdfile[entry1])

            print(len(pdfile[entry1]))
            print(n1, " --- ", pdfile[entry1])

            for x in range(n2):

                if is_int(pdfile[entry1][x]) is True:
                    print("int:", x, "\t", pdfile[entry1][x])

                    # numbers.insert(pdfile[n1][x], pdfile[entry1][x])

                elif is_float(pdfile[entry1][x]) is True:
                    print("float:", x, "\t", pdfile[entry1][x])

                elif is_str(pdfile[entry1][x]) is True:
                    print("str:", x, "\t", pdfile[entry1][x])
    '''
        # return index

    # def coloum_analyses(data_file):


class Boxplot():

    def __init__(self, data):

        self.list = data
        self.list.sort()
        x = len(data)

        self.min = data[0]
        self.max = data[-1]

        if x > 2:
            if x % 2:
                pm = x // 2
                self.median = data[pm]

                if pm % 2:
                    pq1 = pm // 2
                    self.q1 = data[pq1]

                    pq3 = pm + pq1 + 1  # pm und pq1 sind beide für die Listenposition um 1 zu gering, damit pq3 in der Folge auch nur um 1 zu gering ist --> +1
                    self.q3 = data[pq3]

                else:
                    pq11 = pm / 2 - 1  # eigentlich +1, da mp1/2 Positionen in der Liste eind welche schon mit 0 beginnt beide -1
                    pq12 = pm / 2

                    pq11 = int(pq11)
                    pq12 = int(pq12)
                    self.q1 = (data[pq11] + data[pq12]) / 2

                    pq31 = pm + pq11 + 1
                    pq32 = pm + pq12 + 1

                    self.q3 = (data[pq31] + data[pq32]) / 2

            else:

                pm1 = x / 2 - 1  # eigentlich +1, da mp1/2 Positionen in der Liste eind welche schon mit 0 beginnt beide -1
                pm2 = x / 2

                pm1 = int(pm1)
                pm2 = int(pm2)
                self.median = (data[pm1] + data[pm2]) / 2

                pm1 += 1

                if pm1 % 2:
                    pq1 = pm1 // 2
                    self.q1 = data[pq1]

                    pq3 = pm1 + pq1
                    self.q3 = data[pq3]

                else:
                    pq11 = pm1 / 2 - 1  # eigentlich +1, da mp1/2 Positionen in der Liste eind welche schon mit 0 beginnt beide -1
                    pq12 = pm1 / 2

                    pq11 = int(pq11)
                    pq12 = int(pq12)

                    self.q1 = (data[pq11] + data[pq12]) / 2

                    pq31 = pm1 + pq11
                    pq32 = pm1 + pq12

                    self.q3 = (data[pq31] + data[pq32]) / 2
            '''
            print("\nList: ", self.list)
            print("median: ", self.median)
            print("q1: ", self.q1)
            print("q3: ", self.q3)
            print("min: ", self.min)
            print("max:", self.max)
            '''

        else:
            print("Liste zu kurz um sinnvoll aus zu werten. Minimum 3 Elemente")
