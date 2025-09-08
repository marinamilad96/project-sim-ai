library(treestats)
library(ape)
library(tibble)
library(yaml)

tmpdir <- Sys.getenv("TMPDIR")

# Print it to check
print(tmpdir)

config <- yaml::read_yaml("/home/miladm/scratch/git/TreeStatistics-/scripts/config.yaml")

# expand $TMPDIR (and other env vars if any)
# Get the TMPDIR environment variable



config$Directory$Input_Tree_Folder <- gsub(
  "\\$TMPDIR", Sys.getenv("TMPDIR"), config$Directory$Input_Tree_Folder
)

print(config$Directory$Input_Tree_Folder)

# Define the path to the tree file and ensure the tree file exists, If it is not phylo format, you will need to convert it first to calculate statistics.
tree_files <- list.files(config$Directory$Input_Tree_Folder, pattern = ".trees$", full.names = TRUE) # Extract only full trees (pattern = "\\.full\\.trees$")

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
  
  # Calculate stats
  all_stats <- calc_all_stats(tree)
  
  # Convert to data frame with one column
  stats_df <- data.frame(all_stats)
  
  # Use the file name as the column name
  colname <- basename(file)
  colnames(stats_df) <- colname
  
  # Store in the list
  all_results[[colname]] <- stats_df
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