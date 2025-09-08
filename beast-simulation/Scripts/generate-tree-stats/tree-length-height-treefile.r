library(ape)

config <- yaml::read_yaml("/Users/MiladM-Dev/Documents/1PhD/project-1-N450/AI-Model/TreeStats/Tutorials/config.yaml")

# Define the path to the tree file and ensure the tree file exists
# If it is not phylo format, you will need to convert it first to calculate statistics. # 
tree <- read.nexus(file = config$Directory$Input_Tree_File)
print(class(tree))       # should be "Phylo"

# Tree height (max root-to-tip distance)
height <- max(node.depth.edgelength(tree))

# Tree length (sum of branch lengths)
length <- sum(tree$edge.length)

cat("Tree height:", height, "\n")
cat("Tree length:", length, "\n")
