  
fcmpp <- function(starts, imax, fuzziness, t_scaled, algo, cmin, cmax, step_size, dataset){
  
  valsum = data.frame()
  for(n in cmin:cmax) {
    clusteranzahl = ( n * step_size )
    
    algo_name = algo
    #algo_name = paste("kmean", "(i:", toString(iterations), ")", sep = "")
    
    title = paste(algo_name, " (s:", toString(starts), " imax:", toString(imax),"m:", fuzziness, ")",  " - k=", toString(clusteranzahl), sep = "")
   
#filenames 
    #save_filename = paste(algo_name, "(s", toString(starts), "imax", toString(imax), "k", toString(clusteranzahl), "m", toString(fuzziness), ")_", "config(", conf, ")_", sep="")
    save_filename = paste(algo_name, "(s", toString(starts), "imax", toString(imax), "k", toString(clusteranzahl), "m", toString(fuzziness), ")_", sep="")
    save_filename = paste(save_filename, "_data(", dataset, ")", sep = "")
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
    silf <- SIL.F(t_scaled, cluster_data$u, alpha=1)
    
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
    
    
   # jaci <- JACCARD.F(cluster_data$cluster, cluster_data$u)
   # ri <- RI.F(cluster_data$cluster, cluster_data$u)
  #  xb <- XB(t_scaled, cluster_data$u, cluster_data$v, fuzziness)
    
    

    
    clustval = data.frame(clusteranzahl, silf, parent, parcoef, modparcoef, cluster_data$sumsqrs$between.ss, cluster_data$sumsqrs$tot.within.ss)
    valsum = rbind(valsum, clustval)
    write.csv(clustval, filename_val)
    
#Save Clustering Data
    filename_centers = paste(save_file, "_centers.csv", sep = "")
    write.csv(cluster_data$v, filename_centers)
    
    filename_v0 = paste(save_file, "_v0.csv", sep = "")
    write.csv(cluster_data$v0, filename_v0)
    
    filename_d = paste(save_file, "_d.csv", sep = "")
    write.csv(cluster_data$d, filename_d)
    
    filename_x = paste(save_file, "_x.csv", sep = "")
    write.csv(cluster_data$x, filename_x)
    
#Cluster-Grafik
    pdf(filename_pdf)
    plot(cluster_data$cluster, main=title, xlab="Index", ylab="Cluster", type="p", pch=19, cex=0.1)
    dev.off()
    
#Cluster-Zuordnung
    frame = data.frame(cluster_data$cluster, cluster_data$u, data_o[1:nrows, 2:7])
    write.csv(frame, filename_clust)
  
#Cluster-GrÃ¶Ãen
    write.csv(cluster_data$csize, filename_info)
    
    
    
    print(save_filename)
    
    
  }
  valsum
  
  cstart = cmin * step_size
  cend = cmax * step_size
  filename_valsum = paste(save_file, "_valsum", cstart,"-", cend, ".csv", sep = "")
  write.csv(valsum, filename_valsum)
  
  
} 
