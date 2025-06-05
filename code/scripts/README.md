# Python Scripts

This folder contains **Python scripts** used for preprocessing the climatic extremes data in support of the main R/Quarto-based analysis.

## File Overview

- `indicators_drywet_aggr.py` — Extreme climate indicator computation for extreme dry and wet conditions (crop aggregated for main results)
- `indicators_hot_aggr.py` — Extreme climate indicator computation for extreme hot conditions (crop aggregated for main results)
- `indicators_drywet_crop.py` — Extreme climate indicator computation for extreme dry and wet conditions (crop specific for appendix results)
- `indicators_drywet_crop.py` - Extreme climate indicator computation for extreme hot conditions (crop specific for appendix results)

## Required python packages
- `pyreadr` - Used to read .RData files from R in Python.
- `numpy` - Used for numerical operations.
- `xarray` - Used for handling labeled multi-dimensional arrays.
- `pandas` - Used for data manipulation and analysis.

