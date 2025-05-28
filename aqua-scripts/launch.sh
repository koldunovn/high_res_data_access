#!/bin/bash
#SBATCH --partition=small
#SBATCH --job-name=data-access
#SBATCH --output=data-access_%j.out
#SBATCH --error=data-access_%j.err
#SBATCH --account=project_462000911
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=12
#SBATCH --time=02:00:00
#SBATCH --mem=200G
set -e

var=2t
catalog=climatedt-phase1
model=IFS-FESOM
exps=(story-2017-historical-bridge story-2017-historical-HPC story-2017-historical-stac)
source=hourly-hpz9-atm2d
freq=monthly
regrid=r100
outdir=/scratch/project_462000911/mnurisso/data-access
tmpdir=/scratch/project_462000911/mnurisso/lra_tmp

for exp in "${exps[@]}"; do
    echo "Processing experiment: $exp"
    python lra_prec_italy.py --var $var --catalog $catalog --model $model --exp $exp --source $source --freq $freq --regrid $regrid
done