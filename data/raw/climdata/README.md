# Climate Data

This folder is intended to store the ISIMIP3a climate forcing dataset **GSWP3-W5E5**, used to compute climate extremes indicators in our study. 

The data is **not included** in the GitHub repository. To reproduce the results of the analysis the required data files need to be downloaded manually. 

## Download Instructions

The required files can be downloaded from the ISIMIP repository:[https://doi.pangaea.de/10.1594/PANGAEA.909132](https://doi.pangaea.de/10.1594/PANGAEA.909132)

### Steps:

1. Click the **“Download dataset”** button to obtain a `.zip` archive of all yield files.
2. This zip file is already organized by crop.
3. Unzip the archive.
4. **Rename each crop folder** to match the structure expected in this repository:
   - `mai` for maize  
   - `soy` for soybean  
   - `swh` for spring wheat  
   - `wwh` for winter wheat  
   - `ri1` for rice (major growing season)  
   - `ri2` for rice (second growing season)  
5. Place the renamed folders into the following path: `data/raw/benchmark_yields/`

## Dataset Description

Each data file covers one year within the period from 1981 to 2016 for one specific crop with a resolution of 0.5°. The outputs are always provided in **NetCDF format**.

The benchmark data is a hybrid product of both national census data from FAO and remote sensing observations. More details on the dataset are available in the original data publication: [Iizumi and Sakai (2020)](https://doi.org/10.1038/s41597-020-0433-7)


