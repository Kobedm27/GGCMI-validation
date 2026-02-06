# Integrated crop yield data 

This folder contains the fully preprocessed crop yield data ready for analysis. These are the results from the `03_integration_detrending` notebook. The ISIMIP3a model simulations (irrigated and rainfed) are integrated into one yield value per observation (gridcell-year) and merged with the corresponding GDHY benchmark data. Then, both simulated and benchmark data are quadratically detrended. 

The folder contains:
- `crop_specific_data.RData`: contains the ready dataframes for each crop separately
- `aggr_bench.RData`: dataframe with the ready GDHY benchmark data aggregated over crops
- `aggr_sim.RData`: dataframe with the ready ISIMIP3a simulation data aggregated over crops

The data can be downloaded from this link: https://doi.org/10.5281/zenodo.18496260
