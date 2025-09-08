# This script calculates tree statistics using the treestats package in R.
# It reads a tree file, computes various statistics, and saves the results to a CSV file. # : line_length_linter.
if (!require("ape")) install.packages("ape")
if (!require("treestats")) install.packages("treestats")
if (!require("tibble")) install.packages("tibble")
if (!require("yaml")) install.packages("yaml")


library(treestats)
library(ape)
library(tibble)
library(yaml)

#base::Sys.getenv("TMPDIR") # Check if TMPDIR is set, if not, set it to a default value


config <- yaml::read_yaml("/home/miladm/scratch/git/AI-models/RF/RF-measles-simulation/scripts/tutorials/config.yaml")

# Define the path to the tree file and ensure the tree file exists
# If it is not phylo format, you will need to convert it first to calculate statistics. # 
#tree <- read.nexus(file = config$Directory$Input_Tree_File)
scratch_dir <- Sys.getenv("SLURM_TMPDIR")

# Construct full path
tree <- file.path(scratch_dir, "wissdaten/ZKI-PH2_Data/MiladM/trees/SEID-S10k-inf0.0001-1754903740968.full.trees")

print(class(tree))       # should be "Phylo"

# Calculate all statistics for the tree, check treestats documentation for specifc statistics # 
all_stats <- calc_all_stats(tree)
print(all_stats)


# Convert results to a data frame to make it easier to manipulate and save
stats_df <- data.frame(all_stats)

# Change the index is needed as the row names (parameters) are printed as Index
stats_df$Index <- rownames(stats_df)                                            # Copy old row names into a column
rownames(stats_df) <- NULL                                                      # Remove old row names
stats_df <- stats_df[, c("Index", setdiff(names(stats_df), "Index"))]           # Reorder columns to have Index first
colnames(stats_df) <- c("parameter", "value")                                   # Rename columns for clarity
print(stats_df)                                                                 # Print the data frame to check the results

# Save the dataframe to CSV
write.csv(stats_df, file = config$Directory$Output_Tree_File, row.names = TRUE)

# Confirmation message
cat("Stats dataframe saved to:", config$Directory$Output_Tree_File, "\n")
