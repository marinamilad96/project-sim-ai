library(yaml)
library(ape)

#config <- yaml::read_yaml("/Users/MiladM-Dev/Documents/1PhD/project-1-N450/AI-Model/TreeStats/scripts/config.yaml")
tree_folder = "git_trial/init-simulations-densitree/trial1/SEIDp-S10k-inf0.0001"
tree_files <- list.files(tree_folder, pattern = ".full.trees$", full.names = TRUE) # Extract only full trees (pattern = "\\.full\\.trees$")
print(tree_files)

for (file in tree_files) {
  # Read the tree
  tree <- read.nexus(file)
  print(class(tree))
  tree_clean <- collapse.singles(tree)
  # Save the cleaned tree
  output_file <- sub(".trees$", "_collapsed.trees", file)
  write.tree(tree_clean, output_file) 
}
print(paste("All trees processed and saved in", output_file))