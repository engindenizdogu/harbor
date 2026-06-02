---
title: Slurm
tags:
  - hpc
  - scheduling
  - slurm
  - infrastructure
draft: false
---

Slurm is an open-source, highly scalable cluster management and job scheduling system for Linux clusters. It provides three key functions:
1. Allocating exclusive and/or non-exclusive access to resources (compute nodes) for tasks for a set amount of time.
2. Providing a framework for starting, executing, and monitoring work on the set of allocated nodes.
3. Arbitrating contention for resources by managing a queue of pending work.

## References & Documentation

- **sbatch**: Command to submit a batch script to Slurm. It processes `#SBATCH` directives to request specific resources (like CPUs, GPUs, memory, and time limits). 
  - *Source: [sbatch Documentation](https://slurm.schedmd.com/sbatch.html)*
- **Command Summary**: A cheat sheet covering the core Slurm commands (`sbatch`, `srun`, `salloc`, `squeue`, etc.) and their most common parameters. 
  - *Source: [Slurm Summary PDF](https://slurm.schedmd.com/pdfs/summary.pdf)*
