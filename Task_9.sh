#!/bin/bash

#BSUB -J CuPy_solution
#BSUB -q c02613

#BSUB -n 4
#BSUB -R "span[hosts=1]"
#BSUB -W 00:30

#BSUB -o CuPy_solution.out
#BSUB -e CuPy_solution.err

#BSUB -R "rusage[mem=1GB]"
#BSUB -M 1GB

#BSUB -R "select[model == XeonGold6226R]"

#BSUB -gpu "num=1:mode=exclusive_process"

source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613_2026

# Run for a small subset of floorplans and time the execution
for n in 10 20 40
do
    echo "======================================"
    echo "Running with n_floorplans = $n"
    echo "======================================"

    /usr/bin/time -v python -m kernprof -l -v Task_9.py $n
done
