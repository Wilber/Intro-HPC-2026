
# Run the Monte Carlo π (MPI) Notebook on **Perlmutter** @ NERSC

This README shows how to run the provided Jupyter notebook **NERSC_mpi_pi_Notebook-5.ipynb** on Perlmutter, and how to execute the MPI portion on compute nodes using Slurm.  This notebook demonstrates how to estimate π (pi) using the Monte Carlo "dart-throwing" method, 
and how to parallelize the computation using MPI (`mpi4py`) in a High-Performance Computing (HPC) environment.

## Overview

The Monte Carlo method approximates π by randomly generating points in a square and counting how many fall inside a quarter circle.
The ratio of points inside the quarter circle to the total number of points approaches π/4 as the number of points increases.

### Learning Goals

- Understand the Monte Carlo method for estimating π.
- Learn basic MPI concepts: **rank**, **size**, and **reduce** operations.
- See how to run Python MPI programs in an HPC environment using Slurm.


---

## 0) Prerequisites

- Active NERSC account and an active allocation (`-A <account>`).
- Familiarity with Perlmutter queues: `debug` (short) or `regular`.
- The notebook: `NERSC_mpi_pi_Notebook-5.ipynb` is in your working directory on Perlmutter.

---



##  Interactive: run the notebook in **NERSC Jupyter**

The most convenient way to explore the notebook is through NERSC Jupyter:
1. Launch **NERSC Jupyter** and choose a **Perlmutter CPU** environment.
2. In a terminal **inside Jupyter**, activate your venv:
   ```bash
   source $SCRATCH/pm-pi-venv/bin/activate
   module load PrgEnv-gnu cray-mpich
   ```
3. Open `NERSC_mpi_pi_Notebook-5.ipynb` and run cells normally.
   - The serial (non-MPI) cells will run immediately.
   - For the MPI example, prefer Section **2B**/**3** below to execute via `srun` on a compute node.

> Note: Jupyter kernels run as a single process; true multi-rank MPI execution should be launched with `srun` (below).


##  Run on Perlmutter with Slurm

### A) **Interactive** test (CPU)

```bash
# Request an interactive node (CPU)
salloc -N 1 -n 8 -C cpu -q debug -t 00:10:00 -A <account>


# 8 MPI ranks example
srun python pi_mpi.py
```

### B) **Batch** job (CPU)

Create `run_pi.slurm`:
```bash
#!/bin/bash
#SBATCH -J mpi-pi
#SBATCH -A <account>
#SBATCH -C cpu
#SBATCH -q debug
#SBATCH -N 1
#SBATCH -t 00:05:00
#SBATCH -o pi-%j.out

module load PrgEnv-gnu python cray-mpich

srun python pi_mpi.py
```

Submit:
```bash
sbatch run_pi.slurm
```

> For longer runs, change `-q debug` to `-q regular` and adjust `-t` appropriately.

---


## Notes for GPU queues (optional)

This π example is CPU-oriented. If adapting for GPU nodes:
- Use `-C gpu` and set proper GPU modules/containers. MPI pattern is unchanged.
- Python+MPI on GPU is typically for orchestrating GPU work per rank (not needed for this simple CPU Monte Carlo demo).

---

**License**: Educational material for an Intro to HPC Bootcamp.
