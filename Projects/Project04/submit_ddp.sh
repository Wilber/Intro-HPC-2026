#!/bin/bash
#SBATCH --job-name=chem-ddp
#SBATCH -t 00:10:00
#SBATCH -q regular
#SBATCH --output=logs/ddp_%j.out
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --gpus-per-task=4
#SBATCH --cpus-per-task=128

# setup environ,ent
mkdir -p logs

module load conda
conda activate [YOUR ENVIRONMENT HERE]

# Count the GPUs SLURM actually gave us, so one script serves the
# whole scaling study (1, 2, 4 GPUs).
N_GPUS=$(python -c "import torch; print(torch.cuda.device_count())")
echo "Launching DDP on ${N_GPUS} GPU(s)"

# torchrun spawns one Python process per GPU and sets RANK / LOCAL_RANK /
# WORLD_SIZE for each.
# The below options should work for both single- and multi-node training.

export MASTER_ADDR=$(scontrol show hostnames $SLURM_JOB_NODELIST | head -n 1)
export MASTER_PORT=29500

srun torchrun 
    --nnodes="$SLURM_JOB_NUM_NODES" \
    --nproc_per_node=${N_GPUS} \
    --rdzv-backend=c10d \
    --rdzv-id="SLURM_JOB_ID" \
    --rdzv-endpoint="${MASTER_ADDR}:${MASTER_PORT}" \
    train_ddp.py \
        --epochs 50 \
        --batch-size 1024
