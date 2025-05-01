import pandas as pd
import matplotlib.pyplot as plt

data = {
    "Algorithm": ["MLFQ", "MLQ", "EDF"],
    "Average Turnaround Time": [27.96, 30.72, 11.13],
    "Average Waiting Time": [22.39, 25.12, 8.14],
    "Average Throughput": [0.21, 0.1755, 0.34],
    "Average CPU Utilization (%)": [16.67, 94.27, 98.17]
}

df = pd.DataFrame(data)

# Plot each metric in a separate figure
for metric in df.columns[1:]:
    plt.figure(figsize=(6, 4))
    plt.bar(df["Algorithm"], df[metric], color=["skyblue", "salmon", "lightgreen"])
    plt.title(metric)
    plt.ylabel(metric)
    plt.xlabel("Algorithm")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()