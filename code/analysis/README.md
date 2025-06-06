# Quarto Notebooks

This folder contains all **Quarto notebooks (`.qmd`)** used in the analysis for the paper:

**"Global Gridded Crop Models Underestimate Yield Losses from Climatic Extremes"**

All notebooks are written in **R** using [Quarto](https://quarto.org).

## File overview

- `regrid_crop_yield.py` — Regrids crop yield data to a common spatial resolution
- `merge_climate_fields.py` — Combines temperature and precipitation into a single dataset
- `convert_netcdf_to_csv.py` — Converts selected NetCDF variables into tabular format for import into R

## Getting Started

1. Install [Quarto](https://quarto.org) and [R](https://www.r-project.org)
2. Install required R packages (see `requirements.R`)
3. Open `.qmd` files in RStudio, Positron or VS Code and click "Render"

## Reproducibility

All figures and results are generated through individual Quarto notebooks. Notebooks are self-contained and titled according to its output.

Each notebook will:
- Load processed data from `data/processed/`
- Perform analysis
- Save outputs to `results/`
