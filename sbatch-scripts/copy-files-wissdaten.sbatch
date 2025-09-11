#!/bin/bash
#SBATCH --job-name=beast_analysis    # Job name
#SBATCH --output=/home/miladm/scratch/project-sim-ai/beast-simulation/logs/copy-files-%j.out   # Standard output log
#SBATCH --error=/home/miladm/scratch/project-sim-ai/beast-simulation/logs/copy-files-%j.err    # Error log
#SBATCH --time=01:00:00              # Max runtime hh:mm:ss
#SBATCH --cpus-per-task=4            # Number of CPU cores
#SBATCH --mem=8G                     # Memory per node

hpc-ticket
hpc-mount wissdaten
# Make sure logs directory exists
mkdir -p logs
source $(conda info --base)/etc/profile.d/conda.sh 
conda activate /home/miladm/scratch/.conda/envs/beast

cd /home/miladm/scratch/project-sim-ai
# Run BEAST
# cp source_file.txt /path/to/destination/
# cp -r my_folder/ /path/to/destination/

cp -r ./Data/* $TMPDIR/wissdaten/ZKI-PH2_Data/MiladM/trees/Data/

hpc-umount wissdaten