import pandas as pd
import os


subset = pd.read_csv("D:/MEGAsync/BArbeit/Data/cluster_results/done_pdc.csv", header=None)
datasetname_origin = "fulldata(so_cl_zo90)"
os.chdir("D:/MEGAsync/BArbeit/Data/cluster_results/pdc/")
subset = subset.as_matrix()

for subset_entry in subset:



    algo = subset_entry[0]
    subset_name = subset_entry[1]
    split_len = subset_entry[2]
    split_part = subset_entry[3]


    cstart = subset_entry[4]
    cend = subset_entry[5]
    cstep = subset_entry[6]

    alt_name = subset_entry[7]


    c = cstart * cstep
    cend = cend * cstep
    clist = []

    while c <= cend:
        clist.append(c)
        c += cstep


    split_parts = 10618 // split_len
    split_string = "_split(" + str(split_len) + "_" + str(split_part) + "-" + str(split_parts) + "))"
    dataset = "__data(small(" + subset_name + ")" + datasetname_origin

    for clustercount in clist:

        file_name_o = alt_name + "(k" + str(clustercount) + ")__data(" + subset_name + ")"
        file_center = file_name_o + "_centers.csv"
        file_clust = file_name_o + "_clust.csv"
        file_label = file_name_o + "_label.csv"

        centers = pd.read_csv(file_center)
        clust = pd.read_csv(file_clust)
        label = pd.read_csv(file_label)

        config = alt_name + "(k" + str(clustercount) + ")"
        dataset = "__data(small(" + subset_name + ")" + datasetname_origin
        file_center = config + dataset + split_string + "_centers.csv"
        file_clust = config + dataset + split_string + "_clust.csv"
        file_label = config + dataset + split_string + "_label.csv"

        centers.to_csv(file_center)
        clust.to_csv(file_clust)
        label.to_csv(file_label)