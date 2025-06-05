# Crop specific extreme climate indicators

Due to file size, processed data files are hosted externally on Zenodo:

To replicate results, download these files and place them in this directory.

## Crop Placeholder

In all filenames and script names, `<crop>` is a placeholder and should be replaced with one of the following main crops:

- `maize`
- `rice1`
- `rice2`
- `soy`
- `spring_wheat`
- `winter_wheat`

For example, `indicators_drywet_maize.py` generates `FDD_maize.nc`, `TPR_maize.nc`, etc.

## Overview of data files

generated from `code/scripts/indicators_drywet_<crop>.py`
- `FDD_<crop>.nc` — Annual **frequency of extreme dry days** (days with precipitation < 0.5th percentile value)
- `FWD_<crop>.nc` — Annual **frequency of extreme wet days** (days with precipitation > 95th percentile value)
- `LDS_<crop>.nc` — Annual **longest dry spell** (consecutive days with precipitation < 0.5th percentile value)
- `LWS_<crop>.nc` — Annual **longest wet spell** (consecutive days with precipitation > 95th percentile value)
- `TPR_<crop>.nc` — Annual **total precipitation** over growing-season days 


## Notes

- All indicators are computed per gridcell and crop specific calendar year.
- All data files are in **NetCDF format**.
- These data are used for the **appendix figures of the paper** (crop specific)
