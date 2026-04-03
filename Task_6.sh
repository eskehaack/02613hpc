#!/bin/bash

#BSUB -J task6_dynamic
#BSUB -q hpc
#BSUB -n 8
#BSUB -R "span[hosts=1]"
#BSUB -W 03:00

# Output files
#BSUB -o task6_dynamic.out
#BSUB -e task6_dynamic.err

# Memory requirements
#BSUB -R "rusage[mem=8GB]"
#BSUB -M 8GB

# Same CPU model for fair timings
#BSUB -R "select[model == XeonGold6226R]"

source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613

# Number of floorplans
N=100

echo "=================================="
echo "Running simulations"
echo "=================================="

for workers in 1 2 4 8
do
    echo "Running N=${N}, workers=${workers}"

    /usr/bin/time -f "mem=%M KB runtime=%e s" \
    python Task_6.py $N $workers 2>&1

    echo ""
done

echo "=================================="
echo "Generating speed-up plot"
echo "=================================="

python Task_6_plots.py

echo "Done"