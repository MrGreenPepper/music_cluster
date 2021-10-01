install.packages("ppclust")
install.packages("fclust")
install.packages("cluster")
install.packages("factorextra")
install.packages("fpc")
install.packages("NbClust")
install.packages("FPDclustering")

rm(list = ls())

library(fpc)
library(NbClust)
library(factoextra)
library(cluster)
library(fclust)
library(ppclust)
library(FPDclustering)

# Daten Konfiguration

dataset = "small(single)fulldata(so_cl_zo90)_split(2000_0-5)"
#dict = "~/MEGAsync/BArbeit/MusicCluster/Data/rawData/"
dict = "D:/MEGAsync/BArbeit/MusicCluster/Data/rawData/"
dict_s = "D:/MEGAsync/BArbeit/MusicCluster/Data/fpdc/"
origin_filename = paste(dataset, ".csv", sep = "")
data_file = paste(dict, origin_filename, sep = "")

clusteranzahl = 19
cmin = 19
cmax = 20
step_size = 1
distanz = "euc"

special_rows = 0
special_columns = 8

# Daten laden
data_o <- read.csv(data_file, header=TRUE)
nrows = nrow(data_o)
ncols = ncol(data_o)
data_s <- data_o[(0:nrows-special_rows) , (special_columns:ncols)]
t_scaled <- scale(data_s)

# Test bei zwei mal 0 ok
sum(is.na(data_s))
sum(is.numeric(data_s))
sum(is.na(data_s))


if(sum(is.na(data_s))>0)
{
  print("na Einträge in:")
  for(r in rows){  
    for(c in coloumns){
      #print(r)
      #print(c)
      if (is.na(data_s[r, c])){
        print("na:", "", c)
        print(r)
      }
    }
  }
}

entries = nrows*ncols

if(sum(is.numeric(t_scaled))=0){
} else {
  print("Keine Zahl in:")
  for(r in rows){  
    for(c in coloumns){
      #print(r)
      #print(c)
      if (is.numeric(data_o[r, c])){
      } else {
        print(c)
        print(r)
        }     
      }
    }
  }



valsum = data.frame()

un = 25
fa = 25

for(n in cmin:cmax) {
  clusteranzahl = n * step_size
  
  algo_name = "fpdc"
  
  set.seed(20)
  # https://in.mathworks.com/matlabcentral/mlc-downloads/downloads/submissions/45765/versions/1/previews/FPDC%20toolbox%20copy/Example_FPDC.m/index.html
  # https://cran.r-project.org/web/packages/FPDclustering/FPDclustering.pdf
  
  #tfactor <- TuckerFactors(data = t_scaled, nc = clusteranzahl)
  #tfactor
 
  
   #cluster_data <- FPDC(data = t_scaled, k = clusteranzahl, nu = un, nf = fa )
  cluster_data <- FPDC(data = t_scaled, k = clusteranzahl)
  
  #save_filename = paste(algo_name, "(k", toString(clusteranzahl), "nu", un, "nf", fa, "dist", distanz, ")", sep = "")
  save_filename = paste(algo_name, "(k", toString(clusteranzahl), ")", sep = "")
  save_filename = paste(save_filename, "data(", dataset, ")", sep = "")
  save_file = paste(dict_s, save_filename, sep = "")
  
  title = paste(algo_name, "k: ", toString(clusteranzahl), "nu: ", un, "nf: ", fa, "dist: ", distanz, sep = "")
  
  filename_clust = paste(save_file, "_clust.csv", sep = "")
  filename_val = paste(save_file, "_val.csv", sep = "")
  filename_info = paste(save_file, "_cinfo.csv", sep = "")
  filename_pdf  = paste(save_file, ".pdf", sep = "")
  
  
  
 
  
  cluster_data$probability
  cluster_data$explained
  
  pdf(filename_pdf)
  plot(cluster_data$label, main=title, xlab="Index", ylab="Cluster", type="p", pch=19, cex=0.1)
  dev.off()
  
  
  frame = data.frame(cluster_data$probability, data_o[1:nrows, 2:7])
  frame
  write.csv(frame, filename_clust)
  write.csv(cluster_data$size, filename_info)
  
  
  
  
  #http://rpubs.com/rahulSaha/Fuzzy-CMeansClustering
  silf <- SIL.F(t_scaled, cluster_data$probability, alpha=1)
  silf
  
  parent <- PE(cluster_data$probability)
  parent
  
  parcoef <- PC(cluster_data$probability)
  parcoef
  
  modparcoef <- MPC(cluster_data$probability)
  modparcoef
  
  clustval = data.frame(clusteranzahl, silf, parent, parcoef, modparcoef, cluster_data$JDF, cluster_data$explained, un, fa)
  clustval
  
  
  valsum = rbind(valsum, clustval)
  write.csv(clustval, filename_val)
  
  filename_centers = paste(save_file, "_centers.csv", sep = "")
  write.csv(cluster_data$v, filename_centers)
  
  filename_v0 = paste(save_file, "_v0.csv", sep = "")
  write.csv(cluster_data$v0, filename_v0)
  
  filename_d = paste(save_file, "_d.csv", sep = "")
  write.csv(cluster_data$d, filename_d)
  
  filename_x = paste(save_file, "_x.csv", sep = "")
  write.csv(cluster_data$x, filename_x)
  
  filename_centers = paste(save_file, "_centers.csv", sep = "")
  write.csv(cluster_data$centers, filename_centers)
  
  print(save_filename)
  
  
}

valsum
cstart = cmin * step_size
cend = cmax * step_size
filename_valsum = paste(save_file, "_valsum", cstart,"-", cend, ".csv", sep = "")
write.csv(valsum, filename_valsum)


clustval
valsum
cluster_data$u













cluster_data$u
plotcluster(cluster_data$u)

valtest <- clValid(cluster_data$u, nClust=clusteranzahl, validation="internal")
valtest$c

tkmean <- kmeans(data_s, centers = 10)
tkmean$cluster
dd <- dist(data_s, method = "euclidean")
valstats <- cluster.stats(dd, tkmean$cluster)
valstats$n


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
