
rm(list = ls())
}
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
work_load = rbind(
  
  # c("fcmpp", "single_tonal", 2000, 0, 100, 40, 1.5, 1, 4, 5, "fcmpp_alt30"),
  
  c("fanny", "timeline", 2000, 1, "SqEuclidean", 2000, 1.3, 1, 3, 5, "pcs_fanny"),  
  c("fanny", "timeline", 2000, 0, "SqEuclidean", 2000, 1.3, 1, 3, 5, "pcs_fanny")
  
  # c("fanny", "special2", 2000, 1, "euclidean", 500, 1.2, 1, 3, 5, "pcs_fanny"),
  # c("fanny", "special", 2000, 1, "euclidean", 500, 1.2, 1, 3, 5, "pcs_fanny"),
  # 
  # 
  # c("fanny", "special3", 2000, 1, "manhattan", 500, 1.3, 1, 3, 5, "pcs_fanny"),
  # c("fanny", "special2", 2000, 1, "manhattan", 500, 1.3, 1, 3, 5, "pcs_fanny"),
  #  c("fanny", "special", 2000, 1, "manhattan", 500, 1.3, 1, 3, 5, "pcs_fanny"),
  #  
  #  c("fanny", "special3", 2000, 1, "SqEuclidean", 500, 1.1, 1, 3, 5, "pcs_fanny"),
  # c("fanny", "special2", 2000, 1, "SqEuclidean", 500, 1.1, 1, 3, 5, "pcs_fanny"),
  #  c("fanny", "special", 2000, 1, "SqEuclidean", 500, 1.1, 1, 3, 5, "pcs_fanny")
  
  # c("fanny", "single_string", 2000, 0, "manhattan", 1000, 1.1, 1, 3, 5, "fanny5"),
  # c("fanny", "single_normal", 2000, 0, "manhattan", 1000, 1.1, 1, 3, 5, "fanny5"),
  # c("fanny", "single_string_normal", 2000, 0, "manhattan", 1000, 1.1, 1, 3, 5, "fanny5"),
  # 
  # c("fanny", "single_string", 2000, 0, "euclidean", 1000, 1.1, 1, 3, 5, "fanny5"),
  # c("fanny", "single_normal", 2000, 0, "euclidean", 1000, 1.1, 1, 3, 5, "fanny5"),
  # c("fanny", "single_string_normal", 2000, 0, "euclidean", 1000, 1.1, 1, 3, 5, "fanny5"),
  # 
  # c("fanny", "single_string", 2000, 0, "SqEuclidean", 1000, 1.1, 1, 3, 5, "fanny5"),
  # c("fanny", "single_normal", 2000, 0, "SqEuclidean", 1000, 1.1, 1, 3, 5, "fanny5"),
  # c("fanny", "single_string_normal", 2000, 0, "SqEuclidean", 1000, 1.1, 1, 3, 5, "fanny5"),
  
  
  
  
  # c("fanny", "single", 2000, 0, "SqEuclidean", 1000, 1.2, 1, 3, 5, "fanny5"),
  # c("fanny", "normal", 2000, 0, "SqEuclidean", 1000, 1.2, 1, 3, 5, "fanny5"),
  # c("fanny", "string", 2000, 0, "SqEuclidean", 1000, 1.2, 1, 3, 5, "fanny5"),
  # 
  # c("fanny", "single", 2000, 0, "manhattan", 1000, 1.2, 1, 3, 5, "fanny5"),
  # c("fanny", "normal", 2000, 0, "manhattan", 1000, 1.2, 1, 3, 5, "fanny5"),
  # c("fanny", "string", 2000, 0, "manhattan", 1000, 1.2, 1, 3, 5, "fanny5"),
  # 
  # c("fanny", "single", 2000, 0, "euclidean", 1000, 1.2, 1, 3, 5, "fanny5"),
  # c("fanny", "normal", 2000, 0, "euclidean", 1000, 1.2, 1, 3, 5, "fanny5"),
  # c("fanny", "string", 2000, 0, "euclidean", 1000, 1.2, 1, 3, 5, "fanny5"),
  # 
  # c("fanny", "single_string", 2000, 0, "manhattan", 1000, 1.2, 1, 3, 5, "fanny5"),
  # c("fanny", "single_normal", 2000, 0, "manhattan", 1000, 1.2, 1, 3, 5, "fanny5"),
  # c("fanny", "single_string_normal", 2000, 0, "manhattan", 1000, 1.2, 1, 3, 5, "fanny5"),
  # 
  # c("fanny", "single_string", 2000, 0, "euclidean", 1000, 1.2, 1, 3, 5, "fanny5"),
  # c("fanny", "single_normal", 2000, 0, "euclidean", 1000, 1.2, 1, 3, 5, "fanny5"),
  # c("fanny", "single_string_normal", 2000, 0, "euclidean", 1000, 1.2, 1, 3, 5, "fanny5"),
  # 
  # c("fanny", "single_string", 2000, 0, "SqEuclidean", 1000, 1.2, 1, 3, 5, "fanny5"),
  # c("fanny", "single_normal", 2000, 0, "SqEuclidean", 1000, 1.2, 1, 3, 5, "fanny5"),
  # c("fanny", "single_string_normal", 2000, 0, "SqEuclidean", 1000, 1.2, 1, 3, 5, "fanny5")
)

nr = as.numeric(nrow(work_load))

for (n in 1:nr){
  print(n)
  
  algo_name <- work_load[n, 1]
  dataset <- work_load[n, 2]
  split_len = as.numeric(work_load[n, 3])
  split_part = as.numeric(work_load[n, 4])
  
  me = work_load[n, 5]
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
  
  
  # cluster_algo <- match.fun(algo_name)
  #  cluster_algo(starts, imax, fuzziness, t_scaled, altname, cstart, cend, cstep, data_filename)
  
  cmin= cstart
  cmax = cend
  step_size = cstep
  algo = altname
  
  
  #PCA  
  p_scaled <- prcomp(t_scaled)
  eig = p_scaled$sdev^2
  eig
  crit = mean(eig)*0.7
  crit
  ncrit = 1
  
  eig[ncrit] > crit
  while (eig[ncrit] > crit) {
    ncrit = ncrit + 1
  }
  ncrit = ncrit - 1
  t_scaled =  p_scaled$x[,(1:ncrit)]
  t_scaled
  
  
  
  valsum = data.frame()
  for(nc in cmin:cmax) {
    clusteranzahl = ( nc * step_size )
    
    
    algo_name = algo
    #algo_name = paste("kmean", "(i:", toString(iterations), ")", sep = "")
    
    title = paste(algo_name, " (imax:", toString(imax),"m:", fuzziness, "metric:", me, ")", " - k=", toString(clusteranzahl), sep = "")
    
    #filenames 
    #save_filename = paste(algo_name, "(s", toString(starts), "imax", toString(imax), "k", toString(clusteranzahl), "m", toString(fuzziness), ")_", "config(", conf, ")_", sep="")
    save_filename = paste(algo_name, "(imax", toString(imax), "k", toString(clusteranzahl), "m", toString(fuzziness), "met", me, ")_", sep="")
    save_filename = paste(save_filename, "_data(small(", dataset, ")_split(", split_len, "_", split_part, "-", split_parts, "))", sep = "")
    save_file = paste(dict_s, save_filename, sep = "")
    
    print(save_filename)
    
    filename_clust = paste(save_file, "_clust.csv", sep = "")
    filename_val = paste(save_file, "_val.csv", sep = "")
    filename_info = paste(save_file, "_cinfo.csv", sep = "")
    filename_pdf  = paste(save_file, ".pdf", sep = "")
    
    
    #Algo    
    set.seed(20)
    # https://www.rdocumentation.org/packages/ppclust/versions/0.1.3/topics/fcm
    
    cluster_data <- fanny(t_scaled, k = clusteranzahl, maxit = imax, memb.exp = fuzziness, metric = me)
    
    
    
    #Cluster-Validierung
    #http://rpubs.com/rahulSaha/Fuzzy-CMeansClustering
    silf <- SIL.F(t_scaled, cluster_data$membership)
    silf
    
    parent <- PE(cluster_data$membership)
    
    parent
    
    parcoef <- PC(cluster_data$membership)
    parcoef
    
    modparcoef <- MPC(cluster_data$membership)
    modparcoef
    
    
    
    
    
    jaci <- JACCARD.F(cluster_data$clustering, cluster_data$membership)
    ri <- RI.F(cluster_data$clustering, cluster_data$membership)
    #   xb <- XB(t_scaled, cluster_data$membership, cluster_data$v, fuzziness)
    
    
    cluster_data$silinfo
    
    
    clustval = data.frame(clusteranzahl, silf, parent, parcoef, modparcoef, jaci, ri, rbind(cluster_data$coeff), cluster_data$silinfo$avg.width, rbind(cluster_data$objective), rbind(cluster_data$convergence))
    clustval
    valsum = rbind(valsum, clustval)
    write.csv(clustval, filename_val, fileEncoding = "UTF-8")
    
    #Save Clustering Data
    filename_centers = paste(save_file, "_conv.csv", sep = "")
    write.csv(cluster_data$convergence, filename_centers, fileEncoding = "UTF-8")
    
    filename_v0 = paste(save_file, "_obj.csv", sep = "")
    write.csv(cluster_data$objective, filename_v0, fileEncoding = "UTF-8")
    
    filename_d = paste(save_file, "_sil.csv", sep = "")
    silframe = data.frame(rbind(cluster_data$silinfo$clus.avg.widths), cluster_data$silinfo$avg.width)
    write.csv(silframe, filename_d, fileEncoding = "UTF-8")
    
    
    #  filename_x = paste(save_file, "_x.csv", sep = "")
    #  write.csv(cluster_data$x, filename_x)
    
    #Cluster-Grafik
    pdf(filename_pdf)
    plot(cluster_data$clustering, main=title, xlab="Index", ylab="Cluster", type="p", pch=19, cex=0.1)
    dev.off()
    
    #Cluster-Zuordnung
    frame = data.frame(cluster_data$clustering, cluster_data$membership, data_o[1:nrows, 2:7])
    write.csv(frame, filename_clust, fileEncoding = "UTF-8")
    
    #Cluster-GrÃ¶Ãen
    # write.csv(cluster_data$csize, filename_info)
    
    
    
    print(save_filename)
    
    
    
  }
  work_load[n,]
  valsum
  write.table(rbind(work_load[n,]), file = "D:/MEGAsync/BArbeit/Data/cluster_results/done_fanny.csv", sep = ",", append = TRUE, quote = FALSE,
              col.names = FALSE, row.names = FALSE)
  cstart = cmin * step_size
  cend = cmax * step_size
  filename_valsum = paste(save_file, "_valsum", cstart,"-", cend, ".csv", sep = "")
  write.csv(valsum, filename_valsum, fileEncoding = "UTF-8")
  
}

