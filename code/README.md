# Code

This directory contains all analysis notebooks used in the study:

**"Global Gridded Crop Models Underestimate Yield Losses from Climatic Extremes"**

All analyses were conducted in **R** using **Quarto notebooks (`.qmd`)**.

## Structure

- `notebooks/`: 

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

