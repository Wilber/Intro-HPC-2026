#!/bin/bash
#SBATCH --job-name=chem-datagen
#SBATCH --output=logs/datagen_%A_%a.out
#SBATCH --ntasks-per-node=40
#SBATCH --cpus-per-task=2
#SBATCH -C cpu
#SBATCH --time=01:00:00

# This achieves the same work as the job array, but packs all of the work into a single job,
# rather than an array of many jobs. On Perlmutter, there is a limit to how many Slurm jobs can 
# actively age (i.e., advance in the job queue) per user. For tasks which require only a small 
# number of cores, it can be better sometimes to pack all of the work into a single job rather
# than spread out the work amongst many tasks. 
# (On some systems, Slurm can assign jobs to arbitirarily small fractions of a node's resources,
#  but this is not the case on Perlmutter. You must request at least half a node, via the shared
#  queue, or a number of whole nodes. On Perlmutter, then, packing jobs helps save on node hours!)

mkdir -p logs chunks

module load conda  # adjust to your cluster's module system
conda activate [YOUR ENVIRONMENT HERE]

# Launch with srun, so that 
srun python generate_data.py \
    --n-samples 25000 \
    --out-dir chunks \
    --sample-nonlinear 0
    
# To generate a more difficult dataset by sampling more nonlinear initial conditions, set --sample-nonlinear to 1

# After the job finishes, merge on the login node or via a
# dependent job:  sbatch --dependency=afterok:<jobid> submit_merge.slurm
# or simply:      python merge_chunks.py --chunk-dir chunks
