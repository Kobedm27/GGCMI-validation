# Global Gridded Crop Models underestimate yield losses from climatic extremes

This repository contains the code supporting the paper:

> **"Global gridded crop models systematically underestimate yield losses from climatic extremes"**  
> Submitted to *Nature Climate Change*, 2026.

Please cite this work as:

xxx

## Contents

- `code/`: Scripts and notebooks for data processing and analysis
- `data/`: Raw and processed data used in the study (raw data access instructions provided)
- `results/`: Folders where final figures and tables will be stored

## Crop abbreviations

- **mai** = maize
- **soy** = soybean
- **wwh** = winter wheat
- **swh** = spring wheat
- **ri1** = rice in the first growing season
- **ri2** = rice in the second growing season
- **aggr** = aggregated across all crops listed above

## Getting Started

To reproduce the analysis:
```bash
git clone https://github.com/Kobedm27/GGCMI-validation.git
cd GGCMI-validation
```
First run all code under `cropdata_preprocessing`, then `climdata_preprocessing`, and finally one can run the notebooks under `analysis`. 

The code is structured to store all intermediate data and final figures in predefined folders within the repository.

## Software dependencies and packages

We used R version 4.5.0 with the following packages:
- `ncdf4`
- `testthat`
- `stringr`
- `raster `
- `dplyr`
- `tidyr`
- `purrr`
- `broom`
- `tidyverse`
- `sjPlot`
- `rnaturalearth`
- `viridis`
- `spdep`

Additionally, Python 3.11.5 was used with the following packages:
- `pyreadr`
- `numpy`
- `xarray`
- `pandas`

No specialized hardware is required to replicate the analysis. However, access to a high-performance computing system, as used in this study, may help to alleviate computational constraints.

## Source data and demo
The raw source data used in this study cannot be provided in this repository, as they are subject to data licenses from external open-source repositories. However, to ensure full reproducibility of the analysis, we provide detailed instructions for downloading and organizing the data within the `data/ folder` of this repository.

For testing the code or running a demonstration, we recommend downloading the `GGCMI_yields` data for only 2–3 models, 1–2 crops and for one extreme type (e.g. hot), as the full dataset can be memory-intensive for local use. In that case, please adapt the appropriate lines of code where e.g. crop names are defined and later looped over:

`crops <- c("mai", "ri1", "ri2", "soy", "swh", "wwh")`

## Expected install and run time
Installing the repository should take less than 5 minutes. Preprocessing the downloaded (demo) source data can take several hours, depending on system resources. Once preprocessing is complete, the analysis code should run in roughly one hour for the demo on a standard desktop computer.

## License
Licensed under the [MIT license](LICENSE).


