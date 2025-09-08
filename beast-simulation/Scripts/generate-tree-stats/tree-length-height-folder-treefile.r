library(ape)
library(tidyr)
library(yaml)


config <- yaml::read_yaml("/Users/MiladM-Dev/Documents/1PhD/project-sim-ai/config-files/config.yaml")

config$Directory$Input_Tree_Folder <- gsub(
  "\\$TMPDIR", Sys.getenv("TMPDIR"), config$Directory$Input_Tree_Folder
)
#print(config$Directory$Input_Tree_Folder)
config$Directory$Output_Tree_File <- gsub(
  "\\$TMPDIR", Sys.getenv("TMPDIR"), config$Directory$Output_Tree_File
)
#print(config$Directory$Output_Tree_File)

# Define the path to the tree file and ensure the tree file exists, If it is not phylo format, you will need to convert it first to calculate statistics.
tree_files <- list.files(config$Directory$Input_Tree_Folder, pattern = ".trees$", full.names = TRUE) # Extract only full trees (pattern = "\\.full\\.trees$")

# Ensure there are tree files in the directory
if (length(tree_files) == 0) {
  stop("\n", "No tree files found in the specified directory.", "\n")
}

# Initialize a list to store stats
all_results_height <- list()
all_results_length <- list()

# Loop over each tree file
for (file in tree_files) {

    # Read the tree
    tree <- read.nexus(file)
    print("Done reading tree:")
    
    # Calculate Tree height and length
    height <- max(node.depth.edgelength(tree))
    length <- sum(tree$edge.length)
    print(paste("Height:", height, "Length:", length))

    # Convert to data frame with one column
    height_df <- data.frame(height)
    length_df <- data.frame(length)
    print("Done creating data frames:")
    # Use the file name as the column name
    colname <- basename(file)
    colnames(height_df) <- colname
    colnames(length_df) <- colname
    
    # Store in the list
    all_results_height[[colname]] <- height_df
    all_results_length[[colname]] <- length_df
    print("Done storing results.")
}


# Combine all results side by side (columns)
final_df_height <- do.call(cbind, all_results_height)
final_df_length <- do.call(cbind, all_results_length)

# Optional: add a column for the statistic names
rownames(final_df_height) <- "tree_height"              # Remove old row names
rownames(final_df_length) <- "tree_length"               # Remove old row names
final_df_height <- final_df_height[, c(setdiff(names(final_df_height), "tree_height"))]
final_df_length <- final_df_length[, c(setdiff(names(final_df_length), "tree_length"))]
final_df <- rbind(final_df_height, final_df_length)

# pivot df
final_df <- as.data.frame(t(final_df))
final_df$file_name <- rownames(final_df)     # Copy old row names into a column
rownames(final_df) <- NULL  # Remove old row names
final_df <- final_df[, c("file_name", setdiff(names(final_df), "file_name"))]  # Move file_name to the first column
print(final_df)

# Save the dataframe to CSV
write.csv(final_df, file = config$Directory$Output_Tree_File, row.names = TRUE)

# Confirmation message
cat("\n", "Stats dataframe saved to:", config$Directory$Output_Tree_File, "\n")