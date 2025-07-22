#!/bin/bash
#SBATCH --partition=small
#SBATCH --job-name=data-production
#SBATCH --output=data-production_%j.out
#SBATCH --error=data-production_%j.err
#SBATCH --account=project_462000911
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=16
#SBATCH --time=08:00:00
#SBATCH --mem=128G

set -euo pipefail

nproc=16

var=tprate
catalog=data-access
model=IFS-FESOM
exp=story-2017-historical-HPC
source=hourly-hpz9-atm2d
engine=fdb
startdate=20180101T0000
enddate=20180131T2300
outdir=/scratch/project_462000911/mnurisso/data-access/regrid-catalog
loglevel=DEBUG

python data-production.py --var $var --catalog $catalog --model $model \
    --exp $exp --source $source --nproc $nproc --engine $engine \
    --startdate $startdate --enddate $enddate \
    --outdir $outdir --loglevel $loglevel
