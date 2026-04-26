#!/bin/bash
#BSUB -J CuPy_profile_modified
#BSUB -q c02613
#BSUB -n 4
#BSUB -R "span[hosts=1]"
#BSUB -W 00:30
#BSUB -o CuPy_profile_modified.out
#BSUB -e CuPy_profile_modified.err
#BSUB -R "rusage[mem=1GB]"
#BSUB -M 1GB
#BSUB -gpu "num=1:mode=exclusive_process"

source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613_2026

module purge
module load cuda

echo "=== profiling ==="
nsys profile -f true -o cupy_profile_modified python Task_10.py 1

echo "=== stats ==="
nsys stats cupy_profile_modified.nsys-rep
