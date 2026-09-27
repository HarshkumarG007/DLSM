from pathlib import Path
import json
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from dlsm.api.schemas import (
    CohortAInput,
    CohortAPredictionResponse,
    CohortBInput,
    CohortBPredictionResponse,
    PolicySimulationRequest,
    PolicySimulationResponse,
    PhenotypeProfile,
    PhenotypesResponse,
)
from dlsm.features.engineer import DatasetAFeatureEngineer, DatasetBFeatureEngineer
from dlsm.simulation.longitudinal import LongitudinalPanelSimulator

app = FastAPI(
    title="Digital Lifestyle Spillover Model (DLSM) REST API",
    version="1.0.0",
    description=(
        "Production AI/ML REST microservice for the Digital Lifestyle Spillover Model (DLSM). "
        "Provides real-time inference for sleep architecture disruption, student mental health, "
        "biophysical optical loads, and dynamic 16-week semester longitudinal simulations."
    ),
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

PROJECT_ROOT = Path(__file__).resolve().parents[3]
MODELS_DIR = PROJECT_ROOT / "artifacts/models"
METRICS_DIR = PROJECT_ROOT / "artifacts/metrics"

# Cache loaded artifacts
_cache = {}

def get_artifacts():
    if "models_loaded" not in _cache:
        try:
            _cache["fe_a"] = DatasetAFeatureEngineer()
            _cache["dll_a"] = joblib.load(MODELS_DIR / "dll_extractor_a.pkl")
            _cache["prep_a"] = joblib.load(MODELS_DIR / "preprocessor_dataset_a.pkl")
            _cache["xgb_a"] = joblib.load(MODELS_DIR / "xgb_fatigue_model_dataset_a.pkl")

            _cache["fe_b"] = DatasetBFeatureEngineer()
            _cache["dll_b"] = joblib.load(MODELS_DIR / "dll_extractor_b.pkl")
            _cache["prep_b"] = joblib.load(MODELS_DIR / "preprocessor_dataset_b.pkl")
            _cache["xgb_b"] = joblib.load(MODELS_DIR / "xgb_mental_health_model_dataset_b.pkl")

            with open(METRICS_DIR / "clustering_phenotypes.json", "r") as f:
                _cache["clustering"] = json.load(f)

            _cache["models_loaded"] = True
        except Exception as e:
            raise RuntimeError(f"Failed to load DLSM model artifacts: {e}")
    return _cache

@app.get("/")
def read_root():
    return {
        "title": "Digital Lifestyle Spillover Model (DLSM) REST API",
        "version": "1.0.0",
        "status": "operational",
        "documentation": "/docs",
        "endpoints": [
            "/health",
            "/api/v1/phenotypes",
            "/api/v1/predict/fatigue",
            "/api/v1/predict/mental-health",
            "/api/v1/simulate/policy"
        ]
    }

@app.get("/health")
def health_check():
    artifacts = get_artifacts()
    return {
        "status": "healthy",
        "models_loaded": artifacts.get("models_loaded", False),
        "version": "1.0.0"
    }

@app.get("/api/v1/phenotypes", response_model=PhenotypesResponse)
def get_phenotypes():
    art = get_artifacts()
    cl_data = art.get("clustering", {})
    
    cohort_a_list = [
        PhenotypeProfile(
            cohort="Cohort A (Bedtime Telemetry)",
            cluster_id=0,
            phenotype_name="High-Load Nocturnally Disrupted",
            population_share_pct=32.6,
            latent_dll=1.69,
            key_characteristics={
                "sleep_latency_min": 59.3,
                "total_sleep_hours": 5.08,
                "deep_sleep_pct": 19.87,
                "caffeine_post_5pm_mg": 128.4
            }
        ),
        PhenotypeProfile(
            cohort="Cohort A (Bedtime Telemetry)",
            cluster_id=1,
            phenotype_name="Regulated Circadian Restorative",
            population_share_pct=67.4,
            latent_dll=-0.82,
            key_characteristics={
                "sleep_latency_min": 31.7,
                "total_sleep_hours": 6.84,
                "deep_sleep_pct": 22.64,
                "caffeine_post_5pm_mg": 52.1
            }
        )
    ]
    
    cohort_b_list = [
        PhenotypeProfile(
            cohort="Cohort B (Student Digital Life)",
            cluster_id=0,
            phenotype_name="Intensive Dual-Screen Load",
            population_share_pct=47.1,
            latent_dll=1.41,
            key_characteristics={
                "daily_social_media_hours": 6.20,
                "daily_ai_tool_usage_hours": 3.30,
                "sleep_hours": 5.92,
                "physical_activity_hours": 1.08
            }
        ),
        PhenotypeProfile(
            cohort="Cohort B (Student Digital Life)",
            cluster_id=1,
            phenotype_name="Balanced Digital Moderates",
            population_share_pct=52.9,
            latent_dll=-1.25,
            key_characteristics={
                "daily_social_media_hours": 3.05,
                "daily_ai_tool_usage_hours": 1.96,
                "sleep_hours": 7.10,
                "physical_activity_hours": 1.40
            }
        )
    ]
    
    return PhenotypesResponse(
        cohort_a_phenotypes=cohort_a_list,
        cohort_b_phenotypes=cohort_b_list
    )

@app.post("/api/v1/predict/fatigue", response_model=CohortAPredictionResponse)
def predict_fatigue(payload: CohortAInput):
    art = get_artifacts()
    
    df_raw = pd.DataFrame([{
        "user_id": "API_USER",
        "age": payload.age,
        "gender": payload.gender,
        "occupation_type": payload.occupation_type,
        "chronotype": payload.chronotype,
        "bedtime_phone_minutes": payload.bedtime_phone_minutes,
        "screen_brightness_pct": payload.screen_brightness_pct,
        "blue_light_filter_active": payload.blue_light_filter_active,
        "caffeine_post_5pm_mg": payload.caffeine_post_5pm_mg,
        "physical_activity_min": payload.physical_activity_min,
        "primary_bedtime_app": payload.primary_bedtime_app,
        "morning_alarm_snoozes": payload.morning_alarm_snoozes,
        "sleep_latency_min": payload.sleep_latency_min,
        "total_sleep_hours": payload.total_sleep_hours,
        "deep_sleep_pct": payload.deep_sleep_pct,
        "rem_sleep_pct": payload.rem_sleep_pct,
        "sleep_debt_category": "Moderate Debt"
    }])
    
    df_eng = art["fe_a"].transform(df_raw)
    df_full = art["dll_a"].transform(df_eng)
    X_mat = art["prep_a"].transform(df_full)
    fatigue_pred = float(art["xgb_a"].predict(X_mat)[0])
    
    bii = float(df_eng["bedtime_intensity_index"].iloc[0])
    ssr = float(df_eng["screen_to_sleep_ratio"].iloc[0])
    slr = float(df_eng["sleep_latency_ratio"].iloc[0])
    caw = float(df_eng["cognitive_arousal_weight"].iloc[0])
    dll = float(df_full["digital_lifestyle_load"].iloc[0])
    
    phenotype = "High-Load Nocturnally Disrupted" if dll > 0.0 else "Regulated Circadian Restorative"
    
    if fatigue_pred >= 6.0:
        risk = "HIGH RISK: Severe daytime fatigue and circadian phase delay."
    elif fatigue_pred >= 4.0:
        risk = "MODERATE RISK: Sub-clinical daytime drowsiness and moderate sleep latency elongation."
    else:
        risk = "LOW RISK: Preserved daytime vitality and restorative sleep architecture."
        
    return CohortAPredictionResponse(
        predicted_fatigue_score=round(fatigue_pred, 2),
        bedtime_intensity_index=round(bii, 2),
        screen_to_sleep_ratio=round(ssr, 2),
        sleep_latency_ratio=round(slr, 2),
        cognitive_arousal_weight=round(caw, 2),
        digital_lifestyle_load=round(dll, 2),
        predicted_phenotype=phenotype,
        risk_assessment=risk
    )

@app.post("/api/v1/predict/mental-health", response_model=CohortBPredictionResponse)
def predict_mental_health(payload: CohortBInput):
    art = get_artifacts()
    
    df_raw = pd.DataFrame([{
        "Student_ID": "API_STUDENT",
        "Age": payload.age,
        "Gender": payload.gender,
        "Education_Level": payload.education_level,
        "Daily_Social_Media_Hours": payload.daily_social_media_hours,
        "Daily_AI_Tool_Usage_Hours": payload.daily_ai_tool_usage_hours,
        "Sleep_Hours": payload.sleep_hours,
        "Physical_Activity_Hours": payload.physical_activity_hours,
        "Physical_Health_Score": payload.physical_health_score
    }])
    
    df_eng = art["fe_b"].transform(df_raw)
    df_full = art["dll_b"].transform(df_eng)
    X_mat = art["prep_b"].transform(df_full)
    mh_pred = float(art["xgb_b"].predict(X_mat)[0])
    
    tdh = float(df_eng["total_digital_hours"].iloc[0])
    ssr = float(df_eng["screen_to_sleep_ratio"].iloc[0])
    abr = float(df_eng["active_buffer_ratio"].iloc[0])
    dll = float(df_full["digital_lifestyle_load"].iloc[0])
    
    phenotype = "Intensive Dual-Screen Load" if dll > 0.0 else "Balanced Digital Moderates"
    
    if mh_pred < 68.0:
        risk_tier = "High Risk / Psychological Strain"
    elif mh_pred < 76.0:
        risk_tier = "Moderate Risk"
    else:
        risk_tier = "Low Risk / Flourishing"
        
    disclosure = (
        "Dataset B Target Outcome Disclosure: Evaluated on empirical Mental_Health_Score. "
        "Dataset B contains no grades or GPA column; downstream academic spillover is modeled conceptually."
    )
    
    return CohortBPredictionResponse(
        predicted_mental_health_score=round(mh_pred, 2),
        total_digital_hours=round(tdh, 2),
        screen_to_sleep_ratio=round(ssr, 2),
        active_buffer_ratio=round(abr, 2),
        digital_lifestyle_load=round(dll, 2),
        predicted_phenotype=phenotype,
        risk_tier=risk_tier,
        target_outcome_disclosure=disclosure
    )

@app.post("/api/v1/simulate/policy", response_model=PolicySimulationResponse)
def simulate_policy(payload: PolicySimulationRequest):
    sim = LongitudinalPanelSimulator(weeks=payload.weeks, random_state=42)
    
    if payload.apply_shield:
        df_sim = sim.simulate_semester(
            baseline_social_hours=3.0,
            baseline_ai_hours=2.0,
            baseline_bedtime_min=30,
            baseline_sleep_hours=7.5,
            baseline_activity_hours=1.8,
            blue_light_filter=True,
            exam_intensity_multiplier=payload.exam_stress_multiplier
        )
    else:
        df_sim = sim.simulate_semester(
            baseline_social_hours=5.0,
            baseline_ai_hours=2.8,
            baseline_bedtime_min=75,
            baseline_sleep_hours=6.2,
            baseline_activity_hours=1.0,
            blue_light_filter=False,
            exam_intensity_multiplier=payload.exam_stress_multiplier
        )
    
    final_debt = float(df_sim["Cumulative_Sleep_Debt_Hours"].iloc[-1])
    severe_risk_weeks = int((df_sim["Risk_Status"] == "Severe Burnout Risk").sum())
    burnout_hazard_pct = round((severe_risk_weeks / payload.weeks) * 100.0, 1)
    
    # Stress wave calculation
    stress_wave = [
        round(1.0 + (0.40 * 2.718 ** (-((t - 7) ** 2) / (2 * 1.2 ** 2)) +
                     0.70 * 2.718 ** (-((t - 15) ** 2) / (2 * 1.5 ** 2))) * payload.exam_stress_multiplier, 3)
        for t in df_sim["Week"].tolist()
    ]
    
    findings = (
        f"Simulated {payload.weeks} academic weeks under {'Shielded Protocol' if payload.apply_shield else 'Unshielded Baseline'}. "
        f"Final cumulative sleep debt: {final_debt:.1f} hours. "
        f"Burnout hazard incidence rate: {burnout_hazard_pct}%. "
        f"Screen-to-sleep ratio averaged {df_sim['Screen_to_Sleep_Ratio'].mean():.2f}."
    )
    
    return PolicySimulationResponse(
        weeks=df_sim["Week"].tolist(),
        stress_wave=stress_wave,
        mean_screen_hours=df_sim["Total_Digital_Hours"].tolist(),
        mean_sleep_hours=df_sim["Sleep_Hours"].tolist(),
        cumulative_sleep_debt=df_sim["Cumulative_Sleep_Debt_Hours"].tolist(),
        burnout_hazard_pct=burnout_hazard_pct,
        shielding_active=payload.apply_shield,
        summary_findings=findings
    )
