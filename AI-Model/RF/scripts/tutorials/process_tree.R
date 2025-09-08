library(treestats)
library(ape)
library(tibble)
library(yaml)

args <- commandArgs(trailingOnly=TRUE)

if (length(args) < 2) {
  stop("Usage: Rscript process_tree.R <input_tree_file> <output_csv>")
}

input_file <- args[1]
output_file <- args[2]

cat("Processing file:", input_file, "\n")

tree <- read.nexus(input_file)
all_stats <- calc_all_stats(tree)
stats_df <- data.frame(all_stats)

# Add parameter column
stats_df$parameter <- rownames(stats_df)
rownames(stats_df) <- NULL

# Reorder columns so parameter is first
stats_df <- stats_df[, c("parameter", setdiff(names(stats_df), "parameter"))]

write.csv(stats_df, output_file, row.names = FALSE)
cat("Saved stats to:", output_file, "\n")
