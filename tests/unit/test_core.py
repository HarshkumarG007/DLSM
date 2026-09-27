import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "src"))

import pytest
import pandas as pd
import numpy as np
from dlsm.validation.schemas import validate_dataset_a, validate_dataset_b
from dlsm.features.engineer import DatasetAFeatureEngineer, DatasetBFeatureEngineer
from dlsm.latent.dll import LatentDLLExtractor
from dlsm.statistics.mediation import StatisticalMediation
from dlsm.models.pipeline import build_preprocessing_pipeline

def test_dataset_a_schema_validation():
    # Synthetic mini-sample matching Dataset A schema
    df = pd.DataFrame({
        "user_id": ["USR-01", "USR-02"],
        "age": [25, 40],
        "gender": ["Female", "Male"],
        "occupation_type": ["Student", "Remote Tech"],
        "chronotype": ["Intermediate", "Night Owl"],
        "bedtime_phone_minutes": [60, 120],
        "primary_bedtime_app": ["YouTube", "TikTok / Reels"],
        "screen_brightness_pct": [50, 80],
        "blue_light_filter_active": [1, 0],
        "caffeine_post_5pm_mg": [0, 50],
        "physical_activity_min": [30, 45],
        "sleep_latency_min": [20.5, 45.0],
        "total_sleep_hours": [7.0, 5.5],
        "deep_sleep_pct": [22.0, 18.0],
        "rem_sleep_pct": [20.0, 17.5],
        "morning_alarm_snoozes": [1, 3],
        "next_day_fatigue_score": [3.5, 7.2],
        "sleep_debt_category": ["Mild Deficit", "Moderate Debt"]
    })
    validated = validate_dataset_a(df)
    assert len(validated) == 2

def test_feature_engineering_dataset_a():
    df = pd.DataFrame({
        "screen_brightness_pct": [100, 50],
        "bedtime_phone_minutes": [60, 30],
        "blue_light_filter_active": [0, 1],
        "total_sleep_hours": [6.0, 7.5],
        "deep_sleep_pct": [20.0, 25.0],
        "rem_sleep_pct": [20.0, 20.0],
        "primary_bedtime_app": ["TikTok / Reels", "News / Reading"],
        "sleep_latency_min": [30.0, 15.0],
        "caffeine_post_5pm_mg": [50, 0]
    })
    fe = DatasetAFeatureEngineer(include_interactions=True)
    df_trans = fe.transform(df)
    
    assert "bedtime_intensity_index" in df_trans.columns
    assert "screen_to_sleep_ratio" in df_trans.columns
    assert "sleep_architecture_efficiency" in df_trans.columns
    
    # Check formula without filter: (100/100) * 60 * (1 - 0) = 60.0
    assert np.isclose(df_trans["bedtime_intensity_index"].iloc[0], 60.0)
    # Check sleep architecture: (20 + 20) / 100 = 0.40
    assert np.isclose(df_trans["sleep_architecture_efficiency"].iloc[0], 0.40)

def test_feature_engineering_dataset_b():
    df = pd.DataFrame({
        "Daily_Social_Media_Hours": [4.0, 2.0],
        "Daily_AI_Tool_Usage_Hours": [2.0, 1.0],
        "Sleep_Hours": [6.0, 8.0],
        "Physical_Activity_Hours": [1.0, 2.0]
    })
    fe = DatasetBFeatureEngineer(include_interactions=True)
    df_trans = fe.transform(df)
    
    assert "total_digital_hours" in df_trans.columns
    assert "digital_composition_ratio" in df_trans.columns
    assert "active_buffer_ratio" in df_trans.columns
    
    # Check total digital: 4 + 2 = 6.0
    assert np.isclose(df_trans["total_digital_hours"].iloc[0], 6.0)
    # Check composition: 2 / 6 = 0.3333
    assert np.isclose(df_trans["digital_composition_ratio"].iloc[0], 2.0 / 6.0, atol=1e-3)

def test_latent_dll_extractor():
    rng = np.random.RandomState(42)
    n = 100
    x1 = rng.normal(0, 1, n)
    x2 = 0.8 * x1 + rng.normal(0, 0.2, n)
    x3 = 0.7 * x1 + rng.normal(0, 0.3, n)
    
    df = pd.DataFrame({"feat1": x1, "feat2": x2, "feat3": x3})
    extractor = LatentDLLExtractor(digital_feature_cols=["feat1", "feat2", "feat3"], n_components=1)
    extractor.fit(df)
    df_trans = extractor.transform(df)
    
    assert "digital_lifestyle_load" in df_trans.columns
    assert extractor.explained_variance_ratio_[0] > 0.70
    assert extractor.loadings_["PC1"].min() > 0  # Orientated positively

def test_statistical_mediation():
    rng = np.random.RandomState(42)
    n = 300
    # Simulate true mediation: X -> M -> Y
    x = rng.normal(0, 1, n)
    m = 0.6 * x + rng.normal(0, 0.5, n)
    y = 0.5 * m + 0.2 * x + rng.normal(0, 0.5, n)
    
    df = pd.DataFrame({"X": x, "M": m, "Y": y})
    med = StatisticalMediation(n_bootstraps=500, random_state=42)
    res = med.fit(df, x_col="X", m_col="M", y_col="Y")
    
    assert res["statistically_significant"] is True
    assert res["indirect_effect_ab"] > 0
    assert res["bootstrap_ci_95"][0] > 0

def test_no_pipeline_leakage():
    # Verify that pipeline strictly isolates train and test statistics
    num_cols = ["x1", "x2"]
    cat_cols = ["c1"]
    
    df_train = pd.DataFrame({"x1": [1.0, 2.0, 3.0], "x2": [10.0, 20.0, 30.0], "c1": ["A", "B", "A"]})
    df_test = pd.DataFrame({"x1": [100.0], "x2": [1000.0], "c1": ["A"]})
    
    pipeline = build_preprocessing_pipeline(num_cols, cat_cols)
    train_proc = pipeline.fit_transform(df_train)
    test_proc = pipeline.transform(df_test)
    
    # Train mean of x1 is 2.0, std is sqrt(2/3)=0.816. Test x1=100 scaled with train mean/std:
    expected_scaled_x1 = (100.0 - 2.0) / np.std([1.0, 2.0, 3.0])
    assert np.isclose(test_proc[0, 0], expected_scaled_x1, atol=1e-3)

def test_executive_report_generation():
    from dlsm.utils.report_generator import generate_executive_report_markdown, generate_executive_report_html
    project_root = Path(__file__).resolve().parent.parent.parent
    md = generate_executive_report_markdown(project_root)
    html = generate_executive_report_html(md)
    
    assert len(md) > 1000
    assert "Executive Research Report" in md
    assert "Digital Lifestyle Spillover Model" in md
    assert len(html) > 2000
    assert "<!DOCTYPE html>" in html

def test_longitudinal_panel_simulator():
    from dlsm.simulation.longitudinal import LongitudinalPanelSimulator
    sim = LongitudinalPanelSimulator(weeks=16, random_state=42)
    df = sim.simulate_semester()
    assert len(df) == 16
    assert "Cumulative_Sleep_Debt_Hours" in df.columns
    assert "Predicted_Fatigue" in df.columns
    assert "Risk_Status" in df.columns
    assert (df["Cumulative_Sleep_Debt_Hours"] >= 0).all()

def test_optuna_trials_ledger():
    import json
    from pathlib import Path
    opt_path = Path(__file__).resolve().parent.parent.parent / "artifacts" / "metrics" / "optuna_trials.json"
    assert opt_path.exists()
    with open(opt_path, "r") as f:
        data = json.load(f)
    assert "cohort_a_fatigue_xgb" in data
    assert "cohort_b_mental_xgb" in data
    assert len(data["cohort_a_fatigue_xgb"]["trials"]) >= 30
    assert any(t["is_pareto"] for t in data["cohort_a_fatigue_xgb"]["trials"])

