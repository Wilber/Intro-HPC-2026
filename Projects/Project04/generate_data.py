"""
Generate training data for the chemistry-step surrogate.

Each sample is one call to the stiff ODE solver:
    input  : (log10 T, log10 n_H, x_HII, x_HeII, x_HeIII, log10 dt)
    output : (log10 T', x_HII', x_HeII', x_HeIII')   -- state after dt

This is embarrassingly parallel: every sample is independent. On a cluster,
run many copies of this script as a SLURM job array, each writing its own
chunk file. Merge the chunks afterwards with merge_chunks.py.

Usage (laptop test):
    python generate_data.py --n-samples 2000 --chunk-id 0 --out-dir chunks

Usage (SLURM array, see submit_datagen_tasks.slurm):
    srun python generate_data.py --n-samples 25000 --out-dir chunks
"""

import argparse
import os
import time

import h5py
import numpy as np

import hhe_chemistry as chem

# Sampling ranges. dt spans ~10 kyr to ~1 Gyr so the surrogate sees both
# "nothing happens" and "cools to the floor" regimes.
LOG_T_RANGE = (4.0, 8.0)
LOG_N_RANGE = (-4.0, 0.0)
LOG_DT_RANGE = (11.5, 16.5)  # seconds


def sample_initial_state(rng, sample_nonlinear=False):
    """
    Draw one random off-equilibrium initial state.

    Half the samples start near CIE (perturbed equilibrium), half are fully
    random. This concentrates training data near the physically visited
    manifold while still covering the full state space.
    """
    log_T = rng.uniform(*LOG_T_RANGE)
    log_n = rng.uniform(*LOG_N_RANGE)
    T = 10.0**log_T
    n_H = 10.0**log_n

    if rng.random() < 0.2:
        # Perturbed CIE state
        y_eq = chem.equilibrium_state(T, n_H)
        x_HII = np.clip(y_eq[0] + rng.normal(0, 0.1), 0.0, 1.0)
        x_HeII = np.clip(y_eq[1] + rng.normal(0, 0.1), 0.0, 1.0)
        x_HeIII = np.clip(y_eq[2] + rng.normal(0, 0.1), 0.0, 1.0 - x_HeII)
    else:
        # Fully random ionization state
        x_HII = rng.random()
        x_HeII = rng.random()
        x_HeIII = rng.uniform(0.0, 1.0 - x_HeII)

    # If you want to test the surrogate on a more nonlinear sample,
    # then set sample_nonlinear to True
    if sample_nonlinear is False:
        log_dt = rng.uniform(*LOG_DT_RANGE)
    else:
        #  This calculates a timestep based on individual cells rather than globally
        y_now = [x_HII, x_HeII, x_HeIII, T]
        state = np.abs(np.array(y_now))
        rates = np.abs(
            np.asarray(chem.rhs(0.0, y_now, n_H))
        )  # [dx_HII, dx_HeII, dx_HeIII, dT]

        # Per-component timescale |value| / |rate|; the fastest-moving component
        # sets when the state visibly changes. Skip components that aren't moving.
        with np.errstate(divide="ignore", invalid="ignore"):
            tscales = state / rates
        tscales = tscales[np.isfinite(tscales) & (tscales > 0.0)]
        if tscales.size == 0:
            # cell is at equilibrium so take a long dt
            log_dt = rng.uniform(*LOG_DT_RANGE)
        else:
            t_local = tscales.min()
            dt = t_local * 10.0 ** rng.uniform(-1.5, 1.5)
            # Keep dt in a physically sane band (reuse the global range as limits).
            dt = float(np.clip(dt, 10.0 ** LOG_DT_RANGE[0], 10.0 ** LOG_DT_RANGE[1]))
            log_dt = np.log10(dt)

    return log_T, log_n, x_HII, x_HeII, x_HeIII, log_dt


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n-samples", type=int, default=1000)
    parser.add_argument("--chunk-id", type=int, default=0)
    parser.add_argument("--out-dir", type=str, default="chunks")
    parser.add_argument("--seed-base", type=int, default=2026)
    parser.add_argument("--sample-nonlinear", type=int, default=0)
    args = parser.parse_args()

    # Use the process ID, if submitted via srun.
    # Otherwise, rely on the chunk_id input
    chunk_id = int(os.environ.get("SLURM_PROCID", args.chunk_id))

    os.makedirs(args.out_dir, exist_ok=True)
    # Different seed per chunk so array tasks don't duplicate samples
    rng = np.random.default_rng(args.seed_base + chunk_id)

    X = np.empty((args.n_samples, 6))
    Y = np.empty((args.n_samples, 4))
    n_failed = 0

    t_start = time.time()
    for i in range(args.n_samples):
        log_T, log_n, x_HII, x_HeII, x_HeIII, log_dt = sample_initial_state(
            rng, bool(args.sample_nonlinear)
        )
        y0 = [x_HII, x_HeII, x_HeIII, 10.0**log_T]
        try:
            y1, _ = chem.integrate_cell(y0, 10.0**log_n, 10.0**log_dt)
        except RuntimeError:
            n_failed += 1
            continue
        X[i] = [log_T, log_n, x_HII, x_HeII, x_HeIII, log_dt]
        Y[i] = [np.log10(y1[3]), y1[0], y1[1], y1[2]]

        if (i + 1) % 500 == 0:
            rate = (i + 1) / (time.time() - t_start)
            print(
                f"  chunk {chunk_id}: {i + 1}/{args.n_samples} ({rate:.0f} samples/s)",
                flush=True,
            )

    out_file = os.path.join(args.out_dir, f"chunk_{chunk_id:04d}.h5")
    with h5py.File(out_file, "w") as f:
        f.create_dataset("X", data=X)
        f.create_dataset("Y", data=Y)
        f.attrs["features"] = [
            "log10_T",
            "log10_n_H",
            "x_HII",
            "x_HeII",
            "x_HeIII",
            "log10_dt",
        ]
        f.attrs["targets"] = ["log10_T_new", "x_HII_new", "x_HeII_new", "x_HeIII_new"]
        f.attrs["n_failed"] = n_failed

    elapsed = time.time() - t_start
    print(
        f"chunk {chunk_id}: wrote {out_file} "
        f"({args.n_samples} samples, {n_failed} failed, {elapsed:.0f}s)"
    )


if __name__ == "__main__":
    main()
