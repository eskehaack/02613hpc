#!/bin/bash
#BSUB -J jacobi_profile
#BSUB -q hpc

#BSUB -n 8
#BSUB -R "span[hosts=1]"
#BSUB -W 01:00

#BSUB -o jacobi_profile.out
#BSUB -e jacobi_profile.err

#BSUB -R "rusage[mem=16GB]"
#BSUB -M 16GB

#BSUB -R "select[model == XeonGold6226R]"

source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613_2026

# Run for a small subset of floorplans {10, 20, 40} to compare performance with reference solution, measure and print runtime and memory usage.
python -m kernprof -l -v Task_9.py 10

