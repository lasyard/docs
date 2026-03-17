#!/bin/bash

## Resource Request
#SBATCH --job-name=Test
#SBATCH --output=Test-%j.out
#SBATCH --ntasks=3
#SBATCH --nodes=3
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=16k

## Job Steps
srun echo "Start Job ${SLURM_JOB_ID}: ${SLURM_JOB_NAME}..."
srun hostname
srun sleep 10
srun echo "End Job"
