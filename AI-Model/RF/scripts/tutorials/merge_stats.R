library(dplyr)

# Folder where individual CSV stats files are saved
stats_folder <- "/scratch/miladm/git/AI-models/RF/RF-measles-simulation/results/tree_stats"

# List all CSV files
files <- list.files(stats_folder, pattern = "_stats.csv$", full.names = TRUE)

# Read and join all data frames by "parameter"
dfs <- lapply(files, read.csv)

# Rename value columns to filename
names(dfs) <- basename(files)

# Join all by "parameter"
merged_df <- Reduce(function(x, y) merge(x, y, by = "parameter", all = TRUE), dfs)

# Optionally write to final CSV
write.csv(merged_df, file = "/scratch/miladm/git/AI-models/RF/RF-measles-simulation/results/final_tree_stats.csv", row.names = FALSE)

cat("Final merged stats saved to: /scratch/miladm/git/AI-models/RF/RF-measles-simulation/results/final_tree_stats.csv\n")
