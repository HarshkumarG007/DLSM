"""
Preprint Packaging Utility for DLSM.
Bundles manuscript.tex, references.bib, high-resolution figures, and submission metadata
into a self-contained archive ready for 1-click upload to Overleaf, arXiv, or medRxiv.
"""

import shutil
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
LATEX_DIR = REPO_ROOT / "docs/latex"
IMAGES_DIR = REPO_ROOT / "docs/images"
OUTPUT_ZIP = LATEX_DIR / "dlsm_preprint_package.zip"
ARTIFACTS_ZIP = REPO_ROOT / "artifacts/reports/dlsm_preprint_package.zip"

def create_preprint_package():
    print(f"Creating DLSM Preprint Submission Package...")
    
    # Target in-memory or temporary folder
    pkg_temp = REPO_ROOT / "artifacts/reports/preprint_bundle_temp"
    pkg_temp.mkdir(parents=True, exist_ok=True)
    fig_dir = pkg_temp / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)

    # Copy TeX source & BibTeX
    shutil.copy2(LATEX_DIR / "manuscript.tex", pkg_temp / "main.tex")
    shutil.copy2(LATEX_DIR / "manuscript.tex", pkg_temp / "manuscript.tex")
    shutil.copy2(LATEX_DIR / "references.bib", pkg_temp / "references.bib")

    # Copy high-res figures
    if IMAGES_DIR.exists():
        for fig in IMAGES_DIR.glob("*.png"):
            shutil.copy2(fig, fig_dir / fig.name)
            print(f"  Copied figure: {fig.name}")

    # Create Overleaf / arXiv README instructions
    readme_content = """# DLSM Academic Preprint Submission Package

## Package Contents
- `main.tex` / `manuscript.tex`: Two-column IEEE/Nature-styled LaTeX manuscript source.
- `references.bib`: BibTeX citations including literature benchmark calibrations.
- `figures/`: High-resolution figures and dashboard telemetry screenshots.

## How to Compile on Overleaf (1-Click)
1. Go to [https://www.overleaf.com](https://www.overleaf.com) and log in.
2. Click **New Project** -> **Upload Project**.
3. Select this `dlsm_preprint_package.zip` file.
4. Overleaf will automatically detect `main.tex` and compile the full publication PDF with bibliography and formulas in seconds!

## How to Submit to arXiv / medRxiv / TechRxiv
1. This package adheres to standard arXiv automated TeX submission formats.
2. Upload this ZIP or its contents directly to the arXiv / medRxiv submission portal.
"""
    with open(pkg_temp / "README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)

    # Build ZIP archive
    for target in [OUTPUT_ZIP, ARTIFACTS_ZIP]:
        target.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as zipf:
            for file_path in pkg_temp.rglob("*"):
                if file_path.is_file():
                    arcname = file_path.relative_to(pkg_temp)
                    zipf.write(file_path, arcname)
        print(f"Preprint package successfully created at: {target}")

    # Clean temporary directory
    shutil.rmtree(pkg_temp, ignore_errors=True)
    print("Preprint bundle complete!")

if __name__ == "__main__":
    create_preprint_package()
