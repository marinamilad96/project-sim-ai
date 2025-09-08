if (!require("ape")) install.packages("ape")
if (!require("treestats")) install.packages("treestats")
if (!require("tibble")) install.packages("tibble")
if (!require("yaml")) install.packages("yaml")

library(treestats)
library(ape)
library(tibble)
library(yaml)

config <- yaml::read_yaml("/scratch/miladm/git/AI-models/RF/RF-measles-simulation/scripts/tutorials/config.yaml")
config$Directory <- lapply(config$Directory, function(x) {
  gsub("^\\$SLURM_TMPDIR", Sys.getenv("SLURM_TMPDIR"), x)
})
# Define the path to the tree file and ensure the tree file exists, If it is not phylo format, you will need to convert it first to calculate statistics.
tree_files <- list.files(config$Directory$Input_Tree_Folder, pattern = "\\.full\\.trees$", full.names = TRUE) # Extract only full trees (pattern = "\\.full\\.trees$")

print(tree_files)

# Ensure there are tree files in the directory
if (length(tree_files) == 0) {
  stop("\n", "No tree files found in the specified directory.", "\n")
}

# Initialize a list to store stats
all_results <- list()

# Loop over each tree file
for (file in tree_files) {
  # Read the tree
  tree <- read.nexus(file)
  print(paste("Processing file in the loop step 1:", file))
  print(class(tree))       # should be "Phylo"
  # Calculate stats
  all_stats <- calc_all_stats(tree)
  print(paste("Processing file in the loop step 2:", file))
  # Convert to data frame with one column
  stats_df <- data.frame(all_stats)
  print(paste("Processing file in the loop step 3:", file))
  
  # Use the file name as the column name
  colname <- basename(file)
  colnames(stats_df) <- colname
  print(paste("Processing file in the loop step 4:", file))
  # Store in the list
  all_results[[colname]] <- stats_df
  print(paste("Processing file in the loop step 5:", file))
}

# Combine all results side by side (columns)
final_df <- do.call(cbind, all_results)

# Optional: add a column for the statistic names
final_df$parameter <- rownames(final_df)     # Copy old row names into a column
rownames(final_df) <- NULL               # Remove old row names
final_df <- final_df[, c("parameter", setdiff(names(final_df), "parameter"))]

print(final_df)

# Save the dataframe to CSV
write.csv(final_df, file = config$Directory$Output_Tree_File, row.names = TRUE)

# Confirmation message
cat("\n", "Stats dataframe saved to:", config$Directory$Output_Tree_File, "\n")