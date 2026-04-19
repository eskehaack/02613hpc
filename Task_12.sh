#!/bin/bash

#BSUB -J task12
#BSUB -q gpua100
#BSUB -n 4
#BSUB -R "span[hosts=1]"
#BSUB -W 02:00
#BSUB -u s214725@student.dtu.dk

# Output files
#BSUB -o task12.out
#BSUB -e task12.err

# Memory requirements
#BSUB -R "rusage[mem=4GB]"
#BSUB -gpu"num=1:mode=exclusive_process"

# Same CPU model for fair timings
#BSUB -R "select[model == XeonGold6326]"

source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613_2026

pyhton Task_12.py 4571
