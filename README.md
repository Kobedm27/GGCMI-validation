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
Note that we cannot provide the raw source data used for this study in this repository as they are under data license on other open-source repositories. Nevertheless, to be able to replicate the entire analysis, we give detailed instructions on how to download and organize the data in the folder structure of this repository under the `data/` folder. To test the functionality of the code we recommend to only download for 2-3 model simulations, since the data can be memory intensive. 

## License
Licensed under the [MIT license](LICENSE).


