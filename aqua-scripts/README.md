# What's this folder

This folder contains a series of scripts based on the [AQUA code](https://github.com/DestinE-Climate-DT/AQUA) to compute time or spatial aggregation of data.
This is done within the effort of comparing the capabilities of accessing high-resolution data stored or accessed with different formats.
The code has been used to perform the benchmarks presented in the paper "AQUA v1.0.0: The Application for QUality Assessment for the Climate Change Adaptation Digital Twin - the core engine".

## Reproduce the plots

In the paper "AQUA v1.0.0: The Application for QUality Assessment for the Climate Change Adaptation Digital Twin - the core engine" figure 5 and figure 6 show the results of the benchmarks.
Figure 5 can be reproduced running the notebook `simple_reader/plots_4months.ipynb`, while figure 6 can be reproduced running the notebook `regrid/plot.ipynb`.
These two notebooks open the results of the benchmarks and produce the plots in the paper. The notebooks are self-contained and can be run without any additional setup.

## Reproduce the benchmarks

It is possible to reproduce the benchmarks presented in the paper by running the scripts in the `simple_reader` and `regrid` folders.
A prerequisite of the benchmarks is to have access to the data used in the paper or a similar dataset from the Climate Digital Twin initiative.

An `install-aqua.sh` script is provided to install the AQUA code and its dependencies.
However a more comprehensive and maintained installation example is available in the [climatedt-community-resources](https://github.com/DestinE-Climate-DT/climatedt-community-resources/blob/main/example_aqua/aqua_installation_and_setup.md) repository.
This example not only installs AQUA, but also contains the info on how to access the Climate Digital Twin data and how to set up the environment to run the benchmarks.

A customized AQUA catalog, called `aqua_catalog` is available in the main folder of this repository.
It contains the info to access the dataset originally used in the benchmarks, making explicit the access from the HPC FDB or the Bridge FDB, in order to take into account the possible differences in the access time.

Note: Climate Digital Twin data could be in the future be replaced by newer version of the data. This will require to use a different catalog. Please contact the authors of the paper for more information on how to access the data and how to set up the environment to run the benchmarks if any of the data is not available anymore.

Note: Some benchmarks make use of `open_cluster` and `close_cluster` from `aqua.diagnostics.base`. This module will be described in a companion paper. To reproduce the benchmarks the user can substitute these functions with pure dask code, using `dask.distributed.Client` and `client.close()`.

### Figure 5 benchmark

The code to reproduce the figure 5 is in the `simple_reader` folder.

This folder contains the code to read data from a source and compute the monthly aggregation of the data.
The code is based on the AQUA code, with a focus on reading and aggregating the data.

`reader_monthly_test.py` is the main code used to test the code.
By default it creates a month of 1 deg data from a desired source of the catalog.
It has many features in order to customize engine, chunking, dates, number of repetitions, etc.

The bash scripts used to submit the jobs to the HPC are contained in `simple_reader/array_4months`: this folder contains bash scripts to launch 2d data analysis with an array of chunking or workers, for 4 months of data. It is used to produce the left panel of figure 5 in the paper.

### Figure 6 benchmark

The code to reproduce the figure 6 is in the `regrid` folder.

The folder contains the code to perform spatial regridding of the data.
It is based on the [smmregrid](https://github.com/jhardenberg/smmregrid) code, which is internally used by AQUA to perform spatial regridding.
The code is simplified to focus on the regridding of data, in order to test the regridding capabilities and compare against CDO.

First, the `data-production.py` code is used to store on disk the data to be regridded, due to the necessity for CDO of having the data on disk.
A `data-production.sh` script is also provided to facilitate the execution of the `data-production.py` code on HPC.
Then, the `regrid-comparison.py` code is used to perform the regridding of the data with smmregrid alone, AQUA and CDO, and to compare the results.
The `regrid-comparison.sh` script is provided to facilitate the execution of the `regrid-comparison.py` code on HPC and it contains an array of jobs to perform the regridding with different number of workers.
