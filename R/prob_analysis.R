install.packages("ppclust")
install.packages("fclust")
install.packages("cluster")
install.packages("factorextra")
install.packages("fpc")
install.packages("NbClust")
install.packages("FPDclustering")
install.packages("e1071")
install.packages("clValid")

install.packages("knitr")
install.packages("advfclust", repos="http://R-Forge.R-project.org")

rm(list = ls())

library(fpc)
library(NbClust)
library(factoextra)
library(cluster)
library(fclust)
library(ppclust)
library(FPDclustering)
library(e1071)
library(clValid)
library(advfclust)
# Daten Konfiguration

dataset = "small(single)fulldata(so_cl_zo90)_split(2000_0-5)"
#dict = "~/MEGAsync/BArbeit/MusicCluster/Data/rawData/"
dict = "D:/MEGAsync/BArbeit/MusicCluster/Data/rawData/"
dict_s = "D:/MEGAsync/BArbeit/MusicCluster/Data/probD/"
origin_filename = paste(dataset, ".csv", sep = "")
data_file = paste(dict, origin_filename, sep = "")

clusteranzahl = 10
cmin = 2
cmax = 5
step_size = 1
distanz = "euc"

special_rows = 0
special_columns = 8

# Daten laden
data_o <- read.csv(data_file, header=TRUE)
nrows = nrow(data_o)
ncols = ncol(data_o)
data_s <- data_o[(special_rows:nrows) , (special_columns:ncols)]
t_scaled <- scale(data_s)


cluster_data1 <- PDclust(data = t_scaled, k = clusteranzahl)
cluster_data1$probability

cluster.stats(dist(t_scaled), alt.clustering = "")
v <- inaparc::kmpp(t_scaled, k=5)$v
ftest1 <- fuzzy.CM(t_scaled, K=5, membership(v), m= 1.5, max.iteration = 1, threshold = 100000000000000000000000)
ftest2 <- fuzzy.GK()

index <- fclustIndex(cluster_data$probability, t_scaled, index = "all")
resultindexes <- fclustIndex(t_scaled, t_scaled, index="all")

itest <- cluster.stats(dist(t_scaled), cluster_data$label, sepindex = TRUE)
itest

ftest1$member
cluster_data$u
itest <- validation.index(ftest1)
itest

data <- cutree(cluster_data1$label)
dtest <- dunn(dist(t_scaled), cluster_data1$probability)
dtest

cluster_data$u


