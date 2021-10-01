

library(kohonen)





rm(list = ls())



music_try3 <- read.delim2("D:/MEGASync/BArbeit/R/data/music_try3.csv", header=TRUE)
set.seed(20)
mscaled <- scale(music_try3[ , (3:188)])







som_grid <- somgrid(xdim = 10, ydim = 10)

sommusic <- som(mscaled, rlen = 10000, alpha=c(0.05,0.01))

plot(sommusic$changes)
sommusic$


somk <- kmeans(sommusic$codes, 12)
plot(somk$cluster)


plot(sommusic, type="count")
plot(sommusic, type="changes")
plot(sommusic, type = "property",  property = sommusic$codes[,10], main=names(sommusic$data)[4])



sommusic$data
sommusic$codes
sommusic




mydata <- sommusic$codes 
wss <- (nrow(mydata)-1)*sum(apply(mydata,2,var)) 
for (i in 2:15) {
  wss[i] <- sum(kmeans(mydata, centers=i)$withinss)
}
plot(wss)



