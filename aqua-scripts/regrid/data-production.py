import argparse
import os
from aqua import Reader
from aqua.logger import log_configure
from aqua.diagnostics.core import open_cluster, close_cluster
from aqua.util import create_folder

def parse_args():
    """Parse command line arguments for the regrid data production."""
    parser = argparse.ArgumentParser(description="Regrid data production.")
    parser.add_argument('--nproc', type=int, required=True, help="Number of Dask workers")
    parser.add_argument('--var', type=str, required=True, help="Variable name to extract")
    parser.add_argument('--catalog', type=str, required=True, help="Catalog name")
    parser.add_argument('--model', type=str, required=True, help="Model name")
    parser.add_argument('--exp', type=str, required=True, help="Experiment name")
    parser.add_argument('--source', type=str, required=True, help="Source name")
    parser.add_argument('--startdate', type=str, default='20180101T0000', help='Startdate for computation')
    parser.add_argument('--enddate', type=str, default='20180131T2300', help='Enddate for computation')
    parser.add_argument('--outdir', type=str, default='./', help='Output directory for the data production')
    parser.add_argument('--loglevel', type=str, default='INFO', help="Logging level")
    parser.add_argument('--engine', type=str, default='fdb', help="Engine to use for FDB access (fdb or polytope)")

    return parser.parse_args()

if __name__ == '__main__':

    args = parse_args()
    var = args.var
    catalog = args.catalog
    model = args.model
    exp = args.exp
    source = args.source
    engine = args.engine
    nproc = args.nproc
    startdate = args.startdate
    enddate = args.enddate
    outdir = args.outdir
    loglevel = args.loglevel

    logger = log_configure(log_level=loglevel, log_name='RegridDataProduction')

    if nproc > 1:
        logger.info(f"Opening a cluster with {nproc} workers")
        client, cluster, private_cluster = open_cluster(nworkers=nproc, cluster=None, loglevel=loglevel)
    else:
        logger.info("No dask cluster is opened, using local Dask client")

    create_folder(outdir, loglevel)

    reader = Reader(catalog=catalog, model=model, exp=exp, source=source,
                    nproc=nproc, engine=engine, loglevel=loglevel)
    data = reader.retrieve(var=var, startdate=startdate, enddate=enddate)

    filename = f"{model}_{exp}_{source}_{var}_{startdate}-{enddate}.nc"
    filename = os.path.join(outdir, filename)

    data.to_netcdf(filename)

    logger.info(f"Results saved successfully to {filename}")
    if nproc > 1:
        logger.info("Closing the cluster")
        close_cluster(client, cluster, private_cluster, loglevel=loglevel)