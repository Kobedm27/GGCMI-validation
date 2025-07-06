# Analysis notebooks

This folder contains all **Quarto notebooks (both as `.qmd` and `.html`)** used in the analysis for the paper:

**"Global Gridded Crop Models underestimate yield losses from climatic extremes"**

All notebooks are written in **R** using [Quarto](https://quarto.org).

## File overview

- `00_filtering_extremes` — Filters the datasets for extremes, gets rid of "marginal" land and produces model ensemble median
- `01_general_performance` — Creates figures to analyse the model performance under general conditions
- `02_spatial_extremes_performance` — Creates figures to spatially analyze model ensemble performance under extremes
- `03_rainclouds_extremes_performance` — Creates figures to analyze each model performance in terms of over and underestimation
- `04_heatmaps_extremes_performance` — Creates regional heatmap figures analyzing model performance in terms of KGE and hit rate. 

## Reproducibility

Each notebook will:
- Load processed data from `data/processed/`
- Perform analysis
- Save outputs to `results/`

Note that: 
- The `.html` files provided in the `code/analysis/` folder can be downloaded and viewed to quickly see for each figure the corresponding code and the rendered plot without having to run the notebook.
- Rerun the corresponding `.qmd` notebook if updates are needed.

