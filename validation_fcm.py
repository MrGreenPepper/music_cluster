import numpy as np
import pandas as pd
import analysis
import os

summary_main = pd.DataFrame(
    index=["Durchschnittlicher Anteil größtes Cluster",
           "Varianz des Anteils vom jeweils größtem Cluster",
           "SD des Anteils vom jeweils größtem Cluster",
           "Durchschnittliche Clusteranzahl pro Intervall",
           "Varianz der Clusteranzahl pro Intervall",
           "SD der Clusteranzahl pro Intervall",
           "Summe aller Abweichungen zum jeweiligem Intervall",
           "Durchschnittliche Abweichung",
           "Summe aller Varianzen",
           "Silhoutte",
           "Partition Entropie",
           "Partition Koeffizient",
           "Modifizierte Partition Koeffizienz",
           "Ges. Abstand zwischen den Clustern",
           "Ges. Abstand in den Clustern"])

summary_add = pd.DataFrame(
    index=["Größtes Cluster Anteile Boxplot-min",
           "Größtes Cluster Anteile Boxplot-q1",
           "Größtes Cluster Anteile Boxplot-meadian",
           "Größtes Cluster Anteile Boxplot-q3",
           "Größtes Cluster Anteile Boxplot-max",
           "Cluster Anzahl Boxplot-min",
           "Cluster Anzahl Boxplot-q1",
           "Cluster Anzahl Boxplot-median",
           "Cluster Anzahl Boxplot-q3",
           "Cluster Anzahl Boxplot-max"])

summary_full = pd.DataFrame(
    index=["Durchschnittlicher Anteil größtes Cluster",
           "Varianz des Anteils vom jeweils größtem Cluster",
           "SD des Anteils vom jeweils größtem Cluster",
           "Durchschnittliche Clusteranzahl pro Intervall",
           "Varianz der Clusteranzahl pro Intervall",
           "SD der Clusteranzahl pro Intervall",
           "Summe aller Abweichungen zum jeweiligem Intervall",
           "Durchschnittliche Abweichung",
           "Summe aller Varianzen",
           "Silhoutte",
           "Partition Entropie",
           "Partition Koeffizient",
           "Modifizierte Partition Koeffizienz",
           "Ges. Abstand zwischen den Clustern",
           "Ges. Abstand in den Clustern",
           "Größtes Cluster Anteile Boxplot-min",
           "Größtes Cluster Anteile Boxplot-q1",
           "Größtes Cluster Anteile Boxplot-meadian",
           "Größtes Cluster Anteile Boxplot-q3",
           "Größtes Cluster Anteile Boxplot-max",
           "Cluster Anzahl Boxplot-min",
           "Cluster Anzahl Boxplot-q1",
           "Cluster Anzahl Boxplot-median",
           "Cluster Anzahl Boxplot-q3",
           "Cluster Anzahl Boxplot-max"])


# datadir = "/home/nox/MEGAsync/BArbeit/MusicCluster/Data/fcmpp"
datadir = "D:/MEGAsync/BArbeit/MusicCluster/Data/fcm"
os.chdir(datadir)
dataset = "small(single)fulldata(so_cl_zo90)_split(2000_0-5))"

algo = "fcm"
cstart = 5
cend = 15
cstep = 5

c = cstart
clist = []
while c <= cend:
    clist.append(c)
    c += cstep

starts = 50
itermax = 1000
fuzziness = 1.5

for clustercount in clist:

    directory_position = clustercount + 5

    config = algo + "(s" + str(starts) + "imax" + str(itermax) + "k" + str(clustercount) + "m" + str(fuzziness) + ")__"
    data_file = config + "data(" + dataset + "_clust.csv"

    data = pd.read_csv(data_file)

    cluster = pd.DataFrame(data)

    # print(cluster.keys())

    old = cluster.iloc[0, directory_position]
    new: str

    # print(old)
    clusterlist_small = []
    clusterlist_big = []

    for n, entry in enumerate(cluster.iloc[:, directory_position], 0):
        if entry == old:
            clusterlist_small.append(cluster.iloc[n, 1])

            # for c in range(2, (clustercount+2)):


        else:
            old = cluster.iloc[n, directory_position]
            clusterlist_big.append(clusterlist_small)
            clusterlist_small = []
            clusterlist_small.append(cluster.iloc[n, 1])
    # beim Ende des letzten Eintrags ist der Name immer noch = old deswegen wird die Anhäng Bedingung nicht
    # ausgeführt was an die stelle manuell nach gehohlt werden muss

    clusterlist_big.append(clusterlist_small)
    print(clusterlist_big)
    # print(len(clusterlist_big))

    for n, entry in enumerate(clusterlist_big, 1):
        if len(entry) == 0:
            print(n)

    # cluster_quality [größe des betrachteten Bereichs, [größtes Cluster, anzahl des größten Clusters], Anteil des
    # größten Clusters an gesamter Menge, unterschiedliche Cluster Anzahl]
    cluster_quality = []

    # geht Intervall Einträge in der gesamten Liste (clusterlist_big) durch
    for entry in clusterlist_big:
        # print(entry)
        # schaut bis zu welcher Clusternummer er überhaupt im folgendem prüfen muss
        highest_cluster = max(entry) + 1
        most_cluster = [0, 0]  # zählt die Anzahl wie oft das cluster mit der höcsten anzahl innerhalb des Intervalls Auftritt
        # - 1. Zahl: Clusternummer
        # - 2.Zahl: Anzahl dieser Clusterzuordnung

        howmany_dif_cl = 0  # zählt wieviele verschiedene Cluster es innerhalb des aktuellen Intervalls gibt

        for n in range(1, highest_cluster):
            counter = entry.count(n)

            if counter > 0:
                howmany_dif_cl += 1

            if counter > most_cluster[1]:
                most_cluster[0] = n
                most_cluster[1] = counter

        cluster_proportions = most_cluster[1] / len(entry)  # Anteil der größten Clusterzuordnung am gesamten Interval

        cluster_quality.append([len(entry), most_cluster, cluster_proportions, howmany_dif_cl])

    # for entry in cluster_quality:
    #     print(entry)

    cluster_proportions = []
    cluster_counter = []

    for entry in cluster_quality:
        cluster_proportions.append(entry[2])
        cluster_counter.append(entry[3])

    proportions_average = analysis.average(cluster_proportions)
    proportions_var, proportions_sd = analysis.variance(cluster_proportions)
    proportions_box = analysis.Boxplot(cluster_proportions)

    counter_average = analysis.average(cluster_counter)
    counter_var, counter_sd = analysis.variance(cluster_counter)
    counter_box = analysis.Boxplot(cluster_counter)


    # print("-----------------------------")
    # print(proportions_average)
    # print(proportions_var)
    # print("-----------------------------")
    # print(proportions_box.min)
    # print(proportions_box.q1)
    # print(proportions_box.median)
    # print(proportions_box.q3)
    # print(proportions_box.max)
    #
    # print("\n-----------------------------")
    # print(counter_average)
    # print(counter_var)
    # print("-----------------------------")
    # print(counter_box.min)
    # print(counter_box.q1)
    # print(counter_box.median)
    # print(counter_box.q3)
    # print(counter_box.max)'

    #ltest = 0
    #for cl_test in clusterlist_big:
    #    print(cl_test)
    #    ltest += len(cl_test)
    #    print(ltest)

    intervall_start = 0
    prob_sd = []
    prob_var = []

    for n, cl_big in enumerate(clusterlist_big, 0):
        clusternumber_min = 2
        clusternumber_max = clustercount

        intervall_end = intervall_start + len(cl_big)

        # ließt innerhalb eines Intervalls die prob-Clusterzuordnungen aus
        for cl_num in range(clusternumber_min, (clusternumber_min + clusternumber_max)):
            cl_probabilities = cluster.iloc[intervall_start:intervall_end, cl_num]
            # print(prob1)

            prob_var_list = cl_probabilities.values.tolist()
           # prob_var_list2 = []

            # wandelt Liste nur um von [[[]],[[]]] in [[],[]]
           # for sd_entry in prob_var_list1:
             #   prob_var_list2.append(sd_entry)



            var, sd = analysis.variance(prob_var_list)
            prob_sd_entry = []
            prob_sd_entry.append(len(cl_big))
            prob_sd_entry.append(sd)

            prob_sd.append(prob_sd_entry)

            prob_var_entry = []
            prob_var_entry.append(len(cl_big))
            prob_var_entry.append(var)

            prob_var.append(prob_var_entry)


        #if intervall_end > 1998:
        #    print("end")
        intervall_start += len(cl_big)

    intervall_start = 0



    sum_sd = 0                              # für jedes Objekt einmal seine Standardabweichung gezählt
    n = 0
    for entry in prob_sd:
        sum_sd += entry[0] * entry [1]
        n += entry[0]
    mean_sum_sd = sum_sd / n
    print("Summe aller Standardabweichungen multipliziert mit der jeweiligen Intervallgröße", sum_sd)
    #print(n)

    n = 0
    sum_var = 0                             # für jedes Objekt einmal seine Varianz gezählt
    for entry in prob_var:
        sum_var += entry[0] * entry [1]
        n += entry[0]
    print("Summe aller Varianzen multipliziert mit der jeweiligen Intervallgröße", sum_var)
    #print(n)


       # intervall_start += len(cl_big)

    print(data_file)


    # lade restliche, schon vorhandene ValidierungsDaten
    config = algo + "(s" + str(starts) + "imax" + str(itermax) + "k" + str(clustercount) + "m" + str(fuzziness) + ")__"
    data_val_file = config + "data(" + dataset + "_val.csv"
    data_val = pd.read_csv(data_val_file)

    silh = data_val.iloc[0, 2]
    partition_entropy = data_val.iloc[0, 3]
    partition_coefficient = data_val.iloc[0, 4]
    partition_mod_coef = data_val.iloc[0, 5]
    ss_between = data_val.iloc[0, 6]
    ss_in = data_val.iloc[0, 7]


    summary_main[clustercount] = [proportions_average,
                                  proportions_var,
                                  proportions_sd,
                                  counter_average,
                                  counter_var,
                                  counter_sd,
                                  sum_sd,
                                  mean_sum_sd,
                                  sum_var,
                                  silh,
                                  partition_entropy,
                                  partition_coefficient,
                                  partition_mod_coef,
                                  ss_between,
                                  ss_in]

    summary_add[clustercount] = [proportions_box.min,
                                proportions_box.q1,
                                proportions_box.median,
                                proportions_box.q3,
                                proportions_box.max,
                                counter_box.min,
                                counter_box.q1,
                                counter_box.median,
                                counter_box.q3,
                                counter_box.max]

    summary_full[clustercount] = [proportions_average,
                                  proportions_var,
                                  proportions_sd,
                                  counter_average,
                                  counter_var,
                                  counter_sd,
                                  sum_sd,
                                  mean_sum_sd,
                                  sum_var,
                                  silh,
                                  partition_entropy,
                                  partition_coefficient,
                                  partition_mod_coef,
                                  ss_between,
                                  ss_in,
                                  proportions_box.min,
                                  proportions_box.q1,
                                  proportions_box.median,
                                  proportions_box.q3,
                                  proportions_box.max,
                                  counter_box.min,
                                  counter_box.q1,
                                  counter_box.median,
                                  counter_box.q3,
                                  counter_box.max]

print(summary_main)
config = "fcm(s" + str(starts) + "imax" + str(itermax) + "k" + str(clustercount) + "m" + str(fuzziness) + ")__"
data_file = config + "data(" + dataset

summaryname_main = "summary_" + str(cstart) + "_" + str(cend) + data_file + ".csv"
summary_main.to_csv(summaryname_main)

summaryname_add = "summary_add_" + str(cstart) + "_" + str(cend) + data_file + ".csv"
summary_add.to_csv(summaryname_add)

summaryname_full = "summary_full_" + str(cstart) + "_" + str(cend) + data_file + ".csv"
summary_full.to_csv(summaryname_full)

