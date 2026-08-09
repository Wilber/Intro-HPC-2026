"""
Distributed (multi-GPU) training of the chemistry surrogate with PyTorch DDP.

Launch with torchrun (see submit_ddp.slurm), never with plain `python`:

    torchrun --nproc_per_node=4 train_ddp.py --epochs 50

Every DDP-specific line is marked with  # DDP.
Appends one summary line per run to scaling_results.csv for nb3 analysis.
"""

import argparse
import csv
import os
import time

import h5py
import numpy as np
import torch
import torch.distributed as dist                              # DDP
import torch.nn as nn
from torch.nn.parallel import DistributedDataParallel as DDP  # DDP
from torch.utils.data import TensorDataset, DataLoader
from torch.utils.data.distributed import DistributedSampler   # DDP


class ResidualBlock(nn.Module):
    def __init__(self, hidden):
        super().__init__()
        self.f = nn.Sequential(nn.Linear(hidden, hidden), nn.GELU(),
                               nn.Linear(hidden, hidden))
        self.act = nn.GELU()

    def forward(self, x):
        return self.act(x + self.f(x))


class ResidualMLP(nn.Module):
    def __init__(self, n_in=6, n_out=4, hidden=256, n_blocks=3):
        super().__init__()
        self.inp = nn.Linear(n_in, hidden)
        self.blocks = nn.Sequential(*[ResidualBlock(hidden)
                                      for _ in range(n_blocks)])
        self.out = nn.Linear(hidden, n_out)

    def forward(self, x):
        return self.out(self.blocks(nn.functional.gelu(self.inp(x))))

class GPUTimer:

    def __init__(self, reporting: bool, region_name: str):
        self.reporting = reporting
        self.region_name = region_name
        self.start_event = torch.cuda.Event(enable_timing=True)
        self.end_event = torch.cuda.Event(enable_timing=True)

    def __enter__(self):
        self.start_event.record()

    def __exit__(self, *args, **kwargs):
        self.end_event.record()
        torch.cuda.synchronize()
        if self.reporting:
            self.report()
        
    def report(self):
        print(f'[{self.region_name}] took {self.elapsed_time():0.3f}s')
        
    def elapsed_time(self) -> float:
        # CUDA events record elapsed time in milliseconds
        return self.start_event.elapsed_time(self.end_event) / 1.0e3


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default="surrogate_training_data.h5")
    parser.add_argument("--epochs", type=int, default=50)
    parser.add_argument("--batch-size", type=int, default=1024,
                        help="per-GPU batch size")
    parser.add_argument("--lr", type=float, default=1e-3)
    parser.add_argument("--hidden", type=int, default=256)
    parser.add_argument("--n-blocks", type=int, default=3)
    parser.add_argument("--amp", action="store_true",
                        help="use mixed-precision training")
    args = parser.parse_args()

    # torchrun sets RANK, LOCAL_RANK, WORLD_SIZE for every process.   # DDP
    dist.init_process_group(backend="nccl")                          # DDP
    rank = dist.get_rank()                                           # DDP
    local_rank = int(os.environ["LOCAL_RANK"])                       # DDP
    world_size = dist.get_world_size()                               # DDP
    torch.cuda.set_device(local_rank)                                # DDP
    device = torch.device(f"cuda:{local_rank}")

    if rank == 0:
        print(f"DDP training on {world_size} GPU(s), "
              f"per-GPU batch {args.batch_size}, AMP={args.amp}")

    # ---- Data (same preprocessing as nb2) ----
    with h5py.File(args.data, "r") as f:
        X_train, Y_train = f["X_train"][:], f["Y_train"][:]

    CONT, IN_STATE = [0, 1, 5], [0, 2, 3, 4]
    dY_train = Y_train - X_train[:, IN_STATE]      # delta targets first
    x_mean = X_train[:, CONT].mean(axis=0)         # then scale inputs
    x_std = X_train[:, CONT].std(axis=0)
    X_train[:, CONT] = (X_train[:, CONT] - x_mean) / x_std

    dataset = TensorDataset(torch.tensor(X_train, dtype=torch.float32),
                            torch.tensor(dY_train, dtype=torch.float32))
    # The sampler gives each rank a disjoint shard of every epoch.     # DDP
    sampler = DistributedSampler(dataset)                             # DDP
    loader = DataLoader(dataset, batch_size=args.batch_size,
                        sampler=sampler, num_workers=2, pin_memory=True)

    # ---- Model: identical on every rank, wrapped so gradients        # DDP
    # are all-reduced (averaged) across ranks each backward pass.      # DDP
    torch.manual_seed(42)  # same init on every rank
    model = ResidualMLP(hidden=args.hidden, n_blocks=args.n_blocks).to(device)
    model = DDP(model, device_ids=[local_rank])                       # DDP

    opt = torch.optim.AdamW(model.parameters(), lr=args.lr)
    loss_fn = nn.MSELoss()

    # NOTE: There are a variety of  mixed precision floating point formats,
    # with two being perhaps the most common: float16, and bfloat16.
    # The compromise between the two is the amount of floating point range vs. precision you would like to keep.
    # The number of exponent bits controls the range, while the mantissa (fraction) controls the precision
    # float32: single-precision floating point. 1 bit for sign, 8 bits for exponent, 23 bits for mantissa
    # float16: 1 bit for sign, 5 bits for exponent, 10 bits for mantissa
    # bfloat16: 1 bit for sign, 8 bits for exponent, 7 bits for mantissa

    # When using torch.amp (automated mixed precision), if you are using float16 as the half-precision format,
    # we need to rescale the gradients when leaving the mixed-precision region, due to difference between 
    # the ranges of float16 and float32. With bfloat16, no scaling is necessary.
    # float16 is the default for operations performed on CUDA devices.
    
    scaler = torch.amp.GradScaler(enabled=args.amp)

    # ---- Training loop with throughput measurement ----
    n_samples_total = 0
    torch.cuda.synchronize() # not stricly necessary

    # Switch first argument to rank==0 if not using custom reporting logic at end of script
    timer = GPUTimer(False, 'DDP training loop')
    with timer:
        for epoch in range(args.epochs):
            sampler.set_epoch(epoch)   # reshuffle shards each epoch       # DDP
            model.train()
            epoch_loss = 0.0
            for xb, yb in loader:
                xb = xb.to(device, non_blocking=True)
                yb = yb.to(device, non_blocking=True)
                opt.zero_grad()
                with torch.amp.autocast(device_type="cuda", enabled=args.amp):
                    loss = loss_fn(model(xb), yb)
                scaler.scale(loss).backward()   # all-reduce happens here  # DDP
                scaler.step(opt)
                scaler.update()
                epoch_loss += loss.item()
                n_samples_total += xb.shape[0] * world_size
            if rank == 0 and (epoch + 1) % 10 == 0:
                print(f"  epoch {epoch+1:3d}/{args.epochs}  "
                      f"loss {epoch_loss/len(loader):.5f}")

    elapsed = timer.elapsed_time()
    throughput = n_samples_total / elapsed

    # ---- Only rank 0 writes results and the checkpoint ----          # DDP
    if rank == 0:
        print(f"Done: {elapsed:.1f}s, {throughput:,.0f} samples/s "
              f"on {world_size} GPU(s)")
        torch.save(model.module.state_dict(), "surrogate_model_ddp.pt")

        header = ["n_gpus", "batch_per_gpu", "hidden", "amp",
                  "wall_s", "samples_per_sec"]
        write_header = not os.path.exists("scaling_results.csv")
        with open("scaling_results.csv", "a", newline="") as f:
            w = csv.writer(f)
            if write_header:
                w.writerow(header)
            w.writerow([world_size, args.batch_size, args.hidden,
                        int(args.amp), f"{elapsed:.2f}",
                        f"{throughput:.0f}"])

    dist.destroy_process_group()                                      # DDP


if __name__ == "__main__":
    main()
