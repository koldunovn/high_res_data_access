#!/bin/bash
#SBATCH --partition=small
#SBATCH --job-name=regrid-comparison
#SBATCH --output=regrid-comparison_%j.out
#SBATCH --error=regrid-comparison_%j.err
#SBATCH --account=project_462000911
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=64
#SBATCH --time=08:00:00
#SBATCH --mem=128G
#SBATCH --array=0-6

set -euo pipefail

# Set here the list of nproc values to test
nproc_list=(1 2 4 8 16 32 64)
# Total combinations
total_nproc=${#nproc_list[@]}
nproc=${nproc_list[$SLURM_ARRAY_TASK_ID]}

outdir=/scratch/project_462000911/mnurisso/data-access/regrid-catalog
loglevel=DEBUG

python regrid-comparison.py --nproc $nproc \
    --outdir $outdir --loglevel $loglevel