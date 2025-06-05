# Crop specific extreme climate indicators

Due to file size, processed data files are hosted externally on Zenodo:

To replicate results, download these files and place them in this directory.

## Crop Placeholder

In all filenames and script names, `crop` is a placeholder and should be replaced with one of the following main crops:

- `mai` - maize
- `ri1` - first growing season rice
- `ri2` - second growing season rice
- `soy` - soy
- `swh` - spring wheat
- `wwh` - winter wheat

For example, `indicators_drywet_mai.py` generates `FDD_mai.nc`, `TPR_mai.nc`, etc.

## Overview of data files

generated from `code/scripts/indicators_drywet_crop.py`
- `FDD_crop.nc` — Annual **frequency of extreme dry days** (days with precipitation < 0.5th percentile value)
- `FWD_crop.nc` — Annual **frequency of extreme wet days** (days with precipitation > 95th percentile value)
- `LDS_crop.nc` — Annual **longest dry spell** (consecutive days with precipitation < 0.5th percentile value)
- `LWS_crop.nc` — Annual **longest wet spell** (consecutive days with precipitation > 95th percentile value)
- `TPR_crop.nc` — Annual **total precipitation** over growing-season days 

generated from `code/scripts/indicators_hot_crop.py`
- `FHD_crop.nc` — Annual **frequency of extreme hot days** (days with tasmax > 95th percentile value)
- `LHS_crop.nc` — Annual **longest hot spell** (consecutive days with tasmax > 95th percentile value)

## Notes

- All indicators are computed per gridcell and crop specific calendar year.
- All data files are in **NetCDF format**.
- These data are used for the **appendix figures of the paper** (crop specific)
