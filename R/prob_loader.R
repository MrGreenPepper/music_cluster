install.packages("ppclust")
install.packages("fclust")
install.packages("cluster")
install.packages("factorextra")
install.packages("fpc")
install.packages("NbClust")
install.packages("advclust")
install.packages("clusterCrit")

rm(list = ls())

library(fpc)
library(NbClust)
library(factoextra)
library(cluster)
library(fclust)
library(ppclust)
#library(advclust)



origin_dataset = "fulldata(so_cl_zo90)"
origin_rows = 10618
# dict = "~/MEGAsync/BArbeit/MusicCluster/Data/rawData/"
dict = "D:/MEGAsync/BArbeit/MusicCluster/Data/data/"
dict_results = "D:/MEGAsync/BArbeit/MusicCluster/Data/cluster_results/"


special_rows = 0
special_columns = 8

# (algo, db, split1, split2, starts, imax, fuzziness, cmin, cmax, step_s, alt)
work_load = rbind(c("fcmpp", "special", 2000, 1, 2, 2, 1.5, 1, 3, 5, "fcmpp"),
                  c("fcmpp", "special2", 2000, 1, help2, 2, 1.5, 1, 3, 5, "fcmpp"),
                  c("fcmpp", "special3", 2000, 1, 2, 2, 1.5, 1, 3, 5, "fcmpp"))

nr = as.numeric(nrow(work_load))

for (n in 1:nr){
  print(n)

  algo_name <- work_load[n, 1]
  dataset <- work_load[n, 2]
  split_len = as.numeric(work_load[n, 3])
  split_part = as.numeric(work_load[n, 4])
  starts  = as.numeric(work_load[n, 5])
  imax = as.numeric(work_load[n, 6])
  fuzziness  = as.numeric(work_load[n, 7])
  cstart  =as.numeric(work_load[n, 8])
  cend = as.numeric(work_load[n, 9])
  cstep  = as.numeric(work_load[n, 10])
  altname <- work_load[n, 11]
  split_parts = (origin_rows - (origin_rows %% split_len)) / split_len
  
  dict_s = paste(dict_results, algo_name, "/", sep = "")
  
  data_filename = paste("small(", dataset, ")", origin_dataset, "_split(", split_len, "_", split_part, "-", split_parts ,")", sep = "")
  data_file = paste(dict, data_filename, ".csv", sep = "")
  
  data_o <- read.csv(data_file, header=TRUE)
  nrows = nrow(data_o)
  ncols = ncol(data_o)
  data_s <- data_o[(special_rows:nrows) , (special_columns:ncols)]
  t_scaled <- scale(data_s)
  
  
  cluster_algo <- match.fun(algo_name)
  cluster_algo(starts, imax, fuzziness, t_scaled, altname, cstart, cend, cstep, data_filename)
}
 
