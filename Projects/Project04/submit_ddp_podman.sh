#!/bin/bash
#SBATCH -t 00:10:00
#SBATCH -q regular
#SBATCH -C gpu
#SBATCH --ntasks-per-node=1
#SBATCH --gpus-per-task=4
#SBATCH --cpus-per-task=128

# setup torchrun env
mkdir -p logs

export MASTER_ADDR=$(scontrol show hostnames $SLURM_JOB_NODELIST | head -n 1)
export MASTER_PORT=29500

srun podman-hpc run \
    --gpu --nccl-cu13 --rm --net=host --ipc=host \
    -v .:/workspace \
    nersc/pytorch:26.01.01 \
    torchrun \
    --nnodes="$SLURM_JOB_NUM_NODES" \
    --nproc-per-node=4 \
    --rdzv-backend=c10d \
    --rdzv-id="$SLURM_JOB_ID" \
    --rdzv-endpoint="${MASTER_ADDR}:${MASTER_PORT}" \
    train_ddp.py \
        --epochs 50 \
        --batch-size 1024
