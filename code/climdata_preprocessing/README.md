# Computation of climate extremes indicators

This folder contains **Python scripts** used for computing netcdf data files with climate extremes indicators from the GSWP3-W5E5 temperature and precipitation data. Be aware that it is necessary to first preprocess the crop data if not done yet.

## Crop Placeholder

In all filenames and script names, `crop` is a placeholder and should be replaced with one of the following main crops:

- `mai` - maize
- `ri1` - first growing season rice
- `ri2` - second growing season rice
- `soy` - soy
- `swh` - spring wheat
- `wwh` - winter wheat

For example, `indicators_drywet_mai.py` generates `FDD_mai.nc`, `TPR_mai.nc`, etc.

## File Overview

- `indicators_drywet_aggr.py` — Extreme climate indicator computation for extreme dry and wet conditions (crop aggregated for main results)
- `indicators_hot_aggr.py` — Extreme climate indicator computation for extreme hot conditions (crop aggregated for main results)
- `indicators_drywet_crop.py` — Extreme climate indicator computation for extreme dry and wet conditions (crop specific for appendix results)
- `indicators_hot_crop.py` - Extreme climate indicator computation for extreme hot conditions (crop specific for appendix results)

## Required python packages
- `pyreadr` - Used to read .RData files from R in Python.
- `numpy` - Used for numerical operations.
- `xarray` - Used for handling labeled multi-dimensional arrays.
- `pandas` - Used for data manipulation and analysis.

