import numpy as np
import pandas as pd
import analysis
import os
import re



# datadir = "/home/nox/MEGAsync/BArbeit/MusicCluster/Data/fcmpp"
datadir = "D:/MEGAsync/BArbeit/Data/cluster_results/fcmpp/"
dataset_origin = "fulldata(so_cl_zo90)"
# subset [ist Subset?, Algorithmus, subset-Art, [Split-Größe, Split-Nr.], [starts, itermax., fuzzyness], [k-Start, k-End, K-Stepsize]]
subset = pd.read_csv("D:/MEGAsync/BArbeit/Data/cluster_results/done_fcmpp.csv", header=None, sep=",")
subset = subset.as_matrix()


#save_subset = pd.concat([subset[:,]])
# index_todo_list = pd.DataFrame(subset)
# index_todo_list.to_csv("D:/MEGAsync/BArbeit/MusicCluster/Data/cluster_results/index_todo.csv")

sumsumindicator = "30_11new_gesamt"



sumsum_main = pd.DataFrame(
    index=["Datensatz",
           "Subset",
           "Algo",
           "Split",
           "Starts",
           "IterMax",
           "Fuzziness",
            "Cluster-Anzahl",
            "Expert-Score gewichtet",
            "Expert-Score Gruppengröße",
           "Expert-Score ungewichtet",
           "Expoert-Score Trennung",
           "Export-Score Trennung Sum",
           "Durchschnittlicher Anteil größtes Cluster",
           "Varianz des Anteils vom jeweils größtem Cluster",
           "SD des Anteils vom jeweils größtem Cluster",
           "Durchschnittliche Clusteranzahl pro Intervall",
           "Varianz der Clusteranzahl pro Intervall",
           "SD der Clusteranzahl pro Intervall",
           "Summe aller Abweichungen innerhalb des jeweiligem Intervall",
           "Durchschnittliche Abweichung",
           "Summe aller Varianzen innerhalb des jeweiligem Intervall",

           "Silhoutte",
           "Partition Entropie",
           "Partition Koeffizient",
           "Modifizierte Partition Koeffizienz",
           "Jaccard Index",
           "Fuzzy Rand Index",
           "Xie Beni",
           "Ges. Abstand zwischen den Clustern",
           "Ges. Abstand in den Clustern",

           "Cluster-Größen gesamt",
           "Cluster-Größen durch.",
           "Cluster-Größen SD",
           "Cluster-Größen min",
           "Cluster-Größen max"])

sumsum_add = pd.DataFrame(
    index=["Datensatz",
           "Subset",
           "Algo",
           "Split",
           "Starts",
           "IterMax",
           "Fuzziness",
            "Cluster-Anzahl",
        "Größtes Cluster Anteile Boxplot-min",
           "Größtes Cluster Anteile Boxplot-q1",
           "Größtes Cluster Anteile Boxplot-meadian",
           "Größtes Cluster Anteile Boxplot-q3",
           "Größtes Cluster Anteile Boxplot-max",
           "Cluster Anzahl Boxplot-min",
           "Cluster Anzahl Boxplot-q1",
           "Cluster Anzahl Boxplot-median",
           "Cluster Anzahl Boxplot-q3",
           "Cluster Anzahl Boxplot-max",
           "Cluster-Größen gesamt:",
           "Cluster-Größen durch.:",
           "Cluster-Größen SD",
           "Cluster-Größen var",
           "Cluster-Größen min",
           "Cluster-Größen q1",
           "Cluster-Größen median",
           "Cluster-Größen q3",
           "Cluster-Größen max"])

sumsum_full = pd.DataFrame(
    index=["Datensatz",
           "Subset",
           "Algo",
           "Split",
           "Starts",
           "IterMax",
           "Fuzziness",
            "Cluster-Anzahl",
            "Expert-Score gewichtet",
            "Expert-Score Gruppengröße",
           "Expert-Score ungewichtet",
           "Expoert-Score Trennung",
           "Export-Score Trennung Sum",
           "Durchschnittlicher Anteil größtes Cluster",
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
           "Jaccard Index",
           "Fuzzy Rand Index",
           "Xie Beni",
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
           "Cluster Anzahl Boxplot-max",
           "Cluster-Größen gesamt",
           "Cluster-Größen durch.",
           "Cluster-Größen SD",
           "Cluster-Größen var",
           "Cluster-Größen min",
           "Cluster-Größen q1",
           "Cluster-Größen median",
           "Cluster-Größen q3",
           "Cluster-Größen max"])

failed = []

os.chdir(datadir)
nsum = 0
for done_nr, subset_entry in enumerate(subset, 1):
    print("donr-nr", done_nr)

    summary_main = pd.DataFrame(
        index=["Datensatz",
           "Subset",
           "Algo",
           "Split",
           "Starts",
           "IterMax",
           "Fuzziness",
            "Cluster-Anzahl",
            "Expert-Score gewichtet",
            "Expert-Score Gruppengröße",
           "Expert-Score ungewichtet",
           "Expoert-Score Trennung",
           "Export-Score Trennung Sum",
           "Durchschnittlicher Anteil größtes Cluster",
           "Varianz des Anteils vom jeweils größtem Cluster",
           "SD des Anteils vom jeweils größtem Cluster",
           "Durchschnittliche Clusteranzahl pro Intervall",
           "Varianz der Clusteranzahl pro Intervall",
           "SD der Clusteranzahl pro Intervall",
           "Summe aller Abweichungen innerhalb des jeweiligem Intervall",
           "Durchschnittliche Abweichung",
           "Summe aller Varianzen innerhalb des jeweiligem Intervall",

           "Silhoutte",
           "Partition Entropie",
           "Partition Koeffizient",
           "Modifizierte Partition Koeffizienz",
           "Jaccard Index",
           "Fuzzy Rand Index",
           "Xie Beni",
           "Ges. Abstand zwischen den Clustern",
           "Ges. Abstand in den Clustern",

           "Cluster-Größen gesamt",
           "Cluster-Größen durch.",
           "Cluster-Größen SD",
           "Cluster-Größen min",
           "Cluster-Größen max"])

    summary_add = pd.DataFrame(
        index=["Datensatz",
           "Subset",
           "Algo",
           "Split",
           "Starts",
           "IterMax",
           "Fuzziness",
            "Cluster-Anzahl",
            "Größtes Cluster Anteile Boxplot-min",
           "Größtes Cluster Anteile Boxplot-q1",
           "Größtes Cluster Anteile Boxplot-meadian",
           "Größtes Cluster Anteile Boxplot-q3",
           "Größtes Cluster Anteile Boxplot-max",
           "Cluster Anzahl Boxplot-min",
           "Cluster Anzahl Boxplot-q1",
           "Cluster Anzahl Boxplot-median",
           "Cluster Anzahl Boxplot-q3",
           "Cluster Anzahl Boxplot-max",
           "Cluster-Größen gesamt:",
           "Cluster-Größen durch.:",
           "Cluster-Größen SD",
           "Cluster-Größen var",
           "Cluster-Größen min",
           "Cluster-Größen q1",
           "Cluster-Größen median",
           "Cluster-Größen q3",
           "Cluster-Größen max"])

    summary_full = pd.DataFrame(
        index=["Datensatz",
           "Subset",
           "Algo",
           "Split",
           "Starts",
           "IterMax",
           "Fuzziness",
            "Cluster-Anzahl",
            "Expert-Score gewichtet",
            "Expert-Score Gruppengröße",
           "Expert-Score ungewichtet",
           "Expoert-Score Trennung",
           "Export-Score Trennung Sum",
           "Durchschnittlicher Anteil größtes Cluster",
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
           "Jaccard Index",
           "Fuzzy Rand Index",
           "Xie Beni",
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
           "Cluster Anzahl Boxplot-max",
           "Cluster-Größen gesamt",
           "Cluster-Größen durch.",
           "Cluster-Größen SD",
           "Cluster-Größen var",
           "Cluster-Größen min",
           "Cluster-Größen q1",
           "Cluster-Größen median",
           "Cluster-Größen q3",
           "Cluster-Größen max"])

    subset_name = subset_entry[1]
    cstart = subset_entry[7]
    cend = subset_entry[8]
    cstep = subset_entry[9]
    split_part = subset_entry[3]
    split_len = subset_entry[2]
    alt_name = subset_entry[10]

    c = cstart * cstep
    cend = cend * cstep
    clist = []

    while c <= cend:
        clist.append(c)
        c += cstep

    split_parts = 10618 // split_len
    split_string = "_split(" + str(split_len) + "_" + str(split_part) + "-" + str(split_parts) + "))"




    starts = subset_entry[4]
    itermax = subset_entry[5]
    fuzziness = subset_entry[6]



    for clustercount in clist:



        config = alt_name + "(s" + str(starts) + "imax" + str(itermax) + "k" + str(clustercount) + "m" + str(
            fuzziness) + ")__"

        try:
            try:
                dataset = "data(small(" + subset_name + ")" + dataset_origin + split_string
                data_file = config + dataset + "_clust.csv"
                data = pd.read_csv(data_file)
            except:
                dataset = "data(" + subset_name + ")"
                data_file = config + dataset + "_clust.csv"
                data = pd.read_csv(data_file)

            cluster = pd.DataFrame(data)



            # print(cluster.keys())
            directory_position = int(cluster.keys().get_loc("directory1"))
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
            #print(clusterlist_big)
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
            prob_sd = []                                #Schema: [pro intervall: [Intervallgröße, c1-Zuordnung-SD] ... [Intervallgröße, k-te Zuordnung-SD]]
            prob_var = []

            for n, cl_big in enumerate(clusterlist_big, 0):
                clusternumber_min = 2
                clusternumber_max = clustercount

                intervall_end = intervall_start + len(cl_big)

                # ließt innerhalb eines Intervalls, pro Clusterzentrum, je die prob-Zuordnungen aus
                for cl_num in range(clusternumber_min, (clusternumber_min + clusternumber_max)):
                    cl_probabilities = cluster.iloc[intervall_start:intervall_end, cl_num]
                    # print(prob1)

                    prob_intervall_cl_list = cl_probabilities.values.tolist()
                   # prob_var_list2 = []

                    # wandelt Liste nur um von [[[]],[[]]] in [[],[]]
                   # for sd_entry in prob_var_list1:
                     #   prob_var_list2.append(sd_entry)



                    var, sd = analysis.variance(prob_intervall_cl_list)
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
            print("Summe aller Standardabweichungen(<- pro Zentrum pro Intervall) multipliziert mit der jeweiligen Intervallgröße\t", sum_sd)
            #print(n)

            n = 0
            sum_var = 0                             # für jedes Objekt einmal seine Varianz gezählt
            for entry in prob_var:
                sum_var += entry[0] * entry [1]
                n += entry[0]
            print("Summe aller Varianzen multipliziert(<- pro Zentrum pro Intervall) mit der jeweiligen Intervallgröße\t", sum_var)
            #print(n)


               # intervall_start += len(cl_big)

            print(data_file)


        #Expert-Score:
            expert_filename = "D:/MEGAsync/BArbeit/Data/expert_forcode" + str(split_part) + ".csv"
            expert_data = pd.read_csv(expert_filename, sep=";", header=None)
            expert_data_list = expert_data.values.tolist()

            index_position = int(cluster.keys().get_loc("index"))
            cluster_labels = cluster.iloc[:, [1, index_position]]

            # zugehörige Clusterlabels raus suchen
            old_group = int(expert_data_list[0][0])
            group_labels_small = []
            group_labels_big = []

            for expert_entry in expert_data_list:
                group = int(expert_entry[0])
                index_number = int(expert_entry[1])


                if group is old_group:
                    label = cluster_labels.loc[cluster_labels.iloc[:, 1] == index_number]
                    label = label.values.tolist()
                    if len(label) > 0:
                        group_labels_small.append(label[0][0])
                else:
                    if len(group_labels_small) > 1:
                        group_labels_big.append(group_labels_small)
                    old_group = int(expert_entry[0])

                    group_labels_small = []
                    label = cluster_labels.loc[cluster_labels.iloc[:, 1] == index_number]
                    label = label.values.tolist()
                    if len(label) > 0:
                        group_labels_small.append(label[0][0])
            # letzten Eintrag noch anhängen
            if len(group_labels_small) > 1:
                group_labels_big.append(group_labels_small)

            # auszahlen wie oft das selbe Label pro Gruppe gewählt wurde
            expert_score_list = []
            for labels in group_labels_big:
                group_labelcounter = []
                for x in range(1, clustercount+1):
                    group_labelcounter.append(labels.count(x))

                #Wenn keine Übereinstimmung soll 0 und nicht 1/n gezählt werden
                if max(group_labelcounter) > 1:
                    label_proportion = max(group_labelcounter) / len(labels)
                    expert_score_list.append([len(labels), label_proportion])
                else:
                    expert_score_list.append([len(labels), 0])

            expert_prob_sum = 0
            expert_prob_sum_waged = 0
            expert_sum_groupsize = 0
            for expert_score_listentry in expert_score_list:
                expert_group_length = expert_score_listentry[0]
                expert_group_prob = expert_score_listentry[1]

                expert_prob_sum += expert_group_prob
                expert_prob_sum_waged += expert_group_length * expert_group_prob
                expert_sum_groupsize += expert_group_length

            expert_score_prob = expert_prob_sum / len(expert_score_list)
            expert_score_prob_waged = expert_prob_sum_waged / expert_sum_groupsize

            # Expert-Score Sepperation
            old_group = int(expert_data_list[0][2])
            group_genre_small = []
            group_genre_big = []

            for expert_entry in expert_data_list:
                group = int(expert_entry[2])
                index_number = int(expert_entry[1])

                if group is old_group:
                    label = cluster_labels.loc[cluster_labels.iloc[:, 1] == index_number]
                    label = label.values.tolist()
                    if len(label) > 0:
                        group_genre_small.append(label[0][0])
                else:
                    if len(group_labels_small) > 1:
                        group_genre_big.append(group_genre_small)
                    old_group = int(expert_entry[2])

                    group_genre_small = []
                    label = cluster_labels.loc[cluster_labels.iloc[:, 1] == index_number]
                    label = label.values.tolist()
                    if len(label) > 0:
                        group_genre_small.append(label[0][0])
            # letzten Eintrag noch anhängen
            if len(group_genre_small) > 1:
                group_genre_big.append(group_genre_small)

            # auszahlen wie oft das selbe Label pro Gruppe gewählt wurde
            expert_g_label_list = []

            for labels in group_genre_big:
                group_g_labelcounter = []
                for x in range(1, clustercount + 1):
                    group_g_labelcounter.append(labels.count(x))
                expert_g_label_list.append(group_g_labelcounter)

            expert_score_group_sepperation = 0
            sum_g = 0
            for x in range(0, len(expert_g_label_list) - 2):
                for cl in range(0, clustercount):
                    expert_score_group_sepperation += abs(expert_g_label_list[x][cl] - expert_g_label_list[x + 2][cl])
                    sum_g += expert_g_label_list[x][cl]
                    sum_g += expert_g_label_list[x + 2][cl]

            expert_score_group_sepperation = expert_score_group_sepperation / sum_g

        # ClusterGrößen Analyse
            data_csize_file = config + dataset + "_cinfo.csv"
            cluster_size_data = pd.read_csv(data_csize_file)
            cluster_size_data = cluster_size_data.values.tolist()

            cluster_size = []
            cluster_size_sum = 0
            for entry in cluster_size_data:
                cluster_size_sum += entry[1]
                cluster_size.append(entry[1])


            cluster_size_mean = analysis.average(cluster_size)
            cluster_size_var, cluster_size_sd = analysis.variance(cluster_size)
            cluster_size_box = analysis.Boxplot(cluster_size)

        # lade restliche, schon vorhandene ValidierungsDaten
            data_val_file = config + dataset + "_val.csv"
            data_val = pd.read_csv(data_val_file)

            silh = data_val.iloc[0, 2]
            partition_entropy = data_val.iloc[0, 3]
            partition_coefficient = data_val.iloc[0, 4]
            partition_mod_coef = data_val.iloc[0, 5]
            ss_between = data_val.iloc[0, 6]
            ss_in = data_val.iloc[0, 7]
            if len(data_val.count(axis=0)) >= 10:

                jaci = data_val.iloc[0, 8]
                ri = data_val.iloc[0, 9]
                xb = data_val.iloc[0, 10]
            else:
                print(len(data_val.count(axis=0)))
                jaci = "nan"
                ri = "nan"
                xb = "nan"



            config = re.sub("__", "", config)
            summary_main[clustercount] = [dataset_origin,
                                          subset_name,
                                          subset_entry[1],
                                          split_string,
                                          starts,
                                          itermax,
                                          fuzziness,
                                          clustercount,
                                          expert_score_prob_waged,
                                          expert_sum_groupsize,
                                          expert_score_prob,
                                          expert_score_group_sepperation,
                                          sum_g,
                                          proportions_average,
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
                                          jaci,
                                          ri,
                                          xb,
                                          ss_between,
                                          ss_in,

                                          cluster_size_sum,
                                          cluster_size_mean,
                                          cluster_size_sd,
                                          cluster_size_box.min,
                                          cluster_size_box.max]

            summary_add[clustercount] = [dataset_origin,
                                          subset_name,
                                          subset_entry[1],
                                          split_string,
                                          starts,
                                          itermax,
                                          fuzziness,
                                          clustercount,
                                         proportions_box.min,
                                        proportions_box.q1,
                                        proportions_box.median,
                                        proportions_box.q3,
                                        proportions_box.max,
                                        counter_box.min,
                                        counter_box.q1,
                                        counter_box.median,
                                        counter_box.q3,
                                        counter_box.max,
                                        cluster_size_sum,
                                         cluster_size_mean,
                                         cluster_size_sd,
                                         cluster_size_var,
                                         cluster_size_box.min,
                                         cluster_size_box.q1,
                                         cluster_size_box.median,
                                         cluster_size_box.q3,
                                         cluster_size_box.max]

            summary_full[clustercount] = [dataset_origin,
                                          subset_name,
                                          subset_entry[1],
                                          split_string,
                                          starts,
                                          itermax,
                                          fuzziness,
                                          clustercount,
                                          expert_score_prob_waged,
                                          expert_sum_groupsize,
                                          expert_score_prob,
                                          expert_score_group_sepperation,
                                          sum_g,
                                          proportions_average,
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
                                          jaci,
                                          ri,
                                          xb,
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
                                          counter_box.max,
                                          cluster_size_sum,
                                          cluster_size_mean,
                                          cluster_size_sd,
                                          cluster_size_var,
                                          cluster_size_box.min,
                                          cluster_size_box.q1,
                                          cluster_size_box.median,
                                          cluster_size_box.q3,
                                          cluster_size_box.max]

            sumsum_main[nsum] =  [dataset_origin,
                                          subset_name,
                                          alt_name,
                                          split_string,
                                          starts,
                                          itermax,
                                          fuzziness,
                                          clustercount,
                                          expert_score_prob_waged,
                                          expert_sum_groupsize,
                                          expert_score_prob,
                                          expert_score_group_sepperation,
                                          sum_g,
                                          proportions_average,
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
                                          jaci,
                                          ri,
                                          xb,
                                          ss_between,
                                          ss_in,

                                          cluster_size_sum,
                                          cluster_size_mean,
                                          cluster_size_sd,
                                          cluster_size_box.min,
                                          cluster_size_box.max]

            sumsum_add[nsum] = [dataset_origin,
                                          subset_name,
                                          alt_name,
                                          split_string,
                                          starts,
                                          itermax,
                                          fuzziness,
                                          clustercount,
                                         proportions_box.min,
                                        proportions_box.q1,
                                        proportions_box.median,
                                        proportions_box.q3,
                                        proportions_box.max,
                                        counter_box.min,
                                        counter_box.q1,
                                        counter_box.median,
                                        counter_box.q3,
                                        counter_box.max,
                                        cluster_size_sum,
                                         cluster_size_mean,
                                         cluster_size_sd,
                                         cluster_size_var,
                                         cluster_size_box.min,
                                         cluster_size_box.q1,
                                         cluster_size_box.median,
                                         cluster_size_box.q3,
                                         cluster_size_box.max]

            sumsum_full[nsum] = [dataset_origin,
                                          subset_name,
                                          alt_name,
                                          split_string,
                                          starts,
                                          itermax,
                                          fuzziness,
                                          clustercount,
                                          expert_score_prob_waged,
                                          expert_sum_groupsize,
                                          expert_score_prob,
                                          expert_score_group_sepperation,
                                          sum_g,
                                          proportions_average,
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
                                          jaci,
                                          ri,
                                          xb,
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
                                          counter_box.max,
                                          cluster_size_sum,
                                          cluster_size_mean,
                                          cluster_size_sd,
                                          cluster_size_var,
                                          cluster_size_box.min,
                                          cluster_size_box.q1,
                                          cluster_size_box.median,
                                          cluster_size_box.q3,
                                          cluster_size_box.max]
            nsum += 1
        except:
            failed.append(subset_entry)

    print(summary_main)
    config = alt_name + "(s" + str(starts) + "imax" + str(itermax) + "k" + str(clustercount) + "m" + str(fuzziness) + ")__"
    data_file = config + "data(" + dataset

    summaryname_main = "summary_" + str(cstart) + "_" + str(cend) + data_file + ".csv"
    summary_main.to_csv(summaryname_main)

    summaryname_add = "summary_add_" + str(cstart) + "_" + str(cend) + data_file + ".csv"
    summary_add.to_csv(summaryname_add)

    summaryname_full = "summary_full_" + str(cstart) + "_" + str(cend) + data_file + ".csv"
    summary_full.to_csv(summaryname_full)

sumsumname_main = "sumsum" + str(len(subset)) + "-" + str(nsum) + "_" + sumsumindicator + ".csv"
sumsum_main.to_csv(sumsumname_main)

sumsumname_add = "sumsum_add_" + str(len(subset)) + "-" + str(nsum) + "_" + sumsumindicator + ".csv"
sumsum_add.to_csv(sumsumname_add)

sumsumname_full = "sumsum_full_" + str(len(subset)) + "-" + str(nsum) + "_" + sumsumindicator + ".csv"
sumsum_full.to_csv(sumsumname_full)

failed_data = pd.DataFrame(failed)
failed_data.to_csv("failed_fcmpp.csv")