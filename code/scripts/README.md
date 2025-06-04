# Python Scripts

This folder contains **Python scripts** used for preprocessing the climatic extremes data in support of the main R/Quarto-based analysis.

## File Overview

- `regrid_crop_yield.py` — Regrids crop yield data to a common spatial resolution
- `merge_climate_fields.py` — Combines temperature and precipitation into a single dataset
- `convert_netcdf_to_csv.py` — Converts selected NetCDF variables into tabular format for import into R

## Dependencies

Install the required Python packages with:

```bash
# Using pip
pip install -r requirements.txt

# Or using conda
conda env create -f GGCMIval.yml
conda activate GGCMIval
