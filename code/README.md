# Code

This project includes both R and Python code used to conduct the analysis in:

**"Global Gridded Crop Models Underestimate Yield Losses from Climatic Extremes"**

## Structure

- `notebooks/`: R + Quarto notebooks used for main figures and analysis
- `python/`: Python scripts for specific preprocessing steps

## Languages

- **R + Quarto** for all main analyses and figures
- **Python** for the preparation of the climatic extremes data

---

## R Environment

See `code/notebooks/README.md` for how to run `.qmd` notebooks.

---

## Python Environment

If needed, create the environment with:

```bash
conda env create -f environment.yml
conda activate crop-extremes
