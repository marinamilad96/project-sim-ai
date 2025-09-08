#!/bin/bash
#SBATCH --job-name=tree_stats_array
#SBATCH --output=logs/tree_stats_%A_%a.out
#SBATCH --error=logs/tree_stats_%A_%a.err
#SBATCH --time=01:00:00
#SBATCH --mem=4G
#SBATCH --cpus-per-task=1


hpc-ticket
hpc-mount wissdaten

# Base input/output directories
INPUT_DIR="$SLURM_TMPDIR/wissdaten/ZKI-PH2_Data/MiladM/trees"
OUTPUT_DIR="$SLURM_TMPDIR/wissdaten/ZKI-PH2_Data/MiladM/trees"
#ls $SLURM_TMPDIR/wissdaten/ZKI-PH2_Data/MiladM

mkdir -p logs

# Get all matching files into an array
mapfile -t FILES < <(find "$INPUT_DIR" -maxdepth 1 -name "*.full.trees" -print | sort)

# Pick the file for this array task
FILE="${FILES[$SLURM_ARRAY_TASK_ID-1]}"

# Construct output file name from that file's basename
BASENAME=$(basename "$FILE"*.full.trees)
OUTPUT_FILE="${OUTPUT_DIR}/${BASENAME}_stats.csv"

echo "Running task $SLURM_ARRAY_TASK_ID on file $FILE"

R --vanilla /home/miladm/scratch/git/AI-models/RF/RF-measles-simulation/scripts/tutorials/process_tree.R "$FILE" "$OUTPUT_FILE"

# Print confirmation after Rscript finishes
echo "[$(date)] Finished processing $FILE"
echo "[$(date)] Stats saved to $OUTPUT_FILE"

hpc-umount wissdaten
