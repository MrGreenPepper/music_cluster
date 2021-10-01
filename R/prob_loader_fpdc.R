install.packages("ppclust")
install.packages("fclust")
install.packages("cluster")
install.packages("factorextra")
install.packages("fpc")
install.packages("NbClust")
install.packages("advclust")
install.packages("clusterCrit")
install.packages("FPDclustering")

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
work_load = rbind(c("fpdc", "special", 2000, 1, 5, 5, 1, 3, 5, "fpdc2"),
                  c("fpdc", "special2", 2000, 1, 5, 5, 1, 3, 5, "fpdc2"),
                 # c("fpdc", "normal", 2000, 0, 10, 10, 5, 5, 1, "fpdc4"),
                 # c("fpdc", "normal", 2000, 0, 10, 10, 5, 5, 1, "fpdc5"),
                  c("fpdc", "special3", 2000, 1, 5, 5, 1, 3, 5, "fpdc2"))
                  # c("fpdc", "timeline", 2000, 0, 5, 5, 1, 3, 5, "fpdc2"))
                 # c("fpdc", "normal", 2000, 0, 5, 5, 5, 5, 1, "fpdc4"),
                #  c("fpdc", "normal", 2000, 0, 5, 5, 5, 5, 1, "fpdc5"))
                #  c("fpdc", "timeline", 2000, 0, 10, 10, 5, 5, 1, "fpdc"))
                #  c("fpdc", "timeline", 5000, 0, 5, 5, 5, 14, 1, "fpdc"))
                 
             #     c("fpdc", "single_string", 2000, 0, 5, 5, 5, 15, 1, "fpdc"),
             #     c("fpdc", "single_tonal", 2000, 0, 5, 5, 5, 15, 1, "fpdc"),
             #     c("fpdc", "single_normal", 2000, 0, 5, 5, 5, 15, 1, "fpdc"),
             #     c("fpdc", "single_string_normal", 2000, 0, 5, 5, 5, 15, 1, "fpdc"),
             #     c("fpdc", "single_string_tonal", 2000, 0, 5, 5, 5, 15, 1, "fpdc"))
             #c("fpdc", "single", 2000, 0, 10, 10, 5, 5, 1, "fpdc"),
             #  c("fpdc", "string", 2000, 0, 10, 10, 5, 5, 1, "fpdc"),
             # c("fpdc", "tonal", 2000, 0, 10, 10, 5, 5, 1, "fpdc"),
             #  

nr = as.numeric(nrow(work_load))

for (n in 1:nr){
  print(n)
  
  algo_name <- work_load[n, 1]
  dataset <- work_load[n, 2]
  split_len = as.numeric(work_load[n, 3])
  split_part = as.numeric(work_load[n, 4])
  
  #  starts  = as.numeric(work_load[n, 5])
  #  imax = as.numeric(work_load[n, 6])
  nf <- as.numeric(work_load[n, 5])
  nu <- as.numeric(work_load[n, 6])
  cstart  =as.numeric(work_load[n, 7])
  cend = as.numeric(work_load[n, 8])
  cstep  = as.numeric(work_load[n, 9])
  altname <- work_load[n, 10]
  split_parts = (origin_rows - (origin_rows %% split_len)) / split_len
  
  dict_s = paste(dict_results, algo_name, "/", sep = "")
  
  data_filename = paste("small(", dataset, ")", origin_dataset, "_split(", split_len, "_", split_part, "-", split_parts ,")", sep = "")
  data_file = paste(dict, data_filename, ".csv", sep = "")
  
  data_o <- read.csv(data_file, header=TRUE, sep = ",")
  nrows = nrow(data_o)
  ncols = ncol(data_o)
  data_s <- data_o[(special_rows:nrows) , (special_columns:ncols)]
  t_scaled <- scale(data_s)
  
  
  cluster_algo <- match.fun(algo_name)
  cluster_algo(t_scaled, altname, nf, nu, cstart, cend, cstep, data_filename)
  
  write.table(rbind(work_load[n,]), file = "D:/MEGAsync/BArbeit/Data/cluster_results/done_fpdc.csv", sep = ",", append = TRUE, quote = FALSE,
              col.names = FALSE, row.names = FALSE)
}

