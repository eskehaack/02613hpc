import glob
import pandas as pd
import matplotlib.pyplot as plt

# find all timing files
files = sorted(glob.glob("timing_*.csv"))

data = []

for file in files:
    df = pd.read_csv(file)
    data.append(df)

df = pd.concat(data)

# sort by workers
df = df.sort_values("workers")

# compute speed-up
t1 = df[df["workers"] == 1]["elapsed_seconds"].iloc[0]
df["speedup"] = t1 / df["elapsed_seconds"]

print(df)

# plot
plt.figure(figsize=(8,5))

plt.plot(
    df["workers"],
    df["speedup"],
    marker="o",
    label="Measured speed-up"
)


plt.xlabel("Number of workers")
plt.ylabel("Speed-up")
plt.title("Parallel speed-up (static scheduling)")
plt.grid(True)
plt.legend()

plt.savefig("speedup_static.png", dpi=200)
plt.show()