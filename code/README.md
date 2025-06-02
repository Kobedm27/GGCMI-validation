# Code

This directory contains all analysis notebooks used in the study:

**"Global Gridded Crop Models Underestimate Yield Losses from Climatic Extremes"**

All analyses were conducted in **R** using **Quarto notebooks (`.qmd`)**.

## Structure

- `notebooks/`: All figures and results are generated through individual Quarto notebooks.
  Each notebook is numbered and titled according to its output.

## Getting Started

1. Install [Quarto](https://quarto.org/)
2. Install [R](https://cran.r-project.org/)
3. Install required R packages:
   ```r
   install.packages(c("tidyverse", "terra", "sf", "lubridate", "patchwork", "ggtext", "arrow"))
  ```
