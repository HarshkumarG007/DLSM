import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import json
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from dlsm.utils.helpers import setup_logger, load_json

logger = setup_logger("dlsm.visualization.figures")

def generate_research_figures():
    Path("artifacts/figures").mkdir(parents=True, exist_ok=True)
    
    # 1. Latent DLL Loadings Comparison Figure
    dll_data = load_json("artifacts/metrics/dll_latent_analysis.json")
    
    # Dataset A Loadings
    loadings_a = dll_data["dataset_a"]["loadings"]["PC1"]
    df_load_a = pd.DataFrame({
        "Feature": list(loadings_a.keys()),
        "PC1 Loading": list(loadings_a.values()),
        "Dataset": "Dataset A (Bedtime Telemetry)"
    })
    
    # Dataset B Loadings
    loadings_b = dll_data["dataset_b"]["loadings"]["PC1"]
    df_load_b = pd.DataFrame({
        "Feature": list(loadings_b.keys()),
        "PC1 Loading": list(loadings_b.values()),
        "Dataset": "Dataset B (Student Digital Life)"
    })
    
    fig_loadings = go.Figure()
    fig_loadings.add_trace(go.Bar(
        x=df_load_a["PC1 Loading"],
        y=df_load_a["Feature"],
        orientation="h",
        name="Dataset A (Bedtime Load)",
        marker_color="#3b82f6"
    ))
    fig_loadings.add_trace(go.Bar(
        x=df_load_b["PC1 Loading"],
        y=df_load_b["Feature"],
        orientation="h",
        name="Dataset B (Student Dual Load)",
        marker_color="#10b981"
    ))
    fig_loadings.update_layout(
        title="Latent Digital Lifestyle Load (DLL): Principal Component Loadings",
        xaxis_title="Standardized Loading (PC1)",
        yaxis_title="Observed / Engineered Digital Feature",
        barmode="group",
        template="plotly_white",
        height=500
    )
    fig_loadings.write_html("artifacts/figures/fig1_dll_loadings.html")
    
    # 2. Feature Ablation Progression Comparison Figure
    ablation_a = pd.read_csv("artifacts/metrics/ablation_regression_dataset_a.csv")
    ablation_b = pd.read_csv("artifacts/metrics/ablation_regression_dataset_b.csv")
    
    fig_ablation = go.Figure()
    
    for m in ["ridge", "random_forest", "xgboost"]:
        sub_a = ablation_a[ablation_a["model"] == m]
        fig_ablation.add_trace(go.Scatter(
            x=sub_a["experiment"],
            y=sub_a["r2_mean"],
            mode="lines+markers",
            name=f"Dataset A (Fatigue) - {m.upper()}",
            line=dict(dash="solid" if m == "xgboost" else "dash")
        ))
        
    for m in ["ridge", "random_forest", "xgboost"]:
        sub_b = ablation_b[ablation_b["model"] == m]
        fig_ablation.add_trace(go.Scatter(
            x=sub_b["experiment"],
            y=sub_b["r2_mean"],
            mode="lines+markers",
            name=f"Dataset B (Mental Health) - {m.upper()}",
            line=dict(dash="dot" if m == "xgboost" else "dashdot")
        ))
        
    fig_ablation.update_layout(
        title="Feature Ablation Study: Predictive Performance (R²) across Experimental Tiers",
        xaxis_title="Experimental Feature Tier",
        yaxis_title="5-Fold Cross-Validation R² Score",
        template="plotly_white",
        height=500
    )
    fig_ablation.write_html("artifacts/figures/fig2_ablation_performance.html")

    # 3. SHAP Relative Attribution Figure
    shap_a = pd.read_csv("artifacts/shap/shap_importance_dataset_a.csv").head(8)
    shap_b = pd.read_csv("artifacts/shap/shap_importance_dataset_b.csv").head(8)
    
    fig_shap_a = px.bar(
        shap_a,
        x="relative_attribution_pct",
        y="feature",
        orientation="h",
        title="Dataset A: Top SHAP Attributions for Next-Day Fatigue",
        labels={"relative_attribution_pct": "Relative Attribution (%)", "feature": "Feature"},
        template="plotly_white",
        color="relative_attribution_pct",
        color_continuous_scale="Blues"
    )
    fig_shap_a.update_layout(yaxis=dict(autorange="reversed"), height=400)
    fig_shap_a.write_html("artifacts/figures/fig3_shap_dataset_a.html")

    fig_shap_b = px.bar(
        shap_b,
        x="relative_attribution_pct",
        y="feature",
        orientation="h",
        title="Dataset B: Top SHAP Attributions for Student Mental Health",
        labels={"relative_attribution_pct": "Relative Attribution (%)", "feature": "Feature"},
        template="plotly_white",
        color="relative_attribution_pct",
        color_continuous_scale="Viridis"
    )
    fig_shap_b.update_layout(yaxis=dict(autorange="reversed"), height=400)
    fig_shap_b.write_html("artifacts/figures/fig4_shap_dataset_b.html")
    
    logger.info("Interactive Plotly research figures saved to artifacts/figures/")

if __name__ == "__main__":
    generate_research_figures()
