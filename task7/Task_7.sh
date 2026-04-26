#!/bin/bash

#BSUB -J task7_40
#BSUB -q hpc
#BSUB -n 4
#BSUB -R "span[hosts=1]"
#BSUB -W 00:10

# Output files
#BSUB -o task7.out
#BSUB -e task7.err

# Memory requirements
#BSUB -R "rusage[mem=1GB]"
#BSUB -M 1GB


source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613_2026

python Task_7.py 40
