#!/bin/bash

#BSUB -J task5_static
#BSUB -q hpc

# Request enough cores for the largest worker count
#BSUB -n 8
#BSUB -R "span[hosts=1]"
#BSUB -W 30:00

# Output files
#BSUB -o task5_static.out
#BSUB -e task5_static.err

# Memory requirements
#BSUB -R "rusage[mem=8GB]"
#BSUB -M 8GB

# Email notification
#BSUB -u s214704@student.dtu.dk
#BSUB -B -N

# Use same CPU type for fair timing
#BSUB -R "select[model == XeonGold6226R]"

source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613

N=100

for workers in 1 2 4 8
do
    echo "=================================="
    echo "Running with N=${N}, workers=${workers}"
    echo "=================================="

    /usr/bin/time -f "mem=%M KB runtime=%e s" \
    python Task_5.py $N $workers 2>&1

    echo ""
done