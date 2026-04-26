#!/bin/bash

#BSUB -J stats_final
#BSUB -q c02613
#BSUB -n 4
#BSUB -R "span[hosts=1]"
#BSUB -W 00:05

# Output files
#BSUB -o stats_final.out
#BSUB -e stats_final.err

# Memory requirements
#BSUB -R "rusage[mem=4GB]"
#BSUB -gpu"num=1:mode=exclusive_process"

# Same CPU model for fair timings
#BSUB -R "select[model == XeonGold6326]"

source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613_2026

python Task_12_stats.py

