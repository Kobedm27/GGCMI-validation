# Analysis notebooks

This folder contains all **Quarto notebooks (`.qmd`)** used in the analysis for the paper:

**"Global Gridded Crop Models underestimate yield losses from climatic extremes"**

All notebooks are written in **R** using [Quarto](https://quarto.org).

## File overview

- `regrid_crop_yield.py` — Regrids crop yield data to a common spatial resolution
- `merge_climate_fields.py` — Combines temperature and precipitation into a single dataset
- `convert_netcdf_to_csv.py` — Converts selected NetCDF variables into tabular format for import into R

## Reproducibility

Each notebook will:
- Load processed data from `data/processed/`
- Perform analysis
- Save outputs to `results/`

Note that: 
- The `.html` files provided in the `code/analysis/` folder can be downloaded and viewed to quickly see for each figure the corresponding code and the rendered plot without having to run the notebook.
- Rerun the corresponding `.qmd` notebook if updates are needed.

