#!/bin/bash
#SBATCH --job-name=treestat
#SBATCH --output=logs/slurm-%j.out
#SBATCH --error=logs/slurm-%j.err
#SBATCH --time=02:00:00          # Adjust runtime
#SBATCH --cpus-per-task=2        # Number of CPU cores
#SBATCH --mem=16G                 # Memory per node

hpc-ticket
hpc-mount wissdaten

mkdir -p logs

echo "Running task $SLURM_ARRAY_TASK_ID on file $FILE"

Rscript /home/miladm/scratch/git/AI-models/RF/RF-measles-simulation/scripts/tutorials/treestat-folder-treefile-df.r

hpc-umount wissdaten