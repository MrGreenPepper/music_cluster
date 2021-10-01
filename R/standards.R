

library(mclust)
library(class)
library(cluster)




rm(list = ls())


music_try <- read.csv2("D:/MEGASync/BArbeit/R/data/12_2.csv", header=T)

set.seed(20)
mscaled <- scale(music_try[(1:370) , (2:187)])

mkmeans <- kmeans(mscaled[(1:370),], 100, nstart = 1000)

mkmeans$cluster
plot(mkmeans$cluster)





set.seed(20)
mclara <- clara(mscaled[(1:370),], 20)
plot(mclara$clustering)

plot(mclara) #interessant!!!!


mclara$cluster

mtest = data.frame(mkmeans$cluster, mclara$cluster, music_try[(1:370),1:1])  
mtest
