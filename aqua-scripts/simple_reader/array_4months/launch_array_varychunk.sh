#!/bin/bash
#SBATCH --partition=small
#SBATCH --job-name=data-access
#SBATCH --output=data-access_%j.out
#SBATCH --error=data-access_%j.err
#SBATCH --account=project_462000911
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=64
#SBATCH --time=08:00:00
#SBATCH --mem=128G
#SBATCH --array=0-7

set -euo pipefail

# Set here the list of nproc and chunking values to test
nproc_list=(32 64)
chunking_list=(h 3h 6h D)

# Total combinations
total_nproc=${#nproc_list[@]}
total_chunking=${#chunking_list[@]}

# Compute indices
index=$SLURM_ARRAY_TASK_ID
nproc_index=$(( index % total_nproc ))
chunking_index=$(( index / total_nproc ))

nproc=${nproc_list[$nproc_index]}
chunking=${chunking_list[$chunking_index]}

# Deduced by the SLURM environment variables
mem_mb=${SLURM_MEM_PER_NODE}
mem_gb=$((mem_mb / 1024))

var=2t
catalog=data-access
model=IFS-FESOM
exp=story-2017-historical-HPC
source=hourly-hpz9-atm2d
freq=monthly
regrid=r100
repetitions=3
startdate=20180101T0000
enddate=20180430T2300

python ../reader_monthly_test.py --var $var --catalog $catalog --model $model \
    --exp $exp --source $source --freq $freq --regrid $regrid --nproc $nproc \
    --mem_gb $mem_gb --chunking $chunking --repetitions $repetitions \
    --startdate $startdate --enddate $enddate