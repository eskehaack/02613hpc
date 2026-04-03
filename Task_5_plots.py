import glob
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# find all timing files
files = sorted(glob.glob("timing_*.csv"))

data = []
for file in files:
    df = pd.read_csv(file)
    data.append(df)

df = pd.concat(data, ignore_index=True)

# if multiple rows exist per worker, average them
df = (
    df.groupby("workers", as_index=False)["elapsed_seconds"]
    .mean()
    .sort_values("workers")
)

# compute speed-up relative to 1 worker
t1 = df.loc[df["workers"] == 1, "elapsed_seconds"].iloc[0]
df["speedup"] = t1 / df["elapsed_seconds"]

print(df)

# --- plotting ---
fig, ax = plt.subplots(figsize=(7.2, 4.6))

# main curve
ax.plot(
    df["workers"],
    df["speedup"],
    marker="o",
    linewidth=2,
    markersize=6
)

# labels and title
ax.set_title("Parallel speed-up for static scheduling", pad=12)
ax.set_xlabel("Number of workers")
ax.set_ylabel("Speed-up")

# cleaner axes
ax.set_xticks(df["workers"])
ax.set_xlim(df["workers"].min(), df["workers"].max())
ax.set_ylim(0, int(np.ceil(df["speedup"].max())))

# light grid
ax.grid(True, linestyle="--", alpha=0.4)

# remove top/right spines for cleaner look
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

# optional point labels
for x, y in zip(df["workers"], df["speedup"]):
    ax.annotate(f"{y:.2f}", (x, y), textcoords="offset points", xytext=(0, 7), ha="center", fontsize=9)

fig.tight_layout()

plt.savefig("speedup_static.png", dpi=300, bbox_inches="tight")
plt.show()