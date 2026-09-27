import subprocess
import sys
from pathlib import Path
import pandas as pd
import pytest

def test_cli_help():
    cmd = [sys.executable, "-m", "dlsm.cli", "--help"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    assert res.returncode == 0
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
    
    cmd = [
        sys.executable, "-m", "dlsm.cli", "score",
        "--cohort", "b",
        "--input", str(test_csv),
        "--output", str(out_csv)
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    assert res.returncode == 0
    assert out_csv.exists()
    
    df_out = pd.read_csv(out_csv)
    assert "predicted_mental_health_score" in df_out.columns
    assert "assigned_phenotype" in df_out.columns
    assert len(df_out) == 1

def test_cli_simulate(tmp_path):
    out_csv = tmp_path / "sim_output.csv"
    cmd = [
        sys.executable, "-m", "dlsm.cli", "simulate",
        "--weeks", "8",
        "--shield",
        "--output", str(out_csv)
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    assert res.returncode == 0
    assert out_csv.exists()
    
    df_sim = pd.read_csv(out_csv)
    assert len(df_sim) == 8
    assert "Cumulative_Sleep_Debt_Hours" in df_sim.columns
