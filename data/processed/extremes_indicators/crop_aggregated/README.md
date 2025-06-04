# Aggregated crop extreme climate indicators

This folder contains the extreme climate indicator data files for the **main analysis of the paper** (aggregated over crops)


## Overview of data files

from `code/scripts/indicators_drywet_aggr.py`
- `FDD_aggr.nc` — Annual **frequency of extreme dry days** (days with precipitation < 0.5th percentile value)
- `FWD_aggr.nc` — Annual **frequency of extreme wet days** (days with precipitation > 95th percentile value)
- `LDS_aggr.nc` — Annual **longest dry spell** (consecutive days with precipitation < 0.5th percentile value)
- `LWS_aggr.nc` — Annual **longest wet spell** (consecutive days with precipitation > 95th percentile value)
- `TPR_aggr.nc` — Annual **total precipitation** over growing-season days 


## Notes

- All indicators are computed per grid cell and calendar year.
- Only days during which **at least one major crop** is grown at a location (based on crop calendars) are included in the calculation.
- Scripts used to generate these files begin with `indicators_` and end with `_aggr` and can be found in `code/scripts/`.


