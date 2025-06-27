#!/bin/bash
#SBATCH --partition=small
#SBATCH --job-name=data-access
#SBATCH --output=data-access_%j.out
#SBATCH --error=data-access_%j.err
#SBATCH --account=project_462000911
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=12
#SBATCH --time=08:00:00
#SBATCH --mem=64G
set -e

var=2t
catalog=data-access
model=IFS-FESOM
exps=(story-2017-historical-bridge story-2017-historical-HPC story-2017-historical-stac)
source=hourly-hpz9-atm2d
freq=monthly
regrid=r100
outdir=/scratch/project_462000911/mnurisso/data-access
tmpdir=/scratch/project_462000911/mnurisso/lra_tmp

for exp in "${exps[@]}"; do
    echo "Processing experiment: $exp"
    python lra-cli.py --var $var --catalog $catalog --model $model --exp $exp --source $source --freq $freq --regrid $regrid --outdir $outdir --tmpdir $tmpdir
    echo "Completed processing for experiment: $exp"
    echo "----------------------------------------"
done