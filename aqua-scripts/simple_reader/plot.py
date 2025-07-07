import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


def plot_normalized_scaling(df_all, which_time='Total Time (s)',
                            logx=False, logy=False, title=None):
    """Plot normalized scaling curves from all result files."""

    # Group and compute average per (Workers, Memory)
    df_avg = (
        df_all.groupby(['Workers', 'Memory (GB)', 'Variable'])[which_time]
        .mean()
        .reset_index(name='Mean Time')
    )

    # Normalize execution times per memory level
    normalized_dfs = []
    for mem, group in df_avg.groupby('Memory (GB)'):
        baseline_time = group.sort_values('Workers').iloc[0]['Mean Time']
        group = group.copy()
        group['Normalized Speedup'] = baseline_time / group['Mean Time']
        normalized_dfs.append(group)

    df_norm = pd.concat(normalized_dfs, ignore_index=True)

    # Plot
    plt.figure(figsize=(10, 6))
    sns.set_theme(style='whitegrid')

    sns.lineplot(data=df_norm, x='Workers', y='Normalized Speedup',# hue='Memory (GB)',
                 marker='o', palette='viridis', linewidth=2)

    # Perfect scaling line (linear with Workers)
    workers_sorted = sorted(df_norm['Workers'].unique())
    plt.plot(workers_sorted, np.array(workers_sorted)/workers_sorted[0],
             linestyle='--', color='gray', label='Perfect Scaling')

    if logx:
        plt.xscale('log')
    if logy:
        plt.yscale('log')

    if title:
        plt.title(title)
    else:
        plt.title("Normalized Execution Scaling")
    plt.xlabel('Number of Workers')
    plt.ylabel('Normalized Speedup (relative to lowest worker count)')
    plt.legend()
    plt.tight_layout()
    plt.show()