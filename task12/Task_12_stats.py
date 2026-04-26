import glob
import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

print("Working directory:", os.getcwd())

# load CSV files
files = sorted(glob.glob("task12_summary_stats_*.csv"))
data = [pd.read_csv(f) for f in files]

# merge
df = pd.concat(data, ignore_index=True)
df.columns = df.columns.str.strip()

# --- histogram ---
fig, ax = plt.subplots(figsize=(7.2, 4.6))

bins = np.linspace(df["mean_temp"].min(), df["mean_temp"].max(), 30)

ax.set_axisbelow(True)

ax.hist(
    df["mean_temp"],
    bins=bins,
    edgecolor="black",
    linewidth=0.8
)

ax.set_title("Distribution of mean building temperatures", pad=12)
ax.set_xlabel("Mean temperature (°C)")
ax.set_ylabel("Number of buildings")

ax.grid(True, linestyle="--", alpha=0.4)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

fig.tight_layout()
fig.savefig("mean_temperature_histogram.png", dpi=300, bbox_inches="tight")
plt.close(fig)

# --- statistics ---
avg_mean_temp = df["mean_temp"].mean()
avg_std_temp = df["std_temp"].mean()
buildings_above_18 = (df["pct_above_18"] >= 50).sum()
buildings_below_15 = (df["pct_below_15"] >= 50).sum()

print(f"Average mean temperature: {avg_mean_temp:.3f}")
print(f"Average temperature standard deviation: {avg_std_temp:.3f}")
print(f"Buildings with ≥50% area above 18°C: {buildings_above_18}")
print(f"Buildings with ≥50% area below 15°C: {buildings_below_15}")