import argparse
import os
import gc
import time
import xarray as xr
from cdo import Cdo
from smmregrid import Regridder
from aqua import Reader
from aqua.logger import log_configure
from aqua.diagnostics.core import open_cluster, close_cluster
from aqua.util import create_folder, dump_yaml, load_yaml

cdo = Cdo()

def parse_args():
    """Parse command line arguments for the regrid comparison"""
    parser = argparse.ArgumentParser(description="Regrid benchmark.")
    parser.add_argument('--nproc', type=int, default=1, help="Number of Dask workers")
    parser.add_argument('--outdir', type=str, default='./', help='Output directory for the data production')
    parser.add_argument('--loglevel', '-l', type=str, default='INFO', help="Logging level")

    return parser.parse_args()

def compute_cdo(filepath: str, weightspath:str, targetgridfile: str, nproc: int, outdir: str = './', 
                loglevel: str = 'INFO'):
    """
    Compute the regridding using CDO.
    It times:
        - Total time taken for regridding
    
    Args:
        filepath (str): Path to the input file.
        weightspath (str): Path to the weights file.
        targetgridfile (str): Path to the target grid
        nproc (int): Number of Dask workers.
        outdir (str): output directory. Default to './'
        loglevel (str): Logging level. Defaults to 'INFO'.
    """
    logger = log_configure(log_level=loglevel, log_name='RegridComparison-CDO')
    start_time = time.time()
    logger.info(f"Start time: {start_time:.2f}")

    output = cdo.remap(targetgridfile + ',' + weightspath, input=filepath, returnXDataset=True).load()
    time1 = time.time()

    logger.info(f"CDO regridding completed in {time1 - start_time:.2f} seconds")

    filename = os.path.join(outdir, f'regridded_cdo{nproc}_{int(time.time())}.nc')
    output.to_netcdf(filename)
    time2 = time.time()
    compute_time = time2 - time1
    logger.info(f"Data saved to {filename} in {compute_time:.2f} seconds")

    total_time = time2 - start_time
    logger.info(f"Total time taken: {total_time:.2f} seconds")

    del output
    gc.collect()

    return compute_time, total_time

def compute_aqua(catalog: str, model: str, exp: str, source: str, nproc: int,
                 regrid: str = 'r100', outdir: str = './', loglevel: str = 'INFO'):
    """
    Compute the regridding using AQUA Reader.
    It times:
        - Time taken to retrieve data
        - Time taken to compute data
        - Time taken to I/O the data
        - Total time

    Args:
        catalog (str): Name of the catalog.
        model (str): Name of the model.
        exp (str): Name of the experiment.
        source (str): Name of the source.
        nproc (int): Number of Dask workers.
        regrid (str): Target grid for regridding. Defaults to 'r100'.
        loglevel (str): Logging level. Defaults to 'INFO'.
    """
    logger = log_configure(log_level=loglevel, log_name='RegridComparison-AQUA')
    start_time = time.time()
    logger.info(f"Start time: {start_time:.2f}")

    reader = Reader(catalog=catalog, model=model, exp=exp, source=source,
                    nproc=nproc, regrid=regrid, loglevel=loglevel, chunks='D')
    data = reader.retrieve(var='tprate')
    time1 = time.time()
    retrieve_time = time1 - start_time
    logger.info(f"Data retrieval time: {retrieve_time:.2f} seconds")

    data_regridded = reader.regrid(data)
    data_regridded.load()
    time2 = time.time()
    compute_time = time2 - time1
    logger.info(f"Data computation time: {compute_time:.2f} seconds")

    filename = f"{model}_{exp}_{source}_AQUAregridded{nproc}_{int(time.time())}.nc"
    filename = os.path.join(outdir, filename)
    data_regridded.to_netcdf(filename)
    time3 = time.time()
    io_time = time3 - time2
    logger.info(f"Data I/O time: {io_time:.2f} seconds")

    total_time = time3 - start_time
    logger.info(f"Total time taken: {total_time:.2f} seconds")

    del data_regridded
    gc.collect()

    return retrieve_time, compute_time, io_time, total_time

def compute_smmregrid(input_file, weights_file, nproc: int,
                      outdir: str = './', loglevel: str = 'INFO'):
    """
    Compute the regrid using smmregrid
    It times:
        - Time taken to compute data
        - Time taken to I/O the data
        - Total time

    Args:
        input_file (str): file to regrid
        weights_file (str): path of the weights
        nproc (int): Number of Dask workers.
        outdir (str, opt): where to store the regridded file
        loglevel (str): Logging level. Defaults to 'INFO'.
    """
    logger = log_configure(log_level=loglevel, log_name='RegridComparison-smmregrid')
    start_time = time.time()
    logger.info(f"Start time: {start_time:.2f}")

    xfield = xr.open_mfdataset(input_file, chunks={"time": 24})
    wfield = xr.open_mfdataset(weights_file)

    time1 = time.time()
    setup_time = time1 - start_time
    logger.info(f"Dataset setup time: {setup_time:.2f}")

    interpolator = Regridder(weights=wfield)

    data_regridded = interpolator.regrid(xfield)
    data_regridded.load()

    time2 = time.time()
    compute_time = time2 - time1
    logger.info(f"Compute time: {compute_time:.2f}")

    filename = f"smmregrid_regridded{nproc}_{int(time.time())}.nc"
    filename = os.path.join(outdir, filename)

    data_regridded.to_netcdf(filename)

    time3 = time.time()
    io_time = time3 - time2 + setup_time
    logger.info(f"I/O time (setup + write): {io_time:.2f}")

    total_time = time3 - start_time
    logger.info(f"Total time: {total_time:.2f}")

    del data_regridded
    gc.collect()

    return compute_time, io_time, total_time


if __name__ == '__main__':

    args = parse_args()
    nproc = args.nproc
    outdir = os.path.join(args.outdir, 'output')
    loglevel = args.loglevel

    create_folder(outdir, loglevel=loglevel)

    logger = log_configure(log_level=loglevel, log_name='RegridBenchmark')

    # Hardcoded values, which catalog entry to test and the corresponding filepath
    # AQUA will open the NetCDF with the Reader, while CDO will directly open the file
    catalog = 'data-access'
    model = 'IFS-FESOM'
    exp = 'story-2017-historical-HPC'
    source = 'hourly-regrid'
    filepath = '/scratch/project_462000911/mnurisso/data-access/regrid-catalog/IFS-FESOM_story-2017-historical-HPC_hourly-hpz9-atm2d_tprate_20180101T0000-20180131T2300.nc'
    weightspath = '/appl/local/climatedt/data/AQUA/weights/weights_hpz9-nested_ycon_r100_l2d.nc'
    targetgridfile = './r360x180.nc'
    repetitions = 10

    if nproc > 1:
        logger.info(f"Opening a cluster with {nproc} workers")
        client, cluster, private_cluster = open_cluster(nworkers=nproc, cluster=None, loglevel=loglevel)
    else:
        logger.info("No dask cluster is opened, using local Dask client")

    # Initialize results to zero
    cdo_compute_time = cdo_total_time = 0
    retrieve_time = compute_time = io_time = total_time = 0
    smm_compute_time = smm_io_time = smm_total_time = 0

    for i in range(repetitions):

        if nproc == 1:
            cdo_ct, cdo_tt = compute_cdo(
                filepath=filepath, weightspath=weightspath, targetgridfile=targetgridfile,
                loglevel=loglevel, outdir=outdir, nproc=nproc
            )
            cdo_compute_time += cdo_ct
            cdo_total_time += cdo_tt

        r_time, c_time, i_time, t_time = compute_aqua(
            catalog=catalog, model=model, exp=exp, source=source, nproc=nproc,
            loglevel=loglevel, outdir=outdir
        )
        retrieve_time += r_time
        compute_time += c_time
        io_time += i_time
        total_time += t_time

        smm_ct, smm_io, smm_tt = compute_smmregrid(
            input_file=filepath, weights_file=weightspath, outdir=outdir,
            loglevel=loglevel, nproc=nproc
        )
        smm_compute_time += smm_ct
        smm_io_time += smm_io
        smm_total_time += smm_tt

    # Average over repetitions
    if repetitions > 0:
        if nproc == 1:
            cdo_compute_time /= repetitions
            cdo_total_time /= repetitions

        retrieve_time /= repetitions
        compute_time /= repetitions
        io_time /= repetitions
        total_time /= repetitions
        smm_compute_time /= repetitions
        smm_io_time /= repetitions
        smm_total_time /= repetitions

    results_file = './regrid_comparison_results.yaml'
    if os.path.exists(results_file):
        results = load_yaml(results_file)
    else:
        results = {}
    # Store the results in the running folder
    current_results = {
        f'AQUA_{nproc}': {
            'retrieve_time': retrieve_time,
            'compute_time': compute_time,
            'io_time': io_time,
            'total_time': total_time
        },
        f'smmregrid_{nproc}': {
            'compute_time': smm_compute_time,
            'io_time': smm_io_time,
            'total_time': smm_total_time
        }
    }
    if nproc == 1:
        cdo_dict = {'compute_time': cdo_compute_time,
                    'total_time': cdo_total_time}
        current_results['CDO'] = cdo_dict
    
    results.update(current_results)

    dump_yaml(outfile=results_file, cfg=results)
    
    if nproc > 1:
        logger.info("Closing the cluster")
        close_cluster(client, cluster, private_cluster, loglevel=loglevel)