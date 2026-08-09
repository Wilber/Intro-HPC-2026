#!/bin/bash
#SBATCH --job-name=chem-datagen
#SBATCH --output=logs/datagen_%A_%a.out
#SBATCH --array=0-39            # 40 independent tasks
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=2G
#SBATCH --time=01:00:00
# NOTE: update --partition/--account for perlmutter @snigs

# Each array task generates one independent chunk of training data.
# 40 tasks x 25,000 samples = 1,000,000 samples total.
# super parallel:
# no communication between tasks, each writes its own file.

mkdir -p logs chunks

module load conda
conda activate [YOUR ENVIRONMENT HERE]

python generate_data.py \
    --n-samples 25000 \
    --chunk-id ${SLURM_ARRAY_TASK_ID} \
    --out-dir chunks \
    --sample-nonlinear 0
    
# To generate a more difficult dataset by sampling more nonlinear initial conditions, set --sample-nonlinear to 1

# After all array tasks finish, merge on the login node or via a
# dependent job:  sbatch --dependency=afterok:<jobid> submit_merge.slurm
# or simply:      python merge_chunks.py --chunk-dir chunks
