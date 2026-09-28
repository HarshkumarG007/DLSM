# DLSM Academic Preprint & LaTeX Source

This directory contains the publication-ready LaTeX manuscript, BibTeX citations, figures, and preprint deposit packaging for the **Digital Lifestyle Spillover Model (DLSM)** research article.

## Files Overview
- **`PREPRINT_SUBMISSION_METADATA.md`**: Complete copy-paste submission metadata dossier for **arXiv** (`cs.AI`/`cs.CY`), **medRxiv** (`Digital Health`/`Epidemiology`), and **TechRxiv** (`IEEE Engineering in Medicine and Biology`), including title, formatted abstracts, taxonomies, ethics disclosures, and author metadata.
- **`dlsm_preprint_package.zip`**: Self-contained preprint archive containing `main.tex`, `references.bib`, and high-resolution publication figures for 1-click submission or Overleaf compilation.
- **`manuscript.tex`**: Two-column IEEE/Nature-styled LaTeX source code.
- **`references.bib`**: BibTeX bibliography database.
- **`compile_manuscript.py`**: Local compilation helper script.

## Continuous Integration & Automated PDF Compilation
Every push affecting `docs/latex/**` automatically triggers GitHub Actions workflow `.github/workflows/manuscript.yml`, which compiles the TeX source and attaches the publication artifact `dlsm_academic_manuscript` (`manuscript.pdf`).

## One-Click Overleaf Compilation
1. Navigate to [Overleaf](https://www.overleaf.com).
2. Click **New Project** > **Upload Project**.
3. Select `dlsm_preprint_package.zip`.
4. Overleaf automatically compiles `main.tex` into a publication-grade PDF.
