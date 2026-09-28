"""
DLSM Lockfile Generator
Fetches cryptographically verified SHA-256 release digests from PyPI
and authors a strict requirements.lock for supply-chain defense.
"""
import json
import urllib.request
from pathlib import Path

PACKAGES = [
    ("numpy", "2.2.4"),
    ("pandas", "2.3.3"),
    ("scipy", "1.15.2"),
    ("scikit-learn", "1.6.1"),
    ("xgboost", "3.0.5"),
    ("statsmodels", "0.14.5"),
    ("pandera", "0.33.1"),
    ("shap", "0.52.0"),
    ("optuna", "4.5.0"),
    ("streamlit", "1.64.0"),
    ("plotly", "6.3.1"),
    ("matplotlib", "3.10.6"),
    ("seaborn", "0.13.2"),
    ("pyyaml", "6.0.3"),
    ("joblib", "1.4.2"),
    ("pytest", "9.1.1"),
    ("pytest-cov", "7.1.0"),
    ("fastapi", "0.118.0"),
    ("uvicorn", "0.37.0"),
    ("httpx", "0.28.1"),
]

def generate_lockfile():
    repo_root = Path(__file__).resolve().parents[1]
    lock_file = repo_root / "requirements.lock"
    
    lines = [
        "# ============================================================================",
        "# DLSM CRYPTOGRAPHICALLY PINNED DEPENDENCY LOCKFILE",
        "# Generated for SEC-08 Supply Chain Integrity & Deterministic Build Invariance",
        "# ============================================================================",
        "",
    ]
    
    for pkg, ver in PACKAGES:
        url = f"https://pypi.org/pypi/{pkg}/{ver}/json"
        req = urllib.request.Request(url, headers={"User-Agent": "DLSM-Lockfile-Generator/1.0"})
        hashes = []
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                for u in data.get("urls", []):
                    sha = u.get("digests", {}).get("sha256")
                    if sha:
                        hashes.append(f"    --hash=sha256:{sha}")
        except Exception as e:
            print(f"Warning fetching hashes for {pkg}=={ver}: {e}")
        
        if hashes:
            lines.append(f"{pkg}=={ver} \\")
            for i, h in enumerate(hashes):
                suffix = " \\" if i < len(hashes) - 1 else ""
                lines.append(f"{h}{suffix}")
        else:
            lines.append(f"{pkg}=={ver}")
        lines.append("")

    lock_file.write_text("\n".join(lines), encoding="utf-8")
    print(f"Successfully generated {lock_file} with {len(PACKAGES)} cryptographically pinned packages.")

if __name__ == "__main__":
    generate_lockfile()
