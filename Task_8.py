from os.path import join
import sys

import numpy as np
import time
from numba import cuda


def load_data(load_dir, bid):
    SIZE = 512
    u = np.zeros((SIZE + 2, SIZE + 2))
    u[1:-1, 1:-1] = np.load(join(load_dir, f"{bid}_domain.npy"))
    interior_mask = np.load(join(load_dir, f"{bid}_interior.npy"))
    return u, interior_mask

@cuda.jit(device=True)
def jacobi_kernel(interior_mask, u, u_new):
    # single iteration of jacobi method, to be called from GPU
    i = cuda.grid(1)
    if i < len(interior_mask):
        idx = interior_mask[i]
        u_new[idx] = 0.25 * (u[idx[0], idx[1] - 1] + u[idx[0], idx[1] + 1] + u[idx[0] - 1, idx[1]] + u[idx[0] + 1, idx[1]])
        u[idx] = u_new[idx]
    return u



def jacobi_cuda(u, interior_mask, max_iter):
    u = np.copy(u)

    for i in range(max_iter):
        u_new = np.copy(u)
        jacobi_kernel[1, len(interior_mask)](interior_mask, u, u_new)

    return u


def summary_stats(u, interior_mask):
    u_interior = u[1:-1, 1:-1][interior_mask]
    mean_temp = u_interior.mean()
    std_temp = u_interior.std()
    pct_above_18 = np.sum(u_interior > 18) / u_interior.size * 100
    pct_below_15 = np.sum(u_interior < 15) / u_interior.size * 100
    return {
        'mean_temp': mean_temp,
        'std_temp': std_temp,
        'pct_above_18': pct_above_18,
        'pct_below_15': pct_below_15,
    }


if __name__ == '__main__':
    # Load data
    LOAD_DIR = '/dtu/projects/02613_2025/data/modified_swiss_dwellings/'
    with open(join(LOAD_DIR, 'building_ids.txt'), 'r') as f:
        building_ids = f.read().splitlines()

    if len(sys.argv) < 2:
        N = 1
    else:
        N = int(sys.argv[1])
    building_ids = building_ids[:N]

    start_time = time.perf_counter()

    # Load floor plans
    all_u0 = np.empty((N, 514, 514))
    all_interior_mask = np.empty((N, 512, 512), dtype='bool')
    for i, bid in enumerate(building_ids):
        u0, interior_mask = load_data(LOAD_DIR, bid)
        all_u0[i] = u0
        all_interior_mask[i] = interior_mask

    # Run jacobi iterations for each floor plan
    MAX_ITER = 20_000
    ABS_TOL = 1e-4

    all_u = np.empty_like(all_u0)
    for i, (u0, interior_mask) in enumerate(zip(all_u0, all_interior_mask)):
        u = jacobi_cuda(u0, interior_mask, MAX_ITER, ABS_TOL)
        all_u[i] = u

    end_time = time.perf_counter()
    elapsed = end_time - start_time

    # Print summary statistics in CSV format
    stat_keys = ['mean_temp', 'std_temp', 'pct_above_18', 'pct_below_15']
    print('building_id, ' + ', '.join(stat_keys))  # CSV header
    for bid, u, interior_mask in zip(building_ids, all_u, all_interior_mask):
        stats = summary_stats(u, interior_mask)
        print(f"{bid},", ", ".join(str(stats[k]) for k in stat_keys))

    # Save timing results (append to file)
    timing_file = f"timing_jitcuda.csv"

    with open(timing_file, "w") as f:
        f.write("N,elapsed_seconds\n")
        f.write(f"{N},{elapsed:.4f}\n")
    print(f"Saved timing to {timing_file}")