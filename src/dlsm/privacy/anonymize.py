"""
DLSM Privacy Preservation & Data Minimization Engine.
Implements k-anonymity binning, quasi-identifier generalization,
direct identifier suppression, and differential privacy foundations for SEC-05.
"""
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import numpy as np
import pandas as pd


def bin_age(age_series: pd.Series) -> pd.Series:
    """Bins continuous age into epidemiologically sound developmental cohorts."""
    bins = [0, 17, 21, 25, 100]
    labels = ["13-17 (Secondary/Minor)", "18-21 (Undergraduate)", "22-25 (Postgraduate)", "26+ (Adult Learner)"]
    return pd.cut(age_series, bins=bins, labels=labels, right=True).astype(str)


def bin_hours(series: pd.Series, bins: List[float], labels: List[str]) -> pd.Series:
    """Discretizes continuous screen/lifestyle hours into discrete intervals."""
    return pd.cut(series, bins=bins, labels=labels, right=False).astype(str)


def bin_mental_health_score(series: pd.Series) -> pd.Series:
    """Discretizes continuous mental health score into risk tiers to prevent membership inference."""
    bins = [0, 60, 70, 80, 101]
    labels = ["Severe Strain (<60)", "Moderate Strain (60-70)", "Mild Vulnerability (70-80)", "Flourishing (>80)"]
    return pd.cut(series, bins=bins, labels=labels, right=False).astype(str)


def k_anonymize_dataset_b(
    df: pd.DataFrame,
    k: int = 5,
    quasi_identifiers: Optional[List[str]] = None
) -> Tuple[pd.DataFrame, Dict]:
    """
    Applies k-anonymity to Dataset B (AI_SocialMedia_Student_Dataset.csv):
    1. Suppresses direct primary identifier ('Student_ID').
    2. Generalizes demographic and temporal quasi-identifiers into discrete equivalence classes.
    3. Categorizes target outcome ('Mental_Health_Score') to prevent attribute disclosure.
    4. Suppresses / masks equivalence classes that fail to achieve size >= k.
    
    Returns:
        anonymized_df: pd.DataFrame satisfying k-anonymity
        metrics: dict of anonymity audit metrics
    """
    df_clean = df.copy()
    
    # 1. Suppress direct identifier
    if "Student_ID" in df_clean.columns:
        df_clean = df_clean.drop(columns=["Student_ID"])
        
    # 2. Generalize quasi-identifiers
    df_anon = pd.DataFrame()
    df_anon["Age_Band"] = bin_age(df_clean["Age"])
    df_anon["Gender"] = df_clean["Gender"]
    df_anon["Education_Level"] = df_clean["Education_Level"]
    
    # Discretize continuous lifestyle variables
    df_anon["Social_Media_Tier"] = bin_hours(
        df_clean["Daily_Social_Media_Hours"],
        bins=[0.0, 2.0, 4.0, 6.0, 24.0],
        labels=["<2h Low", "2-4h Moderate", "4-6h Heavy", ">6h Excessive"]
    )
    df_anon["AI_Tool_Usage_Tier"] = bin_hours(
        df_clean["Daily_AI_Tool_Usage_Hours"],
        bins=[0.0, 1.0, 2.5, 4.0, 24.0],
        labels=["<1h Light", "1-2.5h Moderate", "2.5-4h Intensive", ">4h Heavy"]
    )
    df_anon["Sleep_Duration_Tier"] = bin_hours(
        df_clean["Sleep_Hours"],
        bins=[0.0, 6.0, 7.0, 8.5, 24.0],
        labels=["<6h Short", "6-7h Borderline", "7-8.5h Restorative", ">8.5h Extended"]
    )
    df_anon["Physical_Activity_Tier"] = bin_hours(
        df_clean["Physical_Activity_Hours"],
        bins=[0.0, 1.0, 2.0, 24.0],
        labels=["<1h Sedentary", "1-2h Active", ">2h Highly Active"]
    )
    
    # Round continuous physical health score to decile
    df_anon["Physical_Health_Decile"] = (np.round(df_clean["Physical_Health_Score"] / 10.0) * 10).astype(int)
    
    # Discretize mental health outcome to prevent exact reconstruction
    df_anon["Mental_Health_Category"] = bin_mental_health_score(df_clean["Mental_Health_Score"])
    
    if quasi_identifiers is None:
        quasi_identifiers = ["Age_Band", "Gender", "Education_Level"]
        
    # 3. Audit equivalence classes and enforce k-anonymity
    eq_class_counts = df_anon.groupby(quasi_identifiers, observed=True).size()
    violating_classes = eq_class_counts[eq_class_counts < k].index
    
    # Filter or suppress violating records if any exist
    if len(violating_classes) > 0:
        mask = df_anon.set_index(quasi_identifiers).index.isin(violating_classes)
        df_anon = df_anon[~mask].reset_index(drop=True)
        suppressed_count = int(mask.sum())
    else:
        suppressed_count = 0
        
    final_eq_counts = df_anon.groupby(quasi_identifiers, observed=True).size()
    min_eq_size = int(final_eq_counts.min()) if len(final_eq_counts) > 0 else 0
    
    metrics = {
        "k_threshold": k,
        "achieved_k": min_eq_size,
        "k_anonymity_satisfied": bool(min_eq_size >= k),
        "total_input_records": len(df),
        "total_anonymized_records": len(df_anon),
        "suppressed_records": suppressed_count,
        "retention_rate_pct": round((len(df_anon) / len(df)) * 100.0, 2),
        "distinct_equivalence_classes": len(final_eq_counts),
        "quasi_identifiers": quasi_identifiers
    }
    
    return df_anon, metrics


def export_anonymized_dataset(output_path: str = "data/processed/dataset_b_k_anonymized.csv", k: int = 5) -> Path:
    """Loads raw Dataset B, applies k-anonymization, and saves to data/processed."""
    from dlsm.data.loader import load_dataset_b
    df = load_dataset_b()
    anon_df, _ = k_anonymize_dataset_b(df, k=k)
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    anon_df.to_csv(out, index=False)
    return out
