"""
This file contains functions to benchmark the performance of CDO and smmregrid remap methods.
It splits the weight generation and the remapping, so that the weights can be reused.
It independently times the remapping and the weight generation, and compares the results.
"""
import os
import argparse
import timeit
import xarray as xr
import dask
from cdo import Cdo
from smmregrid import Regridder, cdo_generate_weights
from aqua.util import load_yaml
from aqua.logger import log_configure
from aqua.diagnostics.core import open_cluster, close_cluster

cdo = Cdo()

def parse_args():
    """Parse command line arguments for smmregrid benchmarking."""
    parser = argparse.ArgumentParser(description="Benchmark CDO and smmregrid remap methods.")
    parser.add_argument('--config', '-c', type=str, required=True, help="Path to the configuration file with remapping parameters")
    parser.add_argument('--nworkers', type=int, default=1, help="Number of Dask workers to use")
    parser.add_argument('--loglevel', type=str, default='INFO', help="Logging level")
    return parser.parse_args()

if __name__ == '__main__':
    config_file = parse_args().config
    nworkers = parse_args().nworkers
    loglevel = parse_args().loglevel

    logger = log_configure(log_level=loglevel, log_name='CDO SMMRegrid Benchmark')

    config = load_yaml(config_file)

    if nworkers == 1:
        dask.config.set(scheduler='sinchronous')
    else:
        client, cluster, private_cluster = open_cluster(nworkers=nworkers, cluster=None, loglevel=loglevel)

    grids_dir = config.get('grids_dir')
    grid_name = config.get('grid_name')
    grid_fullpath = os.path.join(grids_dir, grid_name)
    if grid_fullpath and not os.path.exists(grid_fullpath):
        raise FileNotFoundError(f"Grid file {grid_fullpath} does not exist.")
    logger.info(f"Using grid file: {grid_name}")
    
    target_grid = config.get('target_grid_dir')
    target_grid_name = config.get('target_grid_name')
    tfile = os.path.join(grids_dir, target_grid_name)
    if not tfile or not os.path.exists(tfile):
        raise FileNotFoundError(f"Target grid file {tfile} does not exist.")
    logger.info(f"Using target grid file: {target_grid_name}")
    
    methods = config.get('methods', ['nn', 'con', 'bil'])

    data_dir = config.get('data_dir')
    data_name = config.get('data_name')
    data_fullpath = os.path.join(data_dir, data_name) if data_dir and data_name else None

    data = xr.open_mfdataset(data_fullpath, combine='by_coords', parallel=True)
    logger.info(f"Opened dataset: {data_fullpath}")

    if nworkers > 1:
        close_cluster(client, cluster, private_cluster, loglevel=loglevel)