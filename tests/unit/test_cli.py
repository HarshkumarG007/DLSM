import os
import subprocess
import sys
from pathlib import Path
import pandas as pd
import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = REPO_ROOT / "src"

def _run_cli(args):
    cmd = [sys.executable, "-m", "dlsm.cli"] + args
    env = dict(os.environ, PYTHONPATH=str(SRC_DIR))
    res = subprocess.run(cmd, cwd=str(REPO_ROOT), env=env, capture_output=True, text=True)
    return res

def test_cli_help():
    res = _run_cli(["--help"])
    assert res.returncode == 0, f"CLI help failed: {res.stderr}"
    assert "score" in res.stdout
    assert "simulate" in res.stdout

def test_cli_score_cohort_b(tmp_path):
    test_csv = tmp_path / "cohort_b_test.csv"
    out_csv = tmp_path / "cohort_b_scored.csv"
    
    # Create sample data
    df = pd.DataFrame([{
        "Student_ID": "TEST_001",
        "Age": 21,
        "Gender": "Male",
        "Education_Level": "University",
        "Daily_Social_Media_Hours": 4.0,
        "Daily_AI_Tool_Usage_Hours": 2.0,
        "Sleep_Hours": 7.0,
        "Physical_Activity_Hours": 1.5,
        "Physical_Health_Score": 85.0
    }])
    df.to_csv(test_csv, index=False)
    
    res = _run_cli([
        "score",
        "--cohort", "b",
        "--input", str(test_csv),
        "--output", str(out_csv)
    ])
    assert res.returncode == 0, f"CLI score failed: {res.stderr}"
    assert out_csv.exists()
    
    df_out = pd.read_csv(out_csv)
    assert "predicted_mental_health_score" in df_out.columns
    assert "assigned_phenotype" in df_out.columns
    assert len(df_out) == 1

def test_cli_simulate(tmp_path):
    out_csv = tmp_path / "sim_output.csv"
    res = _run_cli([
        "simulate",
        "--weeks", "8",
        "--shield",
        "--output", str(out_csv)
    ])
    assert res.returncode == 0, f"CLI simulate failed: {res.stderr}"
    assert out_csv.exists()
    
    df_sim = pd.read_csv(out_csv)
    assert len(df_sim) == 8
    assert "Cumulative_Sleep_Debt_Hours" in df_sim.columns
