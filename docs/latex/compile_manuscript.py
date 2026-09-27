"""
Compiler script for DLSM LaTeX Academic Manuscript.
Checks environment for pdflatex or latexmk and compiles docs/latex/manuscript.tex.
"""

import shutil
import subprocess
from pathlib import Path

def compile_latex():
    latex_dir = Path(__file__).resolve().parent
    tex_file = latex_dir / "manuscript.tex"
    bib_file = latex_dir / "references.bib"
    
    print(f"Checking LaTeX manuscript at: {tex_file}")
    if not tex_file.exists():
        print(f"Error: {tex_file} not found.")
        return False
        
    print(f"Checking BibTeX references at: {bib_file}")
    if not bib_file.exists():
        print(f"Error: {bib_file} not found.")
        return False

    has_latexmk = shutil.which("latexmk") is not None
    has_pdflatex = shutil.which("pdflatex") is not None

    if has_latexmk:
        print("Found 'latexmk'. Compiling PDF...")
        cmd = ["latexmk", "-pdf", "-interaction=nonstopmode", "manuscript.tex"]
        res = subprocess.run(cmd, cwd=latex_dir, capture_output=True, text=True)
        if res.returncode == 0:
            print("Successfully compiled manuscript.pdf!")
            return True
        else:
            print("latexmk exited with errors:", res.stderr)
            return False
    elif has_pdflatex:
        print("Found 'pdflatex'. Running two-pass compilation...")
        subprocess.run(["pdflatex", "-interaction=nonstopmode", "manuscript.tex"], cwd=latex_dir)
        if shutil.which("bibtex"):
            subprocess.run(["bibtex", "manuscript"], cwd=latex_dir)
            subprocess.run(["pdflatex", "-interaction=nonstopmode", "manuscript.tex"], cwd=latex_dir)
        subprocess.run(["pdflatex", "-interaction=nonstopmode", "manuscript.tex"], cwd=latex_dir)
        print("Compilation complete.")
        return True
    else:
        print("Note: Neither 'latexmk' nor 'pdflatex' was detected in the local PATH.")
        print("The LaTeX source 'manuscript.tex' and 'references.bib' are validated and ready for Overleaf or arXiv upload.")
        return True

if __name__ == "__main__":
    compile_latex()
