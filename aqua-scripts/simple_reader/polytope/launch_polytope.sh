#!/bin/bash
#SBATCH --partition=small
#SBATCH --job-name=data-access
#SBATCH --output=data-access_%j.out
#SBATCH --error=data-access_%j.err
#SBATCH --account=project_462000911
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=8
#SBATCH --time=08:00:00
#SBATCH --mem=128G

set -euo pipefail

nproc=8
chunking=D

# Deduced by the SLURM environment variables
mem_mb=${SLURM_MEM_PER_NODE}
mem_gb=$((mem_mb / 1024))

var=2t
catalog=data-access
model=IFS-FESOM
exp=story-2017-historical-bridge
source=hourly-hpz9-atm2d
freq=monthly
regrid=r100
engine=polytope

python ../reader_monthly_test.py --var $var --catalog $catalog --model $model \
    --exp $exp --source $source --freq $freq --regrid $regrid --nproc $nproc \
    --mem_gb $mem_gb --chunking $chunking --engine $engine