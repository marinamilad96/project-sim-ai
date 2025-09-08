library(treestats)
library(ape)

focal_tree <- rphylo(n = 10, birth = 1, death = 0)
colless_stat <- colless(focal_tree)
print(colless_stat)

all_stats <- calc_all_stats(focal_tree)
print(all_stats)

plot(focal_tree, main = "My Simulated Tree")
