import argparse
import time
from aqua import LRAgenerator

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Process LRA generation parameters.")
    parser.add_argument('--nproc', type=int, required=True, help="Number of Dask workers")
    parser.add_argument('--var', type=str, required=True, help="Variable name to extract")
    parser.add_argument('--catalog', type=str, required=True, help="Catalog name")
    parser.add_argument('--model', type=str, required=True, help="Model name")
    parser.add_argument('--exp', type=str, required=True, help="Experiment name")
    parser.add_argument('--source', type=str, required=True, help="Source name")
    parser.add_argument('--regrid', type=str, required=True, help="Target grid")
    parser.add_argument('--freq', type=str, required=True, help="Frequency of the data")
    parser.add_argument('--outdir', type=str, required=True, help="Output directory")
    parser.add_argument('--tmpdir', type=str, required=True, help="Temporary directory for processing")

    args = parser.parse_args()
    
    varname = args.var
    model = args.model
    exp = args.exp
    source = args.source
    catalog = args.catalog
    regrid= args.regrid
    frequency = args.freq
    outdir = args.outdir
    tmpdir = args.tmpdir
    region = None
    nproc = args.nproc

    print(f"Generating LRA for {varname} for {model} {exp} {source} from {catalog} with {nproc} workers.")
    start_time = time.time()
    print(f"Start time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))}")
    if region is not None:
        print(f"Region specified: {region}")
    lra = LRAgenerator(
                    catalog=catalog, model=model, exp=exp, source=source,
                    var=varname, resolution=regrid, stat='mean', drop=True,
                    frequency=frequency, fix=True, nproc=nproc,
                    outdir=outdir, tmpdir=tmpdir,
                    performance_reporting=True,
                    loglevel="DEBUG", definitive=True, compact="cdo",
                    region=region)
    print("---CHECK------")
    lra.check_integrity(varname)
    print("---RETRIEVE------")
    lra.retrieve()
    print("---GENERATE------")
    lra.generate_lra()
    end_time = time.time()
    print(f"End time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time))}")
    print(f"Total time taken: {end_time - start_time:.2f} seconds for the {nproc} setup")
    print("LRA generation completed successfully.")