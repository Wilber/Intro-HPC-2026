"""
Merge per-task chunk files into one training dataset with train/test split.

Usage:
    python merge_chunks.py --chunk-dir chunks --out surrogate_training_data.h5
"""

import argparse
import glob
import os

import h5py
import numpy as np


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--chunk-dir", type=str, default="chunks")
    parser.add_argument("--out", type=str, default="surrogate_training_data.h5")
    parser.add_argument("--test-frac", type=float, default=0.2)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    files = sorted(glob.glob(os.path.join(args.chunk_dir, "chunk_*.h5")))
    if not files:
        raise SystemExit(f"No chunk files found in {args.chunk_dir}/")

    X_list, Y_list = [], []
    for fn in files:
        with h5py.File(fn, "r") as f:
            X_list.append(f["X"][:])
            Y_list.append(f["Y"][:])
    X = np.concatenate(X_list)
    Y = np.concatenate(Y_list)
    print(f"Merged {len(files)} chunks -> {X.shape[0]:,} samples")

    # Shuffle and split
    rng = np.random.default_rng(args.seed)
    idx = rng.permutation(X.shape[0])
    n_test = int(args.test_frac * X.shape[0])
    test_idx, train_idx = idx[:n_test], idx[n_test:]

    with h5py.File(args.out, "w") as f:
        f.create_dataset("X_train", data=X[train_idx])
        f.create_dataset("Y_train", data=Y[train_idx])
        f.create_dataset("X_test", data=X[test_idx])
        f.create_dataset("Y_test", data=Y[test_idx])
        f.attrs["features"] = ["log10_T", "log10_n_H", "x_HII", "x_HeII",
                               "x_HeIII", "log10_dt"]
        f.attrs["targets"] = ["log10_T_new", "x_HII_new", "x_HeII_new",
                              "x_HeIII_new"]

    print(f"Wrote {args.out}: {len(train_idx):,} train / {len(test_idx):,} test")


if __name__ == "__main__":
    main()
