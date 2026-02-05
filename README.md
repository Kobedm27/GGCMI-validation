# Global Gridded Crop Models underestimate yield losses from climatic extremes

This repository contains the code supporting the paper:

> **"Global gridded crop models underestimate yield losses from climatic extremes"**  
> Submitted to *Nature Climate Change*, 2026.

Please cite this work as:


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
First run all code under `cropdata_preprocessing`, then `climdata_preprocessing`, and finally one can run the notebooks under `analysis`

The code is structured to store all intermediate data and final figures in predefined folders within the repository.

## Source data and demo
The raw source data used in this study cannot be provided in this repository, as they are subject to data licenses from external open-source repositories. However, to ensure full reproducibility of the analysis, we provide detailed instructions for downloading and organizing the data within the `data/ folder` of this repository.

For testing the code or running a demonstration, we recommend downloading the `GGCMI_yields` data for only 2–3 models and 1–2 crops, as the full dataset can be memory-intensive for local use.

## License
Licensed under the [MIT license](LICENSE).


