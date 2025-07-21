import argparse
import time
import os
from aqua import Reader
from aqua.logger import log_configure
from aqua.diagnostics.core import open_cluster, close_cluster
from aqua.util import create_folder

def parse_args():
    """Parse command line arguments for the Reader script."""
    parser = argparse.ArgumentParser(description="Process Reader parameters.")
    parser.add_argument('--nproc', type=int, required=True, help="Number of Dask workers")
    parser.add_argument('--mem_gb', type=int, default=128, help="Allocated memory of the total node in GB")
    parser.add_argument('--chunking', type=str, required=False, help="Chunking to overwrite the default catalog one")
    parser.add_argument('--var', type=str, required=True, help="Variable name to extract")
    parser.add_argument('--catalog', type=str, required=True, help="Catalog name")
    parser.add_argument('--model', type=str, required=True, help="Model name")
    parser.add_argument('--exp', type=str, required=True, help="Experiment name")
    parser.add_argument('--source', type=str, required=True, help="Source name")
    parser.add_argument('--regrid', type=str, required=True, help="Target grid")
    parser.add_argument('--freq', type=str, required=True, help="Frequency of the data")
    parser.add_argument('--startdate', type=str, default='20180101T0000', help='Startdate for computation')
    parser.add_argument('--enddate', type=str, default='20180131T2300', help='Enddate for computation')
    parser.add_argument('--loglevel', type=str, default='INFO', help="Logging level")
    parser.add_argument('--engine', type=str, default='fdb', help="Engine to use for FDB access (fdb or polytope)")
    parser.add_argument('--repetitions', type=int, default=1, help='Number of repetitions to average with. Default to 1')

    return parser.parse_args()

def compute(catalog: str, model: str, exp: str, source: str, var: str, nproc: int,
            startdate: str = '20180101T0000', enddate: str = '20180131T2300',
            regrid: str = 'r100', chunking: str = None, engine: str = 'fdb',
            loglevel: str = 'INFO'):
    """
    Main function to compute 1 month of data using the Reader.
    It times:
        - Time taken to retrieve data
        - Time taken to compute data
        - Time taken to I/O the data

    Args:
        catalog (str): Name of the catalog.
        model (str): Name of the model.
        exp (str): Name of the experiment.
        source (str): Name of the source.
        var (str): Variable name to extract.
        nproc (int): Number of Dask workers.
        startdate (str, opt): Startdate for the retrieve. Default to '20180101T0000'.
        enddate (str, opt): Enddate for the retrieve. Default to '20180131T2300'.
        regrid (str): Target grid for regridding. Defaults to 'r100'.
        chunking (str): Chunking if the Reader default needs to be changed. Default to None.
                        Time chunking can be one of S (step), 10M, 15M, 30M, h, 1h, 3h, 6h, D, 5D, W, M, Y.
        engine (str): Engine to use for FDB access, either 'fdb' or 'polytope'. Defaults to 'fdb'.
        loglevel (str): Logging level. Defaults to 'INFO'.

    Returns:
        tuple: A tuple containing the time taken for retrieval, computation, I/O operation, and total time.
    """
    logger = log_configure(log_level=loglevel, log_name='ReaderMonthlyTest')
    
    # 1. Reader opening and retrieve of data
    start_time = time.time()
    logger.info(f"Start time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))}")

    reader = Reader(catalog=catalog, model=model, exp=exp, source=source, regrid=regrid,
                    nproc=nproc, chunks=chunking, engine=engine, loglevel='ERROR')
    data = reader.retrieve(var=var, startdate=startdate, enddate=enddate)

    eval_starttime = time.time()
    retrieve_time = eval_starttime - start_time
    logger.info(f"Time taken to evaluate Reader: {retrieve_time:.2f} seconds")

    # 2. Regrid and compute monthly mean
    data_regridded = reader.regrid(data)
    data_monthly = reader.timmean(data_regridded, freq='MS')
    data_monthly.load()
    eval_endtime = time.time()

    compute_time = eval_endtime - eval_starttime
    logger.info(f"Time taken to compute: {compute_time:.2f} seconds")

    # 3. I/O operation with random name
    filename = f"{model}_{exp}_{source}_{var}_{regrid}_monthly_{nproc}workers_{int(time.time())}.nc"
    data_monthly.to_netcdf(filename)
    end_time = time.time()
    logger.info(f"End time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time))}")
    io_time = end_time - eval_endtime
    logger.info(f"Time taken for I/O operation: {io_time:.2f}")
    time_taken = end_time - start_time
    logger.info(f"Total time taken: {time_taken:.2f} seconds for the {nproc} setup")

    return retrieve_time, compute_time, io_time, time_taken

if __name__ == '__main__':

    args = parse_args()
    varname = args.var
    catalog = args.catalog
    model = args.model
    exp = args.exp
    source = args.source
    regrid = args.regrid
    frequency = args.freq
    engine = args.engine
    nproc = args.nproc
    mem_gb = args.mem_gb
    startdate = args.startdate
    enddate = args.enddate
    chunking = args.chunking if args.chunking else None
    repetitions = args.repetitions
    loglevel = args.loglevel

    logger = log_configure(log_level=loglevel, log_name='ReaderMonthlyTest')

    if nproc > 1:
        logger.info(f"Opening a cluster with {nproc} workers")
        client, cluster, private_cluster = open_cluster(nworkers=nproc, cluster=None, loglevel=loglevel)
    else:
        logger.info("No dask cluster is opened, using local Dask client")

    times_total = []
    times_retrieve = []
    times_compute = []
    times_io = []

    if repetitions > 1:
        # Often the first Dask run includes cluster setup and graph compilation overhead.
        logger.info("Running warm-up (first attempt is discarded from timing)")
        _, _, _, _ = compute(catalog=catalog, model=model, exp=exp, source=source,
                            var=varname, nproc=nproc, regrid=regrid,
                            startdate=startdate, enddate=enddate,
                            chunking=chunking, engine=engine, loglevel=loglevel)

    for i in range(repetitions):  # We just want to be sure there is no high variability in the results
        logger.info(f"Computing attempt {i} for variable {varname} with {nproc} workers and {mem_gb}GB memory")
        retrieve_time, compute_time, io_time, time_taken = compute(catalog=catalog, model=model, exp=exp, source=source,
                                                                   var=varname, nproc=nproc, regrid=regrid,
                                                                   startdate=startdate, enddate=enddate,
                                                                   chunking=chunking, engine=engine, loglevel=loglevel)
        logger.info(f"Attempt {i} completed in {time_taken:.2f} seconds.")
        logger.info(f"Compute time for attempt {i}: {compute_time:.2f} seconds.")
        times_total.append(time_taken)
        times_retrieve.append(retrieve_time)
        times_compute.append(compute_time)
        times_io.append(io_time)
    
    logger.info(f"Average compute time over {len(times_compute)} attempts: {sum(times_compute) / len(times_compute):.2f} seconds.")
    logger.info(f"Average total time over {len(times_total)} attempts: {sum(times_total) / len(times_total):.2f} seconds.")

    logger.info("Saving results to output directory")
    chunk_name = chunking if chunking is not None else 'default'
    filename = f"./results_{varname}_{nproc}workers_{mem_gb}GB_{chunk_name}chunk.txt"

    with open(f"./{filename}", 'w') as f:
        f.write(f"## Times for {varname} with {nproc} workers and {mem_gb}GB memory\n")
        f.write(f"## Catalog: {catalog}, Model: {model}, Experiment: {exp}, Source: {source}, Regrid: {regrid}, Engine: {engine}\n")
        f.write(f"## Average compute time: {sum(times_compute) / len(times_compute):.2f} seconds\n")
        f.write(f"## Average total time: {sum(times_total) / len(times_total):.2f} seconds\n")
        f.write("## Individual compute times:\n")
        f.write("## Attempt; Total Time (s); Retrieve Time (s); Compute Time (s); I/O Time (s)\n")
        for i, (total_time, retrieve_time, compute_time, io_time) in enumerate(zip(
            times_total, times_retrieve, times_compute, times_io), start=1):
            f.write(f"{i}; {total_time:.2f}; {retrieve_time:.2f}; {compute_time:.2f}; {io_time:.2f}\n")

    logger.info(f"Results saved successfully to {filename}")
    if nproc > 1:
        logger.info("Closing the cluster")
        close_cluster(client, cluster, private_cluster, loglevel=loglevel)
