from os.path import join
import sys
import numpy as np
import time
from multiprocessing import Pool


def load_data(load_dir, bid):
    SIZE = 512
    u = np.zeros((SIZE + 2, SIZE + 2))
    u[1:-1, 1:-1] = np.load(join(load_dir, f"{bid}_domain.npy"))
    interior_mask = np.load(join(load_dir, f"{bid}_interior.npy"))
    return u, interior_mask


def jacobi(u, interior_mask, max_iter, atol=1e-6):
    u = np.copy(u)

    for i in range(max_iter):
        # Compute average of left, right, up and down neighbors, see eq. (1)
        u_new = 0.25 * (u[1:-1, :-2] + u[1:-1, 2:] + u[:-2, 1:-1] + u[2:, 1:-1])
        u_new_interior = u_new[interior_mask]
        delta = np.abs(u[1:-1, 1:-1][interior_mask] - u_new_interior).max()
        u[1:-1, 1:-1][interior_mask] = u_new_interior

        if delta < atol:
            break
    return u


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


def process_building(bid):
    u0, interior_mask = load_data(LOAD_DIR, bid)
    u = jacobi(u0, interior_mask, MAX_ITER, ABS_TOL)
    stats = summary_stats(u, interior_mask)
    return {
    "building_id": bid,
    "mean_temp": stats["mean_temp"],
    "std_temp": stats["std_temp"],
    "pct_above_18": stats["pct_above_18"],
    "pct_below_15": stats["pct_below_15"]
}


if __name__ == "__main__":
    # Load data
    LOAD_DIR = '/dtu/projects/02613_2025/data/modified_swiss_dwellings/'
    MAX_ITER = 20000
    ABS_TOL = 1e-4

    with open(join(LOAD_DIR, "building_ids.txt"), "r") as f:
        building_ids = f.read().splitlines()

    if len(sys.argv) < 2:
        N = 1
    else:
        N = int(sys.argv[1])

    if len(sys.argv) < 3:
        n_workers = 1
    else:
        n_workers = int(sys.argv[2])

    building_ids = building_ids[:N]

    start_time = time.perf_counter()

    with Pool(processes=n_workers) as pool:
        results = pool.map(process_building, building_ids, chunksize=5)

    end_time = time.perf_counter()
    elapsed = end_time - start_time

    # Save building statistics
    stat_keys = ["mean_temp", "std_temp", "pct_above_18", "pct_below_15"]
    result_filename = f"results_workers_{n_workers}.csv"

    with open(result_filename, "w") as f:
        f.write("building_id," + ",".join(stat_keys) + "\n")

        for row in results:
            f.write(
                f"{row['building_id']},"
                + ",".join(str(row[k]) for k in stat_keys)
                + "\n"
            )

    print(f"Saved building results to {result_filename}")

    # Save timing results (append to file)
    timing_file = f"timingdyn_{n_workers}.csv"

    with open(timing_file, "w") as f:
        f.write("workers,N,elapsed_seconds\n")
        f.write(f"{n_workers},{N},{elapsed:.6f}\n")

    print(f"Saved timing to {timing_file}")