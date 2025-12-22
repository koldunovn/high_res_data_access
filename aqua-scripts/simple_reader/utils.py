import glob
import re
import pandas as pd


def read_benchmark_file(filepath):
    """
    Read a single AQUA benchmark results file into a DataFrame.

    Args:
        filepath (str): Path to the benchmark results file.

    Returns:
        pd.DataFrame: DataFrame containing the benchmark results.
    """
    with open(filepath, 'r') as f:
        lines = f.readlines()

    header_idx = next(i for i, line in enumerate(lines) if 'Attempt;' in line)
    data_lines = lines[header_idx+1:]

    records = []
    for line in data_lines:
        parts = line.strip().split(';')
        if len(parts) == 5:
            attempt, total, retrieve, compute, io = parts
            records.append({
                'Attempt': int(attempt),
                'Total Time (s)': float(total),
                'Retrieve Time (s)': float(retrieve),
                'Compute Time (s)': float(compute),
                'I/O Time (s)': float(io),
            })

    # Extract metadata from filename
    match = re.search(r'results_(\w+?)_(\d+)workers_(\d+)GB\.txt', filepath)
    match2 = re.search(r'results_(\w+?)_(\d+)workers_(\d+)GB_([6h|3h|D|W|h]+)chunk\.txt', filepath)
    if match:
        varname, nworkers, mem_gb = match.groups()
        for r in records:
            r['Variable'] = varname
            r['Workers'] = int(nworkers)
            r['Memory (GB)'] = int(mem_gb)
    elif match2:
        varname, nworkers, mem_gb, chunk_size = match2.groups()
        for r in records:
            r['Variable'] = varname
            r['Workers'] = int(nworkers)
            r['Memory (GB)'] = int(mem_gb)
            r['Chunk Size'] = str(chunk_size)
    else:
        raise ValueError(f"Filename '{filepath}' does not match expected pattern.")

    return pd.DataFrame(records)


def load_all_benchmarks(path_pattern="results_*.txt"):
    """
    Load all AQUA benchmark results files matching the given pattern into a single DataFrame.

    Args:
        path_pattern (str): Glob pattern to match benchmark result files.

    Returns:
        pd.DataFrame: DataFrame containing all benchmark results.
    """
    files = glob.glob(path_pattern)
    print(f"Found {len(files)} benchmark files matching pattern '{path_pattern}'.")
    if not files:
        raise ValueError(f"No files found matching pattern: {path_pattern}")

    df_list = [read_benchmark_file(f) for f in files]
    return pd.concat(df_list, ignore_index=True)


def chunk_translation(df_chunk):
    """Translate the 'Chunk Size' column in the DataFrame according to predefined mappings."""
    # The 'Chunk Size' column has to be translated according to the following dictionary:
    chunk_translation_dict = {
        'h': 1,
        '3h': 3,
        '6h': 6,
        'D': 24,
        'W': 168
    }
    df_chunk['Chunk Size'] = df_chunk['Chunk Size'].map(chunk_translation_dict)
    return df_chunk


def chunk_translation_reverse(df_chunk):
    """Reverse translate the 'Chunk Size' column in the DataFrame according to predefined mappings."""
    chunk_translation_dict_reverse = {
        1: 'h',
        3: '3h',
        6: '6h',
        24: 'D',
        168: 'W'
    }
    df_chunk['Chunk Size'] = df_chunk['Chunk Size'].map(chunk_translation_dict_reverse)
    return df_chunk
