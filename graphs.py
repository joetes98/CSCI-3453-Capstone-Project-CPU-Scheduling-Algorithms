import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import StandardScaler

print("1: Single Image \n2: Multiple Images\n3: Radar Chart")
choice = int(input("Enter your choice: "))

if choice == 1:
    data = {
    "Algorithm": ["MLFQ", "MLQ", "EDF", "RMS"],
    "Average Turnaround Time": [27.86, 30.72, 11.13, 44.70],
    "Average Waiting Time": [22.72, 25.12, 8.14, 28.40],
    "Average Throughput": [0.20, 0.1755, 0.34, 0.46],
    "Average CPU Utilization (%)": [99.57, 94.27, 98.17, 90.36]
}
    df = pd.DataFrame(data)

    fig, axs = plt.subplots(2, 2, figsize=(12, 8))
    fig.suptitle("CPU Scheduling Algorithm Comparison", fontsize=16)

    metrics = df.columns[1:]
    colors = ["skyblue", "salmon", "lightgreen", "orange"]
    axes = axs.flatten()

    for i, metric in enumerate(metrics):
        ax = axes[i]
        bars = ax.bar(df["Algorithm"], df[metric], color=colors)
        ax.set_title(metric)
        ax.set_ylabel(metric)
        ax.set_xlabel("Algorithm")
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        
        for bar in bars:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, yval + yval*0.01, f'{yval:.2f}', 
                    ha='center', va='bottom', fontsize=9)

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig("scheduling_comparison.png")  # Saves the file in your current working directory
    plt.show()

elif choice == 2:

    data = {
        "Algorithm": ["MLFQ", "MLQ", "EDF", "RMS"],
        "Average Turnaround Time": [27.86, 30.72, 11.13, 44.70],
        "Average Waiting Time": [22.72, 25.12, 8.14, 28.40],
        "Average Throughput": [0.20, 0.1755, 0.34, 0.46],
        "Average CPU Utilization (%)": [99.57, 94.27, 98.17, 90.36]
    }

    df = pd.DataFrame(data)

    # Plot each metric in a separate figure
    for metric in df.columns[1:]:
        plt.figure(figsize=(6, 4))
        bars = plt.bar(df["Algorithm"], df[metric], color=["skyblue", "salmon", "lightgreen", "orange"])
        plt.title(metric)
        plt.ylabel(metric)
        plt.xlabel("Algorithm")
        plt.grid(axis='y', linestyle='--', alpha=0.7)

        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2, yval + yval*0.01, f'{yval:.2f}', 
                    ha='center', va='bottom', fontsize=9)

        plt.tight_layout()
        plt.show()
    
elif choice == 3:
    # Input data
    data = {
    "Algorithm": ["MLFQ", "MLQ", "EDF", "RMS"],
    "Average Turnaround Time": [27.86, 30.72, 11.13, 44.70],
    "Average Waiting Time": [22.72, 25.12, 8.14, 28.40],
    "Average Throughput": [0.20, 0.1755, 0.34, 0.46],
    "Average CPU Utilization (%)": [99.57, 94.27, 98.17, 90.36]
}
    df = pd.DataFrame(data)

    df_norm = df.copy()
    df_norm["Average Turnaround Time"] = 1 / df["Average Turnaround Time"]
    df_norm["Average Waiting Time"] = 1 / df["Average Waiting Time"]
    df_norm["Average Throughput"] = df["Average Throughput"]
    df_norm["Average CPU Utilization (%)"] = df["Average CPU Utilization (%)"] / 100

    # Z score normalization
    scaler = StandardScaler()
    scaled_values = scaler.fit_transform(df_norm.iloc[:, 1:])
    df_scaled = pd.DataFrame(scaled_values, columns=df_norm.columns[1:])
    df_scaled.insert(0, "Algorithm", df["Algorithm"])

    # Radar chart setup
    categories = list(df_scaled.columns[1:])
    num_vars = len(categories)
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]

    # Create chart
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    for i, row in df_scaled.iterrows():
        values = row[categories].tolist()
        values += values[:1]
        ax.plot(angles, values, label=row["Algorithm"], linewidth=2)
        ax.fill(angles, values, alpha=0.1)

    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_thetagrids(np.degrees(angles[:-1]), categories)
    plt.title("Scheduling Algorithm Comparison (Z-score Normalized)", size=14, y=1.08)
    plt.legend(loc='upper right', bbox_to_anchor=(1.2, 1.1))
    plt.tight_layout()

    # Show or save the plot
    plt.savefig("scheduling_radar_zscore_chart.png")
    plt.show()