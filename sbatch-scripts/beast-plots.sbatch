#!/bin/bash
#SBATCH --job-name=beast_analysis    # Job name
#SBATCH --output=/home/miladm/scratch/project-sim-ai/beast-simulation/logs/beast-plot-%j.out   # Standard output log
#SBATCH --error=/home/miladm/scratch/project-sim-ai/beast-simulation/logs/beast-plot-%j.err    # Error log
#SBATCH --time=08:00:00              # Max runtime hh:mm:ss
#SBATCH --cpus-per-task=4            # Number of CPU cores
#SBATCH --mem=32G                     # Memory per node

hpc-ticket
hpc-mount wissdaten

#Conda environment
source $(conda info --base)/etc/profile.d/conda.sh 
conda activate /home/miladm/scratch/.conda/envs/beast

# Run BEAST
#python3 /home/miladm/scratch/project-sim-ai/beast-simulation/Scripts/run_all.py
Rscript /home/miladm/scratch/project-sim-ai/beast-simulation/Scripts/generate-tree-stats/tree-length-height-folder-treefile.r
python3 /home/miladm/scratch/project-sim-ai/beast-simulation/Scripts/generate-plots/box-h-l-df-plot.py

hpc-umount wissdaten