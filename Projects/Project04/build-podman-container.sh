#!/bin/bash
# Build the container
podman-hpc build -t intro-to-hpc:latest -f Containerfile .

# The container should be available to use, but only on the node from which you built the container
# Migrating the container will make it available on all nodes
podman-hpc migrate intro-to-hpc:latest
