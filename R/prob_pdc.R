install.packages("ppclust")
install.packages("fclust")
install.packages("cluster")
install.packages("factorextra")
install.packages("fpc")
install.packages("NbClust")
install.packages("advclust")
install.packages("clusterCrit")

rm(list = ls())

library(FPDclustering)
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
dict = "D:/MEGAsync/BArbeit/Data/data/"
dict_results = "D:/MEGAsync/BArbeit/Data/cluster_results/"


special_rows = 0
special_columns = 6

# (algo, db, split1, split2, starts, imax, fuzziness, cmin, cmax, step_s, alt)
work_load = rbind(#c("pdc", "special", 2000, 0, 1, 3, 5, "pdc"),
                  #c("pdc", "special2", 2000, 0, 1, 3, 5, "pdc"),
                  c("pdc", "special", 2000, 1, 5, 15, 1, "pcs_pdc"),
                  c("pdc", "special2", 2000, 1, 5, 15, 1, "pcs_pdc"),
                  c("pdc", "special3", 2000, 1, 5, 15, 1, "pcs_pdc"))

nr = as.numeric(nrow(work_load))

for (n in 1:nr){
  print(n)
  
  algo_name <- work_load[n, 1]
  dataset <- work_load[n, 2]
  split_len = as.numeric(work_load[n, 3])
  split_part = as.numeric(work_load[n, 4])


  cstart  =as.numeric(work_load[n, 5])
  cend = as.numeric(work_load[n, 6])
  cstep  = as.numeric(work_load[n, 7])
  altname <- work_load[n, 8]
  
  split_parts = (origin_rows - (origin_rows %% split_len)) / split_len
  
  dict_s = paste(dict_results, algo_name, "/", sep = "")
  
  data_filename = paste("small(", dataset, ")", origin_dataset, "_split(", split_len, "_", split_part, "-", split_parts ,")", sep = "")
  data_file = paste(dict, data_filename, ".csv", sep = "")
  
  data_o <- read.csv(data_file, header=TRUE, sep = ",")
  nrows = nrow(data_o)
  ncols = ncol(data_o)
  data_s <- data_o[(special_rows:nrows) , (special_columns:ncols)]
  t_scaled <- scale(data_s)
  
  
  
 # PCA
p_scaled <- prcomp(t_scaled)
 eig = p_scaled$sdev^2
eig
 crit = mean(eig)*0.7
 crit
 ncrit = 1
  #
   eig[ncrit] > crit
   while (eig[ncrit] > crit) {
    ncrit = ncrit + 1
   }
   ncrit = ncrit - 1
   t_scaled =  p_scaled$x[,(1:ncrit)]
   t_scaled
#    
   
  
   cmin = cstart
   cmax = cend
   step_size = cstep
  
  
  
  valsum = data.frame()
  for(nv in cmin:cmax) {
    clusteranzahl = ( nv * step_size )
    
    algo_name = altname
    #algo_name = paste("kmean", "(i:", toString(iterations), ")", sep = "")
    
    title = paste(algo_name, " - k=", toString(clusteranzahl), sep = "")
    
    #filenames 
    #save_filename = paste(algo_name, "(s", toString(starts), "imax", toString(imax), "k", toString(clusteranzahl), "m", toString(fuzziness), ")_", "config(", conf, ")_", sep="")
    save_filename = paste(algo_name, "(k", toString(clusteranzahl), ")_", sep="")
    save_filename = paste(save_filename, "_data(", data_filename, ")", sep = "")
    save_file = paste(dict_s, save_filename, sep = "")
    
    print(save_filename)
    
    filename_clust = paste(save_file, "_clust.csv", sep = "")
    filename_val = paste(save_file, "_val.csv", sep = "")
    filename_info = paste(save_file, "_label.csv", sep = "")
    filename_pdf  = paste(save_file, ".pdf", sep = "")
    
    
    #Algo    
    set.seed(20)
    # https://www.rdocumentation.org/packages/ppclust/versions/0.1.3/topics/fcm
    cluster_data <- PDclust(data = t_scaled, k = clusteranzahl)
    
    cluster_data$label
    
    
    
    
    
    #Cluster-Validierung
    #http://rpubs.com/rahulSaha/Fuzzy-CMeansClustering
    silf <- SIL.F(data_s, cluster_data$probability, alpha=1)
    
    parent <- PE(cluster_data$probability)
    
    parent
    
    parcoef <- PC(cluster_data$probability)
    parcoef
    
    modparcoef <- MPC(cluster_data$probability)
    modparcoef
    
    
    
    print(cluster_data$label)
    print(cluster_data$probability)
    
    try(jaci <- JACCARD.F(cluster_data$label, cluster_data$probability))
    try(ri <- RI.F(cluster_data$label, cluster_data$probability))
    try(xb <- XB(t_scaled, cluster_data$probability, cluster_data$centers, 2))
    
    
    
    
    
    
    #  clustval = data.frame(clusteranzahl, silf, parent, parcoef, modparcoef, cluster_data$sumsqrs$between.ss, cluster_data$sumsqrs$tot.within.ss, jaci, ri, xb)
    clustval = data.frame(clusteranzahl, silf, parent, parcoef, modparcoef, jaci, ri, xb)
    # clustval = data.frame(clusteranzahl, silf, parent, parcoef, modparcoef)
    valsum = rbind(valsum, clustval)
    write.csv(clustval, filename_val, fileEncoding = "UTF-8")
    
    #Save Clustering Data
    filename_centers = paste(save_file, "_centers.csv", sep = "")
    write.csv(cluster_data$centers, filename_centers, fileEncoding = "UTF-8")
    
    filename_v0 = paste(save_file, "_iter.csv", sep = "")
    write.csv(cluster_data$iter, filename_v0, fileEncoding = "UTF-8")
    
    filename_d = paste(save_file, "_jdf.csv", sep = "")
    write.csv(cluster_data$jdf, filename_d, fileEncoding = "UTF-8")
    
    filename_x = paste(save_file, "_prob.csv", sep = "")
    write.csv(cluster_data$probability, filename_x, fileEncoding = "UTF-8")
    
    #Cluster-Grafik
    pdf(filename_pdf)
    plot(cluster_data$label, main=title, xlab="Index", ylab="Cluster", type="p", pch=19, cex=0.1)
    dev.off()
    
    #Cluster-Zuordnung
    frame = data.frame(cluster_data$label, cluster_data$probability, data_o[1:nrows, 2:7])
    write.csv(frame, filename_clust, fileEncoding = "UTF-8")
    
    #Cluster-GrÃ¶Ãen
    write.csv(cluster_data$label, filename_info, fileEncoding = "UTF-8")
    
    
    
    print(save_filename)
    
    
  }
  valsum
  
  cstart = cmin * step_size
  cend = cmax * step_size
  filename_valsum = paste(save_file, "_valsum", cstart,"-", cend, ".csv", sep = "")
  write.csv(valsum, filename_valsum, fileEncoding = "UTF-8")
  
  write.table(rbind(work_load[n,]), file = "D:/MEGAsync/BArbeit/Data/cluster_results/done_pdc.csv", sep = ",", append = TRUE, quote = FALSE,
              col.names = FALSE, row.names = FALSE)
  
} 
