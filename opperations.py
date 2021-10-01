import os
import csv
import glob
import re

def exclude(columns, exclude):

    for entry in exclude:
        try:
            columns.pop(columns.index(entry))
        except:
            pass

    return columns

def not_included(columns, length):

    print(columns)
    missing = []
    tomuch = []
    for x in range(0, length):
        if int(columns.count(x)) == 1:
            pass
        elif int(columns.count(x)) == 0:
            missing.append(x)
        elif int(columns.count(x)) > 1:
            tomuch.append([x, columns.count(x)])

    return missing, tomuch

def getfiles(file):

    basedir = os.getcwd()
    basedirlist = os.listdir()

    dirlist = []

    for dir in basedirlist:


        newdir = basedir + "/" + dir

        if os.path.isdir(newdir) == True:

            os.chdir(newdir)

            for filename in glob.glob('*.mp3'):

                dirlist.append(filename, dir)


    return dirlist



def create_sorted_columns(int_columns, float_columns, string_columns):
    columns = [0, 1, 2, 3]

    try:
        int_columns.pop(int_columns.index(0))
    except:
        pass
    try:
        float_columns.pop(float_columns.index(0))
    except:
        pass
    try:
        string_columns.pop(string_columns.index(0))
    except:
        pass
    try:
        int_columns.pop(int_columns.index(1))
    except:
        pass
    try:
        float_columns.pop(float_columns.index(1))
    except:
        pass
    try:
        string_columns.pop(string_columns.index(1))
    except:
        pass
    try:
        int_columns.pop(int_columns.index(2))
    except:
        pass
    try:
        float_columns.pop(float_columns.index(2))
    except:
        pass
    try:
        string_columns.pop(string_columns.index(2))
    except:
        pass
    try:
        int_columns.pop(int_columns.index(3))
    except:
        pass
    try:
        float_columns.pop(float_columns.index(3))
    except:
        pass
    try:
        string_columns.pop(string_columns.index(3))
    except:
        pass

    for entry in int_columns:
        columns.append(entry)
    for entry in float_columns:
        columns.append(entry)
    for entry in string_columns:
        columns.append(entry)

    return columns

def todo(data_file, datadir, musicdir):


    '''
    :param data_file: csv-Dateiname
    :param datadir: Ort der csv-Datei
    :param musicdir: Ort der Musikdateien
    :return: todolist: Liste [index, directory1, directory2, titlename]

    Wertet bisherigen Datenbestand aus und erstellt eine Liste von noch nicht bearbeiteten Titeln

    Ablauf:
         1. ließt bisherigen Datenbestand in ``donelist`` aus
         2. nimmt Fehler-Verzeichnis ebenfalls in ``donelist`` auf
         3. erstellt gesamtes zu bearbeitendes Verzeichnis in ``fulllist``
         4. löscht alle Einträge in  ``fulllist`` die in ``donelist`` schon vorhanden sind


    '''




    donelist = []
    fulllist = []




    os.chdir(datadir)


    # Ließt aus der csv-Dat*ei aus, welche Dateien schon erledigt sind
    with open(data_file, "r") as read_file:
        reader = csv.reader(read_file)

        for entry in reader:

            donelist.append([entry[0], entry[1], entry[2], entry[3]])


    #hängt alle Dateien die nicht funktioniert haben der Liste an
    data_file_error = re.sub("\.csv", "", data_file)
    data_file_error = data_file_error + "error.csv"

    with open(data_file_error, "r") as read_file:
        reader = csv.reader(read_file)

        for entry in reader:

            donelist.append([entry[0], entry[1], entry[2], entry[3]])


    os.chdir(musicdir)
    basedirlist1 = os.listdir()




    # Erstellt Dateien-Verzeichnis
    for dir1 in basedirlist1:

        newdir = musicdir + "/" + dir1

        if os.path.isdir(newdir) == True:

            os.chdir(newdir)
            basedirlist2 = os.listdir()

            for filename in glob.glob('*.mp3'):
                fulllist.append([dir1, 0, filename])


            for dir2 in basedirlist2:

                newdir2 = newdir + "/" + dir2

                if os.path.isdir(newdir2) == True:

                    os.chdir(newdir2)
                    for filename in glob.glob('*.mp3'):
                        fulllist.append([dir1, dir2, filename])


    #donelist.sort(key=lambda x: x[1])
    #fulllist.sort(key=lambda x: x[1])





    #löscht .mp3 Anhang des Dateien-Verzeichnisses, da dieser nicht in der csv-Datei enthalten ist
    for n, item1 in enumerate(fulllist, 0):

        fulllist[n][2] = re.sub("\.", "-", item1[2])
        fulllist[n][2] = re.sub("-mp3", "", item1[2])

    for n, item1 in enumerate(donelist, 0):

        donelist[n][3] = re.sub("\.", "-", item1[3])
        donelist[n][3] = re.sub("-mp3", "", item1[3])






    todolist = fulllist

    print("Fulllist: ")
    print(fulllist)
    print("Donelost: ")
    print(donelist)

    #Vergleicht gesamtes Dateien-Verzeichnis mit der csv-Daten Datei
    #in Fulllist gibt es noch keinen Index-Wert weswegen die zu vergleichende Position um 1 geringer ist
    for item2 in donelist:
        for item1 in fulllist:

            if item1[0] == item2[1]:

                if item1[2] == item2[3]:
                    todolist.remove(item1)


    #hängt .mp3 Endung wieder heran, da aus dieser Liste die Dateipfade für die noch zu analieserenden Stücke ausgelesen werden
    for n, item in enumerate(todolist):
        todolist[n][2] = item[2] + '.mp3'




    index = len(donelist)

    for n, entry in enumerate(todolist, index):

        entry.insert(0, n)

    return todolist





def todonew(musicdir):

    '''

    :param musicdir: Ort der Musikdateien
    :return: todolist: Liste [index, directory1, directory2, titlename]

    Kommt zum Einsatz falls kein vorhandener Datenbestand erkannt wurde. Ließt ausgehend vom ``musicdir``-Verzeichnis
    die Ordnerstruktur bis zum einschließlich 1. Unterordner aus und nimmt alle mp3-Dateien auf.

    '''

    os.chdir(musicdir)
    basedirlist1 = os.listdir()


    todolist = []



    # Erstellt Dateien-Verzeichnis
    for dir1 in basedirlist1:

        newdir = musicdir + "/" + dir1

        if os.path.isdir(newdir) == True:

            os.chdir(newdir)
            basedirlist2 = os.listdir()

            for filename in glob.glob('*.mp3'):
                todolist.append([dir1, 0, filename])


            for dir2 in basedirlist2:

                newdir2 = newdir + "/" + dir2

                if os.path.isdir(newdir2) == True:

                    os.chdir(newdir2)
                    for filename in glob.glob('*.mp3'):
                        todolist.append([dir1, dir2, filename])



    #todolist.sort(key=lambda x: x[1])

    for n, entry in enumerate(todolist, 0):
        entry.insert(0, n)




    return todolist








#sortiert gegebenes csv file und gibt ihn mit dem Namen "..._sorted.csv" aus
def sort(data_file):

    list = []

    with open(data_file, "r") as read_file:
        reader = csv.reader(read_file)

        for entry in reader:
            list.append(entry)

    header = list[0]
    list.remove(list[0])
    list.sort()

    for n, item in enumerate(list, 0):
        if item[0] == "name":
            print(n, item)

    sort = re.sub("\.csv", "-", data_file)
    sort = sort + "_sorted.csv"

    print(sort)

    with open(sort, "w") as write_file:
        writer = csv.writer(write_file, delimiter=',')
        writer.writerow(header)


    with open(sort, "a") as write_file:
        writer = csv.writer(write_file, delimiter=',')
        for item in list:
            writer.writerow(item)

def save_csv(filename, data):

    with open(filename, "w") as write_file:
        writer = csv.writer(write_file, delimiter=',')
        for entry in data:
            writer.writerow(entry)

def load_csv(filename):
    data = []
    with open(filename, "r") as read_file:
        reader = csv.reader(read_file)
        for entry in reader:
            data.append(entry)

    return data