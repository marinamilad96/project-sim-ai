library(treestats)
library(ape)
library(tibble)
library(yaml)

# Load config
config <- yaml::read_yaml("/scratch/miladm/git/AI-models/RF/RF-measles-simulation/scripts/tutorials/config.yaml")

# Get subfolders inside the parent folder
subfolders <- list.dirs(config$Directory$Input_Parent_Folder, full.names = TRUE, recursive = FALSE)
print(subfolders)

# Initialize list for results
all_results <- list()

# Loop over each subfolder
for (folder in subfolders) {
  cat("\nProcessing folder:", folder, "\n")
  
  tree_files <- list.files(folder, pattern = "\\.full\\.trees$", full.names = TRUE)
  
  # Check if tree files exist in this folder
  if (length(tree_files) == 0) {
    cat("No tree files found in:", folder, "\n")
    next  # Skip this folder
  }
  
  # Loop over tree files in this folder
  for (file in tree_files) {
    cat("Reading tree file:", file, "\n")
    tree <- read.nexus(file)
    
    # Calculate stats
    all_stats <- calc_all_stats(tree)
    
    # Convert to dataframe with one column
    stats_df <- data.frame(all_stats)
    
    # Use file name as the column name
    colname <- basename(file)
    colnames(stats_df) <- colname
    
    # Store results
    all_results[[colname]] <- stats_df
  }
}

# Combine all results into one dataframe
if (length(all_results) > 0) {
  final_df <- do.call(cbind, all_results)
  
  # Add parameter column
  final_df$parameter <- rownames(final_df)
  rownames(final_df) <- NULL
  final_df <- final_df[, c("parameter", setdiff(names(final_df), "parameter"))]
  
  print(final_df)
  
  # Save
  write.csv(final_df, file = config$Directory$Output_Tree_File, row.names = FALSE)
  cat("\nStats dataframe saved to:", config$Directory$Output_Tree_File, "\n")
} else {
  stop("No tree stats generated. Check if there are any .trees files in subfolders.")
}
