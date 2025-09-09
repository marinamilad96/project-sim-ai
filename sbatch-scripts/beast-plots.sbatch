#!/bin/bash
#SBATCH --job-name=beast_analysis    # Job name
#SBATCH --output=/home/miladm/scratch/project-sim-ai/beast-simulation/logs/box-plot-%j.out   # Standard output log
#SBATCH --error=/home/miladm/scratch/project-sim-ai/beast-simulation/logs/box-plot-%j.err    # Error log
#SBATCH --time=08:00:00              # Max runtime hh:mm:ss
#SBATCH --cpus-per-task=4            # Number of CPU cores
#SBATCH --mem=32G                     # Memory per node

hpc-ticket
hpc-mount wissdaten
# Make sure logs directory exists
mkdir -p logs
source $(conda info --base)/etc/profile.d/conda.sh 
conda activate /home/miladm/scratch/.conda/envs/beast
# Run BEAST
#python3 /home/miladm/scratch/git/measles_simulations/Scripts/run_all.py
#python3 /home/miladm/scratch/project-sim-ai/beast-simulation/Scripts/generate-plots/box-time-df-plot-specification.py
python3 /home/miladm/scratch/project-sim-ai/beast-simulation/Scripts/generate-plots/box-height-length-df-plot.py
hpc-umount wissdaten