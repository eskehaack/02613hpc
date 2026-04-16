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


@cuda.jit()
def jacobi_kernel(interior_mask, u, u_new):
    # single iteration of jacobi method, to be called from GPU
    i, j = cuda.grid(2)
    ui, uj = i + 1, j + 1
    if i < interior_mask.shape[0] and j < interior_mask.shape[1]:
        if interior_mask[i, j]:
            u_new[ui, uj] = 0.25 * (
                u[ui, uj - 1] + u[ui, uj + 1] + u[ui - 1, uj] + u[ui + 1, uj]
            )


def jacobi_cuda(u, interior_mask, max_iter):
    u = np.copy(u)
    du = cuda.to_device(u)
    du_new = cuda.to_device(u.copy())

    threads_per_block = (16, 16)

    ny, nx = interior_mask.shape
    blocks_per_grid = ((ny + 15) // 16, (nx + 15) // 16)

    for i in range(max_iter):
        du, du_new = du_new, du
        jacobi_kernel[blocks_per_grid, threads_per_block](interior_mask, du, du_new)

    return du.copy_to_host()


def summary_stats(u, interior_mask):
    u_interior = u[1:-1, 1:-1][interior_mask]
    mean_temp = u_interior.mean()
    std_temp = u_interior.std()
    pct_above_18 = np.sum(u_interior > 18) / u_interior.size * 100
    pct_below_15 = np.sum(u_interior < 15) / u_interior.size * 100
    return {
        "mean_temp": mean_temp,
        "std_temp": std_temp,
        "pct_above_18": pct_above_18,
        "pct_below_15": pct_below_15,
    }


if __name__ == "__main__":
    # Load data
    LOAD_DIR = "/dtu/projects/02613_2025/data/modified_swiss_dwellings/"
    with open(join(LOAD_DIR, "building_ids.txt"), "r") as f:
        building_ids = f.read().splitlines()

    if len(sys.argv) < 2:
        N = 1
    else:
        N = int(sys.argv[1])
    building_ids = building_ids[:N]

    start_time = time.perf_counter()

    # Load floor plans
    all_u0 = np.empty((N, 514, 514))
    all_interior_mask = np.empty((N, 512, 512), dtype="bool")
    for i, bid in enumerate(building_ids):
        u0, interior_mask = load_data(LOAD_DIR, bid)
        all_u0[i] = u0
        all_interior_mask[i] = interior_mask

    # Run jacobi iterations for each floor plan
    MAX_ITER = 20_000
    ABS_TOL = 1e-4

    all_u = np.empty_like(all_u0)
    for i, (u0, interior_mask) in enumerate(zip(all_u0, all_interior_mask)):
        u = jacobi_cuda(u0, interior_mask, MAX_ITER)
        all_u[i] = u

    end_time = time.perf_counter()
    elapsed = end_time - start_time

    # Print summary statistics in CSV format
    stat_keys = ["mean_temp", "std_temp", "pct_above_18", "pct_below_15"]
    print("building_id, " + ", ".join(stat_keys))  # CSV header
    for bid, u, interior_mask in zip(building_ids, all_u, all_interior_mask):
        stats = summary_stats(u, interior_mask)
        print(f"{bid},", ", ".join(str(stats[k]) for k in stat_keys))

    # Save timing results (append to file)
    timing_file = "task8_timing.csv"

    with open(timing_file, "a") as f:
        f.write(f"{N},{elapsed:.4f}\n")
    print(f"Saved timing to {timing_file}")
