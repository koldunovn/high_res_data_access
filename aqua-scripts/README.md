# What's this folder

This folder contains a series of scripts based on the [AQUA code](https://github.com/DestinE-Climate-DT/AQUA) to compute time or spatial aggregation of data.
This is done within the effort of comparing the capabilities of accessing high-resolution data stored or accessed with different formats.

A script to install AQUA specific folders and the catalog needed to perform the benchmarks is provided in the `install-aqua.sh` file. It is recommended to run this script before running any of the benchmarks.

## `simple_reader` folder

This folder contains the code to read data from a source and compute the monthly aggregation of the data. The code is based on the AQUA code, but it is simplified to focus on the reading and aggregation of data.

`reader_monthly_test.py` is the main code used to test the code. By default it creates a month of 1 deg data from a desired source of the catalog. It has many features in order to customize engine, chunking, dates, number of repetitions, etc. It is used by most of the benchmarks in the folders.

- `array`: this folder contains bash files to launch 2d data analysis with an array of chunking or workers
- `array3d`: this folder contains bash files to launch 3d data analysis with an array of chunking or workers
- `polytope`: this folder contains experimental access to data with the polytope engine (managed internally by AQUA). Different chunking are tested to check if there is an effect in the total time (due to queue time or other possible issues).
- `bridge`: this folder tests the data access with Bridge FDB, accessing the data not in the HPC but still not with the DataLake, in order to check if a difference from the pure HPC FDB access is present.
- `soft_scaling`: in this folder we double workers and we double the length of data to process, to study the soft scaling with Dask.

## `regrid` folder

This folder contains the code to perform spatial regridding of the data. It is based on the smmregrid code, which is internally used by AQUA to perform spatial regridding. The code is simplified to focus on the regridding of data. The folder is still a WIP and a full benchmark is not yet available. The code is used to test the regridding capabilities and compare against CDO.

## `full_LRA` folder

This folder contains the code to read data from a source and compute the monthly aggregation of the data, but it is based on the full LRA code. It is used to test the full LRA code with different sources and chunking. Only a skeleton of the code is provided, as it is not used in the benchmarks. A visualization notebook is left with some preliminary results. Can be removed in the future.