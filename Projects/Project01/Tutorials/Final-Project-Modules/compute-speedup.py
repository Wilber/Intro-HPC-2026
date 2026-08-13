"""
compute_speedup.py

Reads the timing/<run_tag>/task_*.json files written by train_model.py and
reports wall-clock makespan for one or more runs, without touching sacct.

Usage:
    python compute_speedup.py timing/serial
    python compute_speedup.py timing/serial timing/parallel16
        -> also prints the speedup ratio between the two.
"""
import argparse
import glob
import json
import os
import sys


def load_records(run_dir):
    """Load all task_*.json timing records written for one run."""
    files = sorted(glob.glob(os.path.join(run_dir, "task_*.json")))
    if not files:
        sys.exit(f"No task_*.json files found in {run_dir}")
    records = []
    for f in files:
        with open(f) as fh:
            records.append(json.load(fh))
    return records


def summarize(run_dir):
    """
    Compute the true wall-clock makespan for a run: from the earliest task
    start to the latest task end, across all (possibly concurrent) workers.
    Also reports the fastest/slowest individual task, which highlights
    load imbalance across combos.
    """
    records = load_records(run_dir)
    start = min(r["start"] for r in records)
    end = max(r["end"] for r in records)
    makespan = end - start
    durations = [(r["task_id"], r["duration"]) for r in records]
    fastest = min(durations, key=lambda x: x[1])
    slowest = max(durations, key=lambda x: x[1])

    print(f"\n=== {run_dir} ===")
    print(f"  tasks found:      {len(records)}")
    print(f"  makespan:         {makespan:.2f}s")
    print(f"  fastest task:     task {fastest[0]} ({fastest[1]:.2f}s)")
    print(f"  slowest task:     task {slowest[0]} ({slowest[1]:.2f}s)")
    return makespan


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_dirs", nargs="+",
                         help="One or more timing/<run_tag> directories to summarize.")
    args = parser.parse_args()

    makespans = [(d, summarize(d)) for d in args.run_dirs]

    if len(makespans) == 2:
        (name_a, t_a), (name_b, t_b) = makespans
        faster, slower = (name_a, name_b) if t_a < t_b else (name_b, name_a)
        speedup = max(t_a, t_b) / min(t_a, t_b)
        print(f"\nSpeedup: {faster} was {speedup:.2f}x faster than {slower}")


if __name__ == "__main__":
    main()