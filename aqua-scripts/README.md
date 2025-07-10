# What's this folder

This folder contains a series of scripts based on the [AQUA code](https://github.com/DestinE-Climate-DT/AQUA) to compute time or spatial aggregation of data.
This is done within the effort of comparing the capabilities of accessing high-resolution data stored or accessed with different formats.

`reader_monthly_test.py` is the main code used to test the code. By default it creates a month of 1 deg data from a desired source of the catalog. It has many features in order to customize engine, chunking, dates, number of repetitions, etc.
It is used by most of the benchmark in the folders 

- `array`: this folder contains bash files to launch 2d data analysis with an array of chunking or workers
- `array3d`: this folder contains bash files to launch 2d data analysis with an array of chunking or workers
- `polytope`: this folder contains experimental access to data with the polytope engine (managed internally by AQUA). Different chunking are tested to check if there is an effect in the total time (due to queue time or other possible issues).
- `bridge`: this folder test the data access with Bridge FDB, accessing the data not in the HPC but still not with the DataLake, in order to check if a difference from the pure HPC FDB access is present.
- `soft_scaling`: in this folder we double workers and we double the lenght of data to process, to study the soft scaling with Dask.