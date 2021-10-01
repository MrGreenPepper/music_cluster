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
dict = "D:/MEGAsync/BArbeit/Data/data/"
dict_results = "D:/MEGAsync/BArbeit/Data/cluster_results/"


special_rows = 0

# (algo, db, split1, split2, starts, imax, fuzziness, cmin, cmax, step_s, alt)
work_load = rbind(c("fcmpp", "special", 2000, 1, 2, 2, 1.5, 1, 3, 5, "fcmpp"),
                  c("fcmpp", "special2", 2000, 1, 2, 2, 1.5, 1, 3, 5, "fcmpp"),
                  c("fcmpp", "special3", 2000, 1, 2, 2, 1.5, 1, 3, 5, "fcmpp"))

nr = as.numeric(nrow(work_load))

for (n in 1:nr){
  print(n)
  
  algo_name <- work_load[n, 1]
  dataset <- work_load[n, 2]
  split_len = as.numeric(work_load[n, 3])
  split_part = as.numeric(work_load[n, 4])
#  starts = 2
#  imax = 2
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
  
  
  data_o <- read.csv(data_file, header=TRUE, sep = ",")
  nrows = nrow(data_o)
  ncols = ncol(data_o)
  special_columns <- (which(names(data_o) == "name") + 1)
  data_s <- data_o[(special_rows:nrows) , (special_columns:ncols)]
  t_scaled <- scale(data_s)
  
  
  #   
  # #  # PCA
  p_scaled <- prcomp(t_scaled)
  eig = p_scaled$sdev^2
  eig
  crit = mean(eig)*0.7
  crit
  ncrit = 1
  # #
  eig[ncrit] > crit
  while (eig[ncrit] > crit) {
    ncrit = ncrit + 1
  }
  ncrit = ncrit - 1
  t_scaled =  p_scaled$x[,(1:ncrit)]
  t_scaled


  
  valsum = data.frame()
  for(nv in cmin:cmax) {
    clusteranzahl = ( nv * step_size )
    
    algo_name = altname
    #algo_name = paste("kmean", "(i:", toString(iterations), ")", sep = "")
    
    title = paste(algo_name, " (s:", toString(starts), " imax:", toString(imax),"m:", fuzziness, ")",  " - k=", toString(clusteranzahl), sep = "")
    
    #filenames 
    #save_filename = paste(algo_name, "(s", toString(starts), "imax", toString(imax), "k", toString(clusteranzahl), "m", toString(fuzziness), ")_", "config(", conf, ")_", sep="")
    save_filename = paste(algo_name, "(s", toString(starts), "imax", toString(imax), "k", toString(clusteranzahl), "m", toString(fuzziness), ")_", sep="")
    save_filename = paste(save_filename, data_filename, sep = "")
    save_file = paste(dict_s, save_filename, sep = "")
    
    print(save_filename)
    
    filename_clust = paste(save_file, "_clust.csv", sep = "")
    filename_val = paste(save_file, "_val.csv", sep = "")
    filename_info = paste(save_file, "_cinfo.csv", sep = "")
    filename_pdf  = paste(save_file, ".pdf", sep = "")
    
    
    #Algo    
    set.seed(20)
    # https://www.rdocumentation.org/packages/ppclust/versions/0.1.3/topics/fcm
    v <- inaparc::kmpp(t_scaled, k=clusteranzahl)$v
    cluster_data <- fcm(t_scaled, centers = v, nstart = starts, iter.max = imax, m = fuzziness)
    
    cluster_data$cluster
    
    
    
    
    
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
    
    print(cluster_data$cluster)
    print(cluster_data$u)
    
    #  try(jaci <- JACCARD.F(cluster_data$cluster, cluster_data$u))
    #  try(ri <- RI.F(cluster_data$cluster, cluster_data$u))
    #  try(xb <- XB(t_scaled, cluster_data$u, cluster_data$v, fuzziness))
    
    
    
    
    
    
    #  clustval = data.frame(clusteranzahl, silf, parent, parcoef, modparcoef, cluster_data$sumsqrs$between.ss, cluster_data$sumsqrs$tot.within.ss, jaci, ri, xb)
    clustval = data.frame(clusteranzahl, silf, parent, parcoef, modparcoef, cluster_data$sumsqrs$between.ss, cluster_data$sumsqrs$tot.within.ss)
    valsum = rbind(valsum, clustval)
    write.csv(clustval, filename_val)
    
    #Save Clustering Data
    filename_centers = paste(save_file, "_centers.csv", sep = "")
    write.csv(cluster_data$v, filename_centers, fileEncoding = "UTF-8")
    
    filename_v0 = paste(save_file, "_v0.csv", sep = "")
    write.csv(cluster_data$v0, filename_v0,  fileEncoding = "UTF-8")
    
    filename_d = paste(save_file, "_d.csv", sep = "")
    write.csv(cluster_data$d, filename_d,  fileEncoding = "UTF-8")
    
    filename_x = paste(save_file, "_x.csv", sep = "")
    write.csv(cluster_data$x, filename_x,  fileEncoding = "UTF-8")
    
    #Cluster-Grafik
    pdf(filename_pdf)
    plot(cluster_data$cluster, main=title, xlab="Index", ylab="Cluster", type="p", pch=19, cex=0.1)
    dev.off()
    
    #Cluster-Zuordnung
    frame = data.frame(cluster_data$cluster, cluster_data$u, data_o[1:nrows, 2:7])
    write.csv(frame, filename_clust,  fileEncoding = "UTF-8")
    
    #Cluster-GrÃ¶Ãen
    write.csv(cluster_data$csize, filename_info,  fileEncoding = "UTF-8")
    
    
    
    print(save_filename)
    
    
  }
  
  valsum
  
  cstart = cmin * step_size
  cend = cmax * step_size
  filename_valsum = paste(save_file, "_valsum", cstart,"-", cend, ".csv", sep = "")
  write.csv(valsum, filename_valsum)
  
  
  write.table(rbind(work_load[n,]), file = "D:/MEGAsync/BArbeit/Data/cluster_results/done_pcs_fcmpp.csv", sep = ",", append = TRUE, quote = FALSE,
              col.names = FALSE, row.names = FALSE)
}

  
 
  
  


