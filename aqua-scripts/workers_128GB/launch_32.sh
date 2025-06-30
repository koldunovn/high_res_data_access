#!/bin/bash
#SBATCH --partition=small
#SBATCH --job-name=data-access_32
#SBATCH --output=data-access_32_%j.out
#SBATCH --error=data-access_32_%j.err
#SBATCH --account=project_462000911
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=32
#SBATCH --time=08:00:00
#SBATCH --mem=128G
set -e

nproc=32
var=2t
catalog=data-access
model=IFS-FESOM
exp=story-2017-historical-HPC
source=hourly-hpz9-atm2d
freq=monthly
regrid=r100
outdir=/scratch/project_462000911/mnurisso/data-access-workers/${nproc}_128GB
mkdir -p $outdir
tmpdir=/scratch/project_462000911/mnurisso/lra_tmp

python lra-cli.py --var $var --catalog $catalog --model $model --exp $exp --source $source --freq $freq --regrid $regrid --outdir $outdir --tmpdir $tmpdir --nproc $nproc