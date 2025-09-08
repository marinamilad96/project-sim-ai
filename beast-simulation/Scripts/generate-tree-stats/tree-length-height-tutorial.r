library(ape)

tree <- rtree(5)  # simulate a random tree with 5 tips
plot(tree)

# Tree height (max root-to-tip distance)
height <- max(node.depth.edgelength(tree))

# Tree length (sum of branch lengths)
length <- sum(tree$edge.length)

cat("Tree height:", height, "\n")
cat("Tree length:", length, "\n")
