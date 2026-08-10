#!/bin/bash
#SBATCH -N 1
#SBATCH -C cpu
#SBATCH --time=00:05:00
#SBATCH -q shared
#SBATCH -A m4388
#SBATCH --reservation=bootcamp_day1

echo "Hello, world!"