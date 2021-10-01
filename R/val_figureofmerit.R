# https://rdrr.io/github/ramhiser/clusteval/src/R/figure-of-merit.r

fcm_wrapper <- function(x, K, st, iter) {
   fcm(x = x, centers = K, nstart = st, iter.max = iter)$u
}

figure_of_merit <- function(x, K, st, iter, cluster_method, adjusted = TRUE) {
  x <- as.matrix(x)
  K <- as.integer(K)
  cluster_method <- match.fun(cluster_method)
  
  N <- nrow(x)
  fom_scores <- numeric(N)
  
  for (i in seq_len(N)) {
    labels <- cluster_method(x[-i, ], K = K, st, iter)
    distances <- tapply(seq_along(labels), labels, function(cluster_idx) {
      x_cluster <- x[-i, ][cluster_idx, ]
      if (is.vector(x_cluster)) {
        x_cluster <- matrix(x_cluster, nrow = 1)
      }
      dist2xbar <- as.matrix(dist(rbind(x_cluster, colMeans(x_cluster))))
      sum(tail(dist2xbar, n = 1)^2)
    })
    fom_scores[i] <- sqrt(sum(distances) / N)
  }
  aggregate_fom <- sum(fom_scores)
  if (adjusted) {
    aggregate_fom <- sqrt(N / (N - K)) * aggregate_fom
  }
  obj <- list(
    scores = fom_scores,
    aggregate = aggregate_fom
  )
  class(obj) <- "figure_of_merit"
  obj
}


x <- t_scaled
fom_out <- figure_of_merit(x = x, K=2, 2, 2, cluster_method = "fcm_wrapper")
fom_out2 <- figure_of_merit(x = x, K=3, 2, 2, cluster_method = "fcm_wrapper")
