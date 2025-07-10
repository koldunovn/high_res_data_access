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

    # Update the 'Memory (GB)' column to include units for legend clarity
    df_norm = df_norm.copy()
    df_norm['Memory Label'] = df_norm['Memory (GB)'].astype(str) + ' GB'

    sns.lineplot(
        data=df_norm,
        x='Workers',
        y='Normalized Speedup',
        hue='Memory Label',
        marker='o',
        palette='viridis',
        linewidth=2,
        legend='auto'
    )

    # Perfect scaling line (linear with Workers)
    workers_sorted = sorted(df_norm['Workers'].unique())
    plt.plot(workers_sorted, np.array(workers_sorted)/workers_sorted[0],
             linestyle='--', color='gray', label='Perfect Scaling')

    if logx:
        plt.xscale('log')
    if logy:
        plt.yscale('log')

    if title:
        plt.title(title, fontsize=18)
    else:
        plt.title("Normalized Execution Scaling", fontsize=18)
    plt.xlabel('Number of Workers', fontsize=14)
    plt.ylabel('Normalized Speedup (relative to lowest worker count)', fontsize=14)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.legend(fontsize=12)
    plt.tight_layout()
    plt.show()