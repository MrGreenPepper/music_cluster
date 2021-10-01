rm(list = ls())


library(cluster)


#fulldata_11_4.1 <- read.csv("D:/MEGAsync/BArbeit/Essentia_try/Data/fulldata_11_4-1_sorted_clean_zeroone_90_opt_weighted.csv", header=TRUE)
filename = "~/MEGAsync/BArbeit/Essentia_try/Data/clara/cw_pamframe_" 
clusteranzahl = 10

for(n in 1:20){
  
  clusteranzahl = n * 10
  
  filename = "~/MEGAsync/BArbeit/Essentia_try/Data/clara/cw_claraframe_" 
  
  filename_csv = paste(filename, toString(clusteranzahl), sep = "")
  filename_csv = paste(filename_csv, ".csv", sep = "")
  
  filename_pdf = paste(filename, toString(clusteranzahl), sep = "")
  filename_pdf = paste(filename_pdf, ".pdf", sep = "")

  
  data_m <- read.csv(filename_csv, header=TRUE)

  cluster = data.frame(data_m[, 3], data_m[, 2])

  title = "clara (cw) - "
  title = paste(title, toString(clusteranzahl), sep = "")
  colors <- colors[as.numeric(data_m[, 2])]
  
  pdf(filename_pdf)
  plot(cluster, main=title, xlab="Index", ylab="Cluster", type="p", pch=19, cex=0.1, col=colors()[1:10617])
  dev.off  

}
