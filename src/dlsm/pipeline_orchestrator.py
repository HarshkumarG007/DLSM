import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import json
import numpy as np
import pandas as pd
from dlsm.utils.helpers import setup_logger, set_seed, save_json, save_pickle
from dlsm.data.loader import load_dataset_a, load_dataset_b
from dlsm.validation.schemas import validate_dataset_a, validate_dataset_b
from dlsm.features.engineer import DatasetAFeatureEngineer, DatasetBFeatureEngineer
from dlsm.latent.dll import LatentDLLExtractor
from dlsm.clustering.phenotypes import PhenotypeDiscovery
from dlsm.evaluation.ablation import AblationEvaluator
from dlsm.explainability.shap_analysis import ModelExplainer
from dlsm.statistics.mediation import StatisticalMediation
from dlsm.models.pipeline import build_preprocessing_pipeline, get_regression_model, get_classification_model

logger = setup_logger("dlsm.pipeline")

def run_dlsm_pipeline():
    set_seed(42)
    logger.info("==================================================================")
    logger.info("STARTING DLSM CROSS-DATASET AI/ML RESEARCH EXECUTION PIPELINE")
    logger.info("==================================================================")

    # 1. LOAD AND VALIDATE RAW DATASETS (Phase 0/1)
    logger.info("--- STAGE 1: Loading & Pandera Validation ---")
    df_a_raw = load_dataset_a()
    df_b_raw = load_dataset_b()
    
    validate_dataset_a(df_a_raw)
    validate_dataset_b(df_b_raw)
    logger.info("Pandera schemas validated successfully with 0 missing values.")

    # 2. FEATURE ENGINEERING (Phase 2)
    logger.info("--- STAGE 2: Feature Engineering (Domain & Interactions) ---")
    fe_a = DatasetAFeatureEngineer(include_interactions=True)
    df_a_eng = fe_a.transform(df_a_raw)
    
    fe_b = DatasetBFeatureEngineer(include_interactions=True)
    df_b_eng = fe_b.transform(df_b_raw)
    
    # Create mental health risk classification target in Dataset B (quantiles: low, medium, severe risk)
    df_b_eng["mental_health_risk"] = pd.qcut(
        df_b_eng["Mental_Health_Score"],
        q=[0.0, 0.33, 0.66, 1.0],
        labels=["High Risk / Distress", "Moderate Risk", "Low Risk / Flourishing"]
    ).astype(str)

    # 3. LATENT DIGITAL LIFESTYLE LOAD (DLL) & STABILITY (Phase 3)
    logger.info("--- STAGE 3: Constructing Latent Digital Lifestyle Load (DLL) ---")
    digital_cols_a = [
        "bedtime_phone_minutes",
        "screen_brightness_pct",
        "bedtime_intensity_index",
        "arousal_weighted_bedtime_exposure"
    ]
    dll_extractor_a = LatentDLLExtractor(digital_feature_cols=digital_cols_a, n_components=2, random_state=42)
    dll_extractor_a.fit(df_a_eng)
    df_a_full = dll_extractor_a.transform(df_a_eng)
    dll_stability_a = dll_extractor_a.evaluate_bootstrap_stability(df_a_eng, n_resamples=1000)
    
    digital_cols_b = [
        "Daily_Social_Media_Hours",
        "Daily_AI_Tool_Usage_Hours",
        "total_digital_hours",
        "screen_to_sleep_ratio"
    ]
    dll_extractor_b = LatentDLLExtractor(digital_feature_cols=digital_cols_b, n_components=2, random_state=42)
    dll_extractor_b.fit(df_b_eng)
    df_b_full = dll_extractor_b.transform(df_b_eng)
    dll_stability_b = dll_extractor_b.evaluate_bootstrap_stability(df_b_eng, n_resamples=1000)
    
    # Save Latent DLL artifacts
    save_json({
        "dataset_a": {
            "loadings": dll_extractor_a.loadings_.to_dict(),
            "fa_loadings": dll_extractor_a.fa_loadings_.to_dict() if dll_extractor_a.fa_loadings_ is not None else None,
            "fa_correlation": dll_extractor_a.fa_correlation_,
            "explained_variance_ratio": dll_extractor_a.explained_variance_ratio_.tolist(),
            "stability_metrics": dll_stability_a
        },
        "dataset_b": {
            "loadings": dll_extractor_b.loadings_.to_dict(),
            "fa_loadings": dll_extractor_b.fa_loadings_.to_dict() if dll_extractor_b.fa_loadings_ is not None else None,
            "fa_correlation": dll_extractor_b.fa_correlation_,
            "explained_variance_ratio": dll_extractor_b.explained_variance_ratio_.tolist(),
            "stability_metrics": dll_stability_b
        }
    }, "artifacts/metrics/dll_latent_analysis.json")

    # 4. BEHAVIORAL PHENOTYPE DISCOVERY & CLUSTERING (Phase 4)
    logger.info("--- STAGE 4: Behavioral Phenotype Discovery ---")
    cluster_features_a = [
        "digital_lifestyle_load",
        "total_sleep_hours",
        "sleep_latency_min",
        "deep_sleep_pct",
        "caffeine_post_5pm_mg",
        "physical_activity_min"
    ]
    clustering_a = PhenotypeDiscovery(feature_cols=cluster_features_a, k_range=(2, 5), random_state=42)
    clustering_a.evaluate_k_selection(df_a_full)
    labels_a, profiles_a = clustering_a.fit_predict(df_a_full)
    ari_a = clustering_a.evaluate_cluster_stability(df_a_full, n_resamples=50)
    df_a_full["behavioral_phenotype"] = labels_a
    
    cluster_features_b = [
        "digital_lifestyle_load",
        "Daily_Social_Media_Hours",
        "Daily_AI_Tool_Usage_Hours",
        "Sleep_Hours",
        "Physical_Activity_Hours"
    ]
    clustering_b = PhenotypeDiscovery(feature_cols=cluster_features_b, k_range=(2, 5), random_state=42)
    clustering_b.evaluate_k_selection(df_b_full)
    labels_b, profiles_b = clustering_b.fit_predict(df_b_full)
    ari_b = clustering_b.evaluate_cluster_stability(df_b_full, n_resamples=50)
    df_b_full["behavioral_phenotype"] = labels_b
    
    save_json({
        "dataset_a": {
            "optimal_k": clustering_a.best_k_,
            "k_metrics": clustering_a.k_metrics_,
            "mean_profiles": profiles_a.to_dict(),
            "cluster_stability_ari": ari_a
        },
        "dataset_b": {
            "optimal_k": clustering_b.best_k_,
            "k_metrics": clustering_b.k_metrics_,
            "mean_profiles": profiles_b.to_dict(),
            "cluster_stability_ari": ari_b
        }
    }, "artifacts/metrics/clustering_phenotypes.json")

    # 5. SUPERVISED MODELING & FEATURE ABLATION (Phase 5)
    logger.info("--- STAGE 5: Supervised Modeling & The Central Feature Ablation Study ---")
    evaluator = AblationEvaluator(random_state=42, cv_folds=5)
    
    # Feature sets definitions for Dataset A Regression (next_day_fatigue_score)
    raw_num_a_reg = ["age", "bedtime_phone_minutes", "screen_brightness_pct", "blue_light_filter_active",
                     "caffeine_post_5pm_mg", "physical_activity_min", "sleep_latency_min", "total_sleep_hours",
                     "deep_sleep_pct", "rem_sleep_pct", "morning_alarm_snoozes"]
    raw_cat_a = ["gender", "occupation_type", "chronotype", "primary_bedtime_app"]
    
    eng_num_a_reg = ["bedtime_intensity_index", "screen_to_sleep_ratio", "sleep_architecture_efficiency",
                     "cognitive_arousal_weight", "arousal_weighted_bedtime_exposure", "sleep_latency_ratio"]
    int_num_a_reg = ["caffeine_screen_interaction", "brightness_screen_interaction", "screen_sleep_interaction"]
    dll_num_a = ["digital_lifestyle_load"]
    
    feature_sets_a_reg = {
        "Exp_A_Raw": (raw_num_a_reg, raw_cat_a),
        "Exp_B_Engineered": (raw_num_a_reg + eng_num_a_reg, raw_cat_a),
        "Exp_C_Interactions": (raw_num_a_reg + eng_num_a_reg + int_num_a_reg, raw_cat_a),
        "Exp_D_Full_DLL": (raw_num_a_reg + eng_num_a_reg + int_num_a_reg + dll_num_a, raw_cat_a)
    }

    # Feature sets definitions for Dataset A Classification (sleep_debt_category)
    # CRITICAL METHODOLOGICAL LEAKAGE GUARD:
    # Sleep debt is definitionally derived from total sleep hours.
    # To test whether PRE-SLEEP DIGITAL BEHAVIOR genuinely predicts sleep debt risk,
    # we strictly drop all nocturnal sleep composition columns (total_sleep_hours, deep_sleep_pct,
    # rem_sleep_pct, sleep_latency_min, etc.) preventing circular definitional leakage.
    raw_num_a_clf = ["age", "bedtime_phone_minutes", "screen_brightness_pct", "blue_light_filter_active",
                     "caffeine_post_5pm_mg", "physical_activity_min", "morning_alarm_snoozes"]
    eng_num_a_clf = ["bedtime_intensity_index", "cognitive_arousal_weight", "arousal_weighted_bedtime_exposure"]
    int_num_a_clf = ["caffeine_screen_interaction", "brightness_screen_interaction"]
    
    feature_sets_a_clf = {
        "Exp_A_Raw": (raw_num_a_clf, raw_cat_a),
        "Exp_B_Engineered": (raw_num_a_clf + eng_num_a_clf, raw_cat_a),
        "Exp_C_Interactions": (raw_num_a_clf + eng_num_a_clf + int_num_a_clf, raw_cat_a),
        "Exp_D_Full_DLL": (raw_num_a_clf + eng_num_a_clf + int_num_a_clf + dll_num_a, raw_cat_a)
    }
    
    logger.info("Evaluating Dataset A Regression (next_day_fatigue_score)...")
    reg_results_a = evaluator.evaluate_regression(
        df_a_full, feature_sets_a_reg, target_col="next_day_fatigue_score",
        model_types=["baseline", "ridge", "random_forest", "xgboost"]
    )
    reg_results_a.to_csv("artifacts/metrics/ablation_regression_dataset_a.csv", index=False)
    
    logger.info("Evaluating Dataset A Classification (sleep_debt_category, un-leaked behavioral features)...")
    clf_results_a = evaluator.evaluate_classification(
        df_a_full, feature_sets_a_clf, target_col="sleep_debt_category",
        model_types=["baseline", "logistic", "random_forest", "xgboost"]
    )
    clf_results_a.to_csv("artifacts/metrics/ablation_classification_dataset_a.csv", index=False)
    
    # Feature sets definitions for Dataset B
    raw_num_b = ["Age", "Daily_Social_Media_Hours", "Daily_AI_Tool_Usage_Hours", "Sleep_Hours", "Physical_Activity_Hours"]
    raw_cat_b = ["Gender", "Education_Level"]
    
    eng_num_b = ["total_digital_hours", "digital_composition_ratio", "screen_to_sleep_ratio", "active_buffer_ratio", "sleep_deficit_hours"]
    int_num_b = ["social_sleep_interaction", "ai_sleep_interaction", "social_physical_interaction"]
    dll_num_b = ["digital_lifestyle_load"]
    
    feature_sets_b = {
        "Exp_A_Raw": (raw_num_b, raw_cat_b),
        "Exp_B_Engineered": (raw_num_b + eng_num_b, raw_cat_b),
        "Exp_C_Interactions": (raw_num_b + eng_num_b + int_num_b, raw_cat_b),
        "Exp_D_Full_DLL": (raw_num_b + eng_num_b + int_num_b + dll_num_b, raw_cat_b)
    }
    
    logger.info("Evaluating Dataset B Regression (Mental_Health_Score)...")
    reg_results_b = evaluator.evaluate_regression(
        df_b_full, feature_sets_b, target_col="Mental_Health_Score",
        model_types=["baseline", "ridge", "random_forest", "xgboost"]
    )
    reg_results_b.to_csv("artifacts/metrics/ablation_regression_dataset_b.csv", index=False)
    
    logger.info("Evaluating Dataset B Classification (mental_health_risk)...")
    clf_results_b = evaluator.evaluate_classification(
        df_b_full, feature_sets_b, target_col="mental_health_risk",
        model_types=["baseline", "logistic", "random_forest", "xgboost"]
    )
    clf_results_b.to_csv("artifacts/metrics/ablation_classification_dataset_b.csv", index=False)

    # 6. EXPLAINABILITY & SHAP (Phase 6)
    logger.info("--- STAGE 6: SHAP & Permutation Importance Analysis ---")
    # Fit final representative XGBoost model on Dataset A for fatigue prediction
    num_cols_final_a, cat_cols_final_a = feature_sets_a_reg["Exp_D_Full_DLL"]
    prep_a = build_preprocessing_pipeline(num_cols_final_a, cat_cols_final_a)
    X_a_mat = prep_a.fit_transform(df_a_full)
    y_a = df_a_full["next_day_fatigue_score"].values
    
    xgb_a = get_regression_model("xgboost", random_state=42)
    xgb_a.fit(X_a_mat, y_a)
    save_pickle(xgb_a, "artifacts/models/xgb_fatigue_model_dataset_a.pkl")
    save_pickle(prep_a, "artifacts/models/preprocessor_dataset_a.pkl")
    
    # Extract feature names after one-hot encoding
    encoded_cat_names_a = list(prep_a.named_transformers_["cat"].get_feature_names_out(cat_cols_final_a)) if "cat" in prep_a.named_transformers_ else []
    all_feature_names_a = num_cols_final_a + encoded_cat_names_a
    
    explainer_a = ModelExplainer(xgb_a, feature_names=all_feature_names_a, random_state=42)
    shap_df_a = explainer_a.fit_shap(X_a_mat, max_eval_samples=1000)
    shap_df_a.to_csv("artifacts/shap/shap_importance_dataset_a.csv", index=False)
    
    # Final representative XGBoost model on Dataset B for mental health prediction
    num_cols_final_b, cat_cols_final_b = feature_sets_b["Exp_D_Full_DLL"]
    prep_b = build_preprocessing_pipeline(num_cols_final_b, cat_cols_final_b)
    X_b_mat = prep_b.fit_transform(df_b_full)
    y_b = df_b_full["Mental_Health_Score"].values
    
    xgb_b = get_regression_model("xgboost", random_state=42)
    xgb_b.fit(X_b_mat, y_b)
    save_pickle(xgb_b, "artifacts/models/xgb_mental_health_model_dataset_b.pkl")
    save_pickle(prep_b, "artifacts/models/preprocessor_dataset_b.pkl")
    
    encoded_cat_names_b = list(prep_b.named_transformers_["cat"].get_feature_names_out(cat_cols_final_b)) if "cat" in prep_b.named_transformers_ else []
    all_feature_names_b = num_cols_final_b + encoded_cat_names_b
    
    explainer_b = ModelExplainer(xgb_b, feature_names=all_feature_names_b, random_state=42)
    shap_df_b = explainer_b.fit_shap(X_b_mat, max_eval_samples=1000)
    shap_df_b.to_csv("artifacts/shap/shap_importance_dataset_b.csv", index=False)

    # 7. STATISTICAL MEDIATION ANALYSIS (Phase 7)
    logger.info("--- STAGE 7: Bootstrap Statistical Mediation Modeling ---")
    med = StatisticalMediation(n_bootstraps=5000, ci_level=0.95, random_state=42)
    
    # Dataset A Pathway: Digital Lifestyle Load -> Sleep Latency -> Next-Day Fatigue Score
    med_res_a1 = med.fit(
        df_a_full,
        x_col="digital_lifestyle_load",
        m_col="sleep_latency_min",
        y_col="next_day_fatigue_score",
        covariate_cols=["age", "caffeine_post_5pm_mg", "physical_activity_min"]
    )
    
    # Dataset A Pathway 2: Digital Lifestyle Load -> Total Sleep Hours -> Next-Day Fatigue Score
    med_res_a2 = med.fit(
        df_a_full,
        x_col="digital_lifestyle_load",
        m_col="total_sleep_hours",
        y_col="next_day_fatigue_score",
        covariate_cols=["age", "caffeine_post_5pm_mg", "physical_activity_min"]
    )
    
    # Dataset B Pathway: Total Digital Hours -> Sleep Hours -> Mental Health Score
    med_res_b1 = med.fit(
        df_b_full,
        x_col="total_digital_hours",
        m_col="Sleep_Hours",
        y_col="Mental_Health_Score",
        covariate_cols=["Age", "Physical_Activity_Hours"]
    )
    
    # Dataset B Pathway 2: Digital Lifestyle Load -> Sleep Hours -> Mental Health Score
    med_res_b2 = med.fit(
        df_b_full,
        x_col="digital_lifestyle_load",
        m_col="Sleep_Hours",
        y_col="Mental_Health_Score",
        covariate_cols=["Age", "Physical_Activity_Hours"]
    )
    
    save_json({
        "dataset_a": {
            "latency_mediator": med_res_a1,
            "duration_mediator": med_res_a2
        },
        "dataset_b": {
            "hours_via_sleep": med_res_b1,
            "dll_via_sleep": med_res_b2
        }
    }, "artifacts/metrics/mediation_analysis.json")
    
    # Save processed enriched datasets
    df_a_full.to_csv("data/processed/dataset_a_processed.csv", index=False)
    df_b_full.to_csv("data/processed/dataset_b_processed.csv", index=False)
    logger.info("Processed datasets saved to data/processed/")

    logger.info("==================================================================")
    logger.info("DLSM RESEARCH EXECUTION PIPELINE COMPLETED SUCCESSFULLY!")
    logger.info("==================================================================")

if __name__ == "__main__":
    run_dlsm_pipeline()
