# Aggregated crop extreme climate indicators

Due to file size, processed data files are hosted externally on Zenodo:

To replicate results, download these files and place them in this directory.

## Overview of data files

generated from `code/scripts/indicators_drywet_aggr.py`
- `FDD_aggr.nc` — Annual **frequency of extreme dry days** (days with precipitation < 0.5th percentile value)
- `FWD_aggr.nc` — Annual **frequency of extreme wet days** (days with precipitation > 95th percentile value)
- `LDS_aggr.nc` — Annual **longest dry spell** (consecutive days with precipitation < 0.5th percentile value)
- `LWS_aggr.nc` — Annual **longest wet spell** (consecutive days with precipitation > 95th percentile value)
- `TPR_aggr.nc` — Annual **total precipitation** over growing-season days 


## Notes

- All indicators are computed per gridcell and calendar year.
- Only days during which **at least one major crop** is grown at a location (based on crop calendars) are included in the calculation.
- All data files are in **NetCDF format**.
- These data are used for the **main analysis of the paper** (aggregated over crops)


