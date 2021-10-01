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



dataset = "small(single_normal_tonal)fulldata(so_cl_zo90)_split(2000_0-5)"
# dict = "~/MEGAsync/BArbeit/MusicCluster/Data/rawData/"
dict = "D:/MEGAsync/BArbeit/MusicCluster/Data/rawData/"
dict_s = "D:/MEGAsync/BArbeit/MusicCluster/Data/fcm/"
origin_filename = paste(dataset, ".csv", sep = "")
data_file = paste(dict, origin_filename, sep = "")

starts = 10
imax = 100
clusteranzahl = 10
cmin = 1
cmax = 3
step_size = 5
fuzziness = 1.5

special_rows = 0
special_columns = 8

# Daten laden


data_o <- read.csv(data_file, header=TRUE)
nrows = nrow(data_o)
ncols = ncol(data_o)
data_s <- data_o[(special_rows:nrows) , (special_columns:ncols)]
t_scaled <- scale(data_s)

# Test bei zwei mal 0 ok
sum(is.na(data_s))
sum(is.numeric(data_s))

sum(is.na(data_s))
valsum = data.frame()

for(n in cmin:cmax) {
  clusteranzahl = ( n * step_size )
  
  algo_name = "fcm"
  #algo_name = paste("kmean", "(i:", toString(iterations), ")", sep = "")
  
  title = paste(algo_name, " (s:", toString(starts), " imax:", toString(imax), ")",  " - k=", toString(clusteranzahl), sep = "")
  
  #save_filename = paste(algo_name, "(s", toString(starts), "imax", toString(imax), "k", toString(clusteranzahl), "m", toString(fuzziness), ")_", "config(", conf, ")_", sep="")
  save_filename = paste(algo_name, "(s", toString(starts), "imax", toString(imax), "k", toString(clusteranzahl), "m", toString(fuzziness), ")_", sep="")
  save_filename = paste(save_filename, "_data(", dataset, ")", sep = "")
  save_file = paste(dict_s, save_filename, sep = "")
  
  print(save_filename)
  
  filename_clust = paste(save_file, "_clust.csv", sep = "")
  filename_val = paste(save_file, "_val.csv", sep = "")
  filename_info = paste(save_file, "_cinfo.csv", sep = "")
  filename_pdf  = paste(save_file, ".pdf", sep = "")
  
  
  
  set.seed(20)
  # https://www.rdocumentation.org/packages/ppclust/versions/0.1.3/topics/fcm

  cluster_data <- fcm(t_scaled, k = clusteranzahl, nstart = starts, iter.max = imax, m = fuzziness)
  
  cluster_data$v
  
  #Cluster-Grafik
  pdf(filename_pdf)
  plot(cluster_data$cluster, main=title, xlab="Index", ylab="Cluster", type="p", pch=19, cex=0.1)
  dev.off()
  
  
  
  #Cluster-Zuordnung
  frame = data.frame(cluster_data$cluster, cluster_data$u, data_o[1:nrows, 2:7])
  frame
  write.csv(frame, filename_clust)
  
  cluster_data$cluster
  
  #Cluster-GrÃ¶Ãen
  write.csv(cluster_data$csize, filename_info)
  
  
  
  #Cluster-Validierung
  #http://rpubs.com/rahulSaha/Fuzzy-CMeansClustering
  silf <- SIL.F(data_s, cluster_data$u, alpha=1)
  
  parent <- PE(cluster_data$u)
  
  parent
  
  parcoef <- PC(cluster_data$u)
  parcoef
  
  modparcoef <- MPC(cluster_data$u)
  modparcoef
  
  cluster_data$sumsqrs$between.ss
  cluster_data$sumsqrs$within.ss
  cluster_data$sumsqrs$tot.within.ss
  cluster_data$sumsqrs$tot.ss
  
  clustval = data.frame(clusteranzahl, silf, parent, parcoef, modparcoef, cluster_data$sumsqrs$between.ss, cluster_data$sumsqrs$tot.within.ss)
  clustval
  
  
  valsum = rbind(valsum, clustval)
  write.csv(clustval, filename_val)
  
  filename_centers = paste(save_file, "_centers.csv", sep = "")
  write.csv(cluster_data$v)
  
  print(save_filename)
  
  
}
valsum

cstart = cmin * step_size
cend = cmax * step_size
filename_valsum = paste(save_file, "_valsum", cstart,"-", cend, ".csv", sep = "")
write.csv(valsum, filename_valsum)

