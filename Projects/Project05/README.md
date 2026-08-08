# Project 5: Building a Reproducible GPU Workflow Simulation and Analysis for Particle Physics

This project uses [sim2spec](https://github.com/madantimalsina/sim2spec), a lightweight HPC workflow wrapper around the DUNE `larnd-sim` GPU detector simulation.

## Getting started

Clone the repository into your scratch space on Perlmutter:

```bash
export MYWORKDIR=$PSCRATCH/HPC_intro
mkdir -p "$MYWORKDIR"
cd "$MYWORKDIR"

git clone https://github.com/madantimalsina/sim2spec.git
cd sim2spec
```

For full setup instructions, daily exercise guides, and workflow details, see the [sim2spec README](https://github.com/madantimalsina/sim2spec#readme).
