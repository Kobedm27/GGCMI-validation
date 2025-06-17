# Code for preprocessing benchmark and simulated crop yield data

This folder contains the full pipeline for preprocessing crop yields from both simulations and benchmark datasets. The process is divided into three main steps, which should be run in order:

- `01_calendar_adjustment.R`: script that adjusts the calendars in the original simulation data
- `02_ISIMIP3a_dataprep.qmd`: Extracts the calendar-adjusted simulation data and organizes it into structured R dataframes. Also processes ISIMIP3a land-use data to support integration of full-irrigation (firr) and no-irrigation (noirr) runs.
- `03_integration_detrending.qmd`: Integrates the simulation and benchmark yield data, and applies quadratic detrending to remove long-term trends in yields.

## About the files

Each of the .qmd notebooks is provided in two formats:

.qmd (Quarto): Can be run interactively in code editors such as RStudio, VS Code, or Positron.

.html: Rendered output of the .qmd files, providing a readable and shareable overview of the code, results, and outputs without requiring the runtime environment.

The .html files are useful for reviewing the processing steps or sharing your work with collaborators who don't use R or Quarto.
