#!/bin/bash

#BSUB -J task8
#BSUB -q c02613
#BSUB -n 4
#BSUB -R "span[hosts=1]"
#BSUB -W 1

# Output files
#BSUB -o task8.out
#BSUB -e task8.err

# Memory requirements
#BSUB -R "rusage[mem=1GB]"
#BSUB -gpu"num=1:mode=exclusive_process"

# Same CPU model for fair timings
#BSUB -R "select[model == XeonGold6226R]"

source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613_2026

python Task_8.py 100