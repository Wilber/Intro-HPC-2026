#!/bin/bash
# Runs train_model.py across multiple nodes/GPUs in ONE job using srun

#SBATCH -A xxxx 		#change to your project number on NERSC                  
#SBATCH -C gpu	
#SBATCH -q regular                # debug while testing
#SBATCH -N 4			  # start with less nodes when testing, Perlmutter nodes have 4 GPUs per node
#SBATCH --gpus-per-node=4
#SBATCH --ntasks-per-node=4       # one task per GPU
#SBATCH --gpus-per-task=1         # each task is bound to exactly 1 physical GPU
#SBATCH -c 32			  # 64 physical cores, 128 with hyperthreading, divide by 4 to get cpus per task
#SBATCH -t 00:10:00               # time in HH:MM:SS 
#SBATCH -J train-model-parallel
#SBATCH -o train_model_%j.out
#SBATCH -e train_model_%j.err

module load python                 # TODO: match your usual module load
conda activate buildingsEnv      # TODO: your conda env name

export REPO_PATH=""
export BUILDINGS_BENCH=""
export TRANSFORM_PATH=""

# One srun launches all 16 tasks (4 nodes x 4 tasks/node) at once. Slurm sets
# SLURM_PROCID (0-15, this task's global rank) and SLURM_NTASKS (16) for each
# task automatically -- train_model.py reads those directly, so no wrapper
# script or manual rank math is needed here.
srun python Train-Model-EP.py --task both
