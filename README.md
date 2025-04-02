Compare data access to several high resolution runs
===================================================

We compare data aces to several high resolution runs:
- nextGESM IFS-FESOM. Stored as GRIB, exposed as zarr using [gribscan](https://github.com/gribscan/gribscan)
- nextGEMS ICON. Stored nativelly as zarr.
- DestinE IFS-FESOM storylines. Stored nativelly as GRIB with FDB.

All runs are distributed on HEALPix H512, which is about 3M points. For examples we try to use similar number of time steps and vertical levels.

We distinguish between two main modes of access: remote (e.g. from local machine) and server (when compute is next to the data).

### Remote

- `earthkit_remote.ipynb` - use earthkit to access data from DESP
- `EERIE_cloud_remote.ipynb` - use xarray to access data from EERIE cloud

### Server

- `compare_access_grib_zarr_server_side.ipynb` - use xarray with dask to access data stored in "native zarr" and GRIB exposed as zarr. Run on levante on single node (256 Gb of memory, 128 cores).
- `compare_access_grib_zarr_server_side.ipynb` - same as previous, but without dask.

## Results do far:

[In this this file for a moment](https://docs.google.com/spreadsheets/d/1xj_2v5IYKr2tEPa3Z9Uf9-kquveRIbx1MIeQeBGfQHY/edit?usp=sharing)
