# Global Gridded Crop Models underestimate yield losses from climatic extremes

This repository contains the code supporting the paper:

> **"Global gridded crop models underestimate yield losses from climatic extremes"**  
> Submitted to *Nature Climate Change*, 2025.

Please cite this work as:

Cornelia Auer, Kobe De Maeyer,...(2025). Global Gridded Crop Models underestimate yield losses from climatic extremes. Nature Climate Change (submitted). DOI: TBD

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

## License
Licensed under the [MIT license](LICENSE).


