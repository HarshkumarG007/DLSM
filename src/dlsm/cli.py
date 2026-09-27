"""
Command-Line Interface (CLI) for DLSM.
Enables headless batch scoring of student cohorts, longitudinal policy simulation,
and dataset schema auditing without launching the web GUI.
"""

import argparse
import json
import sys
from pathlib import Path
import pandas as pd
import joblib

from dlsm.features.engineer import DatasetAFeatureEngineer, DatasetBFeatureEngineer
from dlsm.simulation.longitudinal import LongitudinalPanelSimulator
from dlsm.utils.helpers import setup_logger

logger = setup_logger("dlsm.cli")
PROJECT_ROOT = Path(__file__).resolve().parents[2]
MODELS_DIR = PROJECT_ROOT / "artifacts/models"

def _load_or_fit_prep_a(fe_a, dll_a):
    try:
        return joblib.load(MODELS_DIR / "preprocessor_dataset_a.pkl")
    except Exception:
        from dlsm.data.loader import load_dataset_a
        from dlsm.models.pipeline import build_preprocessing_pipeline
        df = load_dataset_a()
        df_eng = fe_a.transform(df)
        df_full = dll_a.transform(df_eng)
        num_cols = [
            "age", "bedtime_phone_minutes", "screen_brightness_pct", "blue_light_filter_active",
            "caffeine_post_5pm_mg", "physical_activity_min", "sleep_latency_min",
            "total_sleep_hours", "deep_sleep_pct", "rem_sleep_pct", "morning_alarm_snoozes",
            "bedtime_intensity_index", "screen_to_sleep_ratio", "sleep_architecture_efficiency",
            "cognitive_arousal_weight", "arousal_weighted_bedtime_exposure", "sleep_latency_ratio",
            "caffeine_screen_interaction", "brightness_screen_interaction", "screen_sleep_interaction",
            "digital_lifestyle_load"
        ]
        cat_cols = ["gender", "occupation_type", "chronotype", "primary_bedtime_app"]
        prep = build_preprocessing_pipeline(num_cols, cat_cols)
        prep.fit(df_full)
        return prep

def _load_or_fit_prep_b(fe_b, dll_b):
    try:
        return joblib.load(MODELS_DIR / "preprocessor_dataset_b.pkl")
    except Exception:
        from dlsm.data.loader import load_dataset_b
        from dlsm.models.pipeline import build_preprocessing_pipeline
        df = load_dataset_b()
        df_eng = fe_b.transform(df)
        df_full = dll_b.transform(df_eng)
        num_cols = [
            "Age", "Daily_Social_Media_Hours", "Daily_AI_Tool_Usage_Hours", "Sleep_Hours",
            "Physical_Activity_Hours", "total_digital_hours", "digital_composition_ratio",
            "screen_to_sleep_ratio", "active_buffer_ratio", "sleep_deficit_hours",
            "social_sleep_interaction", "ai_sleep_interaction", "social_physical_interaction",
            "digital_lifestyle_load"
        ]
        cat_cols = ["Gender", "Education_Level"]
        prep = build_preprocessing_pipeline(num_cols, cat_cols)
        prep.fit(df_full)
        return prep

def score_cohort_a(input_path: Path, output_path: Path):
    logger.info(f"Loading input data for Cohort A from {input_path}")
    df = pd.read_csv(input_path)
    
    fe = DatasetAFeatureEngineer()
    df_eng = fe.transform(df)
    
    dll = joblib.load(MODELS_DIR / "dll_extractor_a.pkl")
    df_full = dll.transform(df_eng)
    
    prep = _load_or_fit_prep_a(fe, dll)
    model = joblib.load(MODELS_DIR / "xgb_fatigue_model_dataset_a.pkl")
    
    X_mat = prep.transform(df_full)
    df["predicted_fatigue_score"] = model.predict(X_mat).round(2)
    df["bedtime_intensity_index"] = df_eng["bedtime_intensity_index"].round(2)
    df["screen_to_sleep_ratio"] = df_eng["screen_to_sleep_ratio"].round(2)
    df["digital_lifestyle_load"] = df_full["digital_lifestyle_load"].round(2)
    df["assigned_phenotype"] = df["digital_lifestyle_load"].apply(
        lambda x: "High-Load Nocturnally Disrupted" if x > 0 else "Regulated Circadian Restorative"
    )
    df["fatigue_risk_tier"] = df["predicted_fatigue_score"].apply(
        lambda x: "High Risk" if x >= 6.0 else ("Moderate Risk" if x >= 4.0 else "Low Risk")
    )
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    logger.info(f"Batch scoring complete. Scored {len(df)} records saved to {output_path}")
    print(f"[SUCCESS] Scored {len(df)} Cohort A records. Saved to: {output_path}")

def score_cohort_b(input_path: Path, output_path: Path):
    logger.info(f"Loading input data for Cohort B from {input_path}")
    df = pd.read_csv(input_path)
    
    fe = DatasetBFeatureEngineer()
    df_eng = fe.transform(df)
    
    dll = joblib.load(MODELS_DIR / "dll_extractor_b.pkl")
    df_full = dll.transform(df_eng)
    
    prep = _load_or_fit_prep_b(fe, dll)
    model = joblib.load(MODELS_DIR / "xgb_mental_health_model_dataset_b.pkl")
    
    X_mat = prep.transform(df_full)
    df["predicted_mental_health_score"] = model.predict(X_mat).round(2)
    df["total_digital_hours"] = df_eng["total_digital_hours"].round(2)
    df["screen_to_sleep_ratio"] = df_eng["screen_to_sleep_ratio"].round(2)
    df["active_buffer_ratio"] = df_eng["active_buffer_ratio"].round(2)
    df["digital_lifestyle_load"] = df_full["digital_lifestyle_load"].round(2)
    df["assigned_phenotype"] = df["digital_lifestyle_load"].apply(
        lambda x: "Intensive Dual-Screen Load" if x > 0 else "Balanced Digital Moderates"
    )
    df["mental_health_risk_tier"] = df["predicted_mental_health_score"].apply(
        lambda x: "High Risk / Strain" if x < 68.0 else ("Moderate Risk" if x < 76.0 else "Low Risk / Flourishing")
    )
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    logger.info(f"Batch scoring complete. Scored {len(df)} records saved to {output_path}")
    print(f"[SUCCESS] Scored {len(df)} Cohort B records. Saved to: {output_path}")

def run_simulation(weeks: int, shield: bool, multiplier: float, output_path: Path):
    sim = LongitudinalPanelSimulator(weeks=weeks, random_state=42)
    if shield:
        df_sim = sim.simulate_semester(
            baseline_social_hours=3.0,
            baseline_ai_hours=2.0,
            baseline_bedtime_min=30,
            baseline_sleep_hours=7.5,
            baseline_activity_hours=1.8,
            blue_light_filter=True,
            exam_intensity_multiplier=multiplier
        )
    else:
        df_sim = sim.simulate_semester(
            baseline_social_hours=5.0,
            baseline_ai_hours=2.8,
            baseline_bedtime_min=75,
            baseline_sleep_hours=6.2,
            baseline_activity_hours=1.0,
            blue_light_filter=False,
            exam_intensity_multiplier=multiplier
        )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df_sim.to_csv(output_path, index=False)
    final_debt = df_sim["Cumulative_Sleep_Debt_Hours"].iloc[-1]
    print(f"[SUCCESS] Simulation complete ({weeks} weeks). Final sleep debt: {final_debt:.1f} hrs. Saved to: {output_path}")

def main():
    parser = argparse.ArgumentParser(
        prog="dlsm",
        description="Digital Lifestyle Spillover Model (DLSM) Batch Scoring & Simulation CLI"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Score subcommand
    score_parser = subparsers.add_parser("score", help="Batch score a CSV cohort file")
    score_parser.add_argument("--cohort", choices=["a", "b"], required=True, help="Cohort type (a: Bedtime Telemetry, b: Student Life)")
    score_parser.add_argument("--input", type=str, required=True, help="Path to input raw CSV file")
    score_parser.add_argument("--output", type=str, required=True, help="Path to save scored CSV file")

    # Simulate subcommand
    sim_parser = subparsers.add_parser("simulate", help="Run 16-week semester longitudinal policy simulation")
    sim_parser.add_argument("--weeks", type=int, default=16, help="Semester duration in weeks")
    sim_parser.add_argument("--shield", action="store_true", help="Apply institutional wellbeing shielding protocol")
    sim_parser.add_argument("--multiplier", type=float, default=1.0, help="Exam stress amplifier multiplier")
    sim_parser.add_argument("--output", type=str, default="artifacts/simulation_cli_output.csv", help="Output path for simulation trajectory")

    args = parser.parse_args()

    if args.command == "score":
        in_p = Path(args.input)
        out_p = Path(args.output)
        if not in_p.exists():
            print(f"[ERROR] Input file {in_p} does not exist.")
            sys.exit(1)
        if args.cohort == "a":
            score_cohort_a(in_p, out_p)
        else:
            score_cohort_b(in_p, out_p)
    elif args.command == "simulate":
        out_p = Path(args.output)
        run_simulation(args.weeks, args.shield, args.multiplier, out_p)

if __name__ == "__main__":
    main()
