install.packages("ppclust")
install.packages("fclust")
install.packages("cluster")
install.packages("factorextra")
install.packages("fpc")
install.packages("NbClust")

rm(list = ls())

library(fpc)
library(NbClust)
library(factoextra)
library(cluster)
library(fclust)
library(ppclust)



dataset_full = "fulldata(so_cl_zo90)_split(2000_0-5)"

dict = "D:/MEGAsync/BArbeit/MusicCluster/Data/rawData/"
dict_s = "D:/MEGAsync/BArbeit/MusicCluster/Data/fcmpp/s/"


algo_name = "fcmpp"
reduction = "single"
starts = 10
imax = 100
clusteranzahl = 9
cmin = 9
cmax = 9
step_size = 1
fuzziness = 1.5

special_rows = 0                  # Zeilen am Ende mit ohne Merkmale (Index Daten usw.)
special_columns = 8               # Spalten am Anfang ohne Merkmals-Daten (Index Daten usw.)

# Daten laden
dataset_small = "small("
dataset_small = paste(dataset_small, reduction, ")", dataset_full, sep="")

origin_filename = paste(dataset_small, sep = "")
path_origin_filename = paste(dict, origin_filename, ".csv", sep = "")

data_o <- read.csv(path_origin_filename, header=TRUE)
nrows = nrow(data_o)
ncols = ncol(data_o)
data_s <- data_o[(special_rows:nrows) , (special_columns:ncols)]
t_scaled <- scale(data_s)

# Test bei zwei mal 0 ok
sum(is.na(data_s))
sum(is.numeric(data_s))
sum(is.na(data_s))


for(n in cmin:cmax) {
  clusteranzahl = ( n * step_size )
  
  
  #algo_name = paste("kmean", "(i:", toString(iterations), ")", sep = "")
  
 
  
  #save_filename = paste(algo_name, "(s", toString(starts), "imax", toString(imax), "k", toString(clusteranzahl), "m", toString(fuzziness), ")_", "config(", conf, ")_", sep="")
  config = paste(algo_name, "(s", toString(starts), "imax", toString(imax), "k", toString(clusteranzahl), "m", toString(fuzziness), ")_", sep="")
  clust_filename = paste(config, "_data(", origin_filename, ")_clust.csv", sep = "")
  clust_filename
  path_clust_filename = paste(dict_s, clust_filename, sep = "")
  

  data_clust <- read.csv(path_clust_filename, header=TRUE)
  
  ncols = 2 + clusteranzahl
  
  data_clust_s = data_clust[,(3:ncols)]
  data_clust_s
  set.seed(20)
  
  tfcm <- FKM(t_scaled, k=9, m=1.5)  
  tfcm$H
  xiebeni <- XB(Xca = data_s, U = data_clust_s, m = fuzziness)
  write.csv(clustval, filename_xiebeni)
  
  print(save_filename)
  
  filename_xiebeni = paste(load_file, "_xiebeni.csv", sep = "")
  
}
valsum

cstart = cmin * step_size
cend = cmax * step_size
filename_valsum = paste(save_file, "_valsum", cstart,"-", cend, ".csv", sep = "")
write.csv(valsum, filename_valsum)

