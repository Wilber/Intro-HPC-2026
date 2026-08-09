#!/bin/bash

## We can't build the container locally with shifter/docker - this requires admin privileges, but if we were able to,
## the command would look equivalent to the podman version

# docker build -t intro-to-hpc:latest -f Containerfile .