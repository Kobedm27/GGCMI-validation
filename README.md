# Global Gridded Crop Models systematically underestimate yield losses from climatic extremes

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

To reproduce the entire analysis:
```bash
git clone https://github.com/Kobedm27/GGCMI-validation.git
cd GGCMI-validation
```
First run all code under `cropdata_preprocessing`, then `climdata_preprocessing`, and finally one can run the notebooks under `analysis`. 

The code is structured to store all intermediate data and final figures in predefined folders within the repository. Intermediate data are publicly available on https://doi.org/10.5281/zenodo.18496260. 

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

## Source and intermediate data

The raw source data used in this study cannot be included in this repository because they are subject to data licenses from external open-source providers. To ensure full reproducibility, we provide detailed instructions for downloading and organizing all required datasets within the `data/` directory of this repository.

For testing and debugging the preprocessing code, we recommend downloading a reduced subset of the `GGCMI_yields` data (e.g. 2–3 models, 1–2 crops, and a single extreme type such as *hot*), as the full dataset can be memory-intensive on local machines. In this case, please adapt the relevant lines of code where crop names are defined and looped over, for example:
```r
crops <- c("mai", "ri1", "ri2", "soy", "swh", "wwh")
```

To reproduce the quantitative results and figures presented in the paper, we provide the fully processed intermediate data via Zenodo: https://doi.org/10.5281/zenodo.18496260
Please download the folders `extremes_indicators` and `integrated_cropdata` and place them into the corresponding (empty) directories in this repository. Once these folders are correctly organized, all scripts in the `analysis/` directory should run without modification.

## Expected install and run time
Installing the repository and required dependencies should take less than 10 minutes. Preprocessing the raw source data may take several hours, depending on system resources. When using the provided intermediate data, the full analysis pipeline should complete in approximately on hour on a standard desktop computer. 

## License
Licensed under the [MIT license](LICENSE).


