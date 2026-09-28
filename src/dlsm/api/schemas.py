from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field

class CohortAInput(BaseModel):
    age: int = Field(default=21, ge=18, le=75, description="Participant age in years")
    gender: str = Field(default="Female", description="Gender (Female, Male, Non-binary)")
    occupation_type: str = Field(default="Student", description="Occupation (Student, Corporate 9-to-5, Remote Tech, Freelance / Creative, Healthcare / Shift Worker)")
    chronotype: str = Field(default="Intermediate", description="Circadian chronotype (Intermediate, Night Owl, Morning Lark)")
    bedtime_phone_minutes: float = Field(default=45.0, ge=0.0, le=300.0, description="Minutes spent on smartphone in bed before trying to sleep")
    screen_brightness_pct: float = Field(default=60.0, ge=10.0, le=100.0, description="Screen brightness setting percentage")
    blue_light_filter_active: int = Field(default=1, ge=0, le=1, description="Night light / blue-light filter active (1 for ON, 0 for OFF)")
    caffeine_post_5pm_mg: float = Field(default=50.0, ge=0.0, le=600.0, description="Milligrams of caffeine consumed after 5:00 PM")
    physical_activity_min: float = Field(default=40.0, ge=0.0, le=360.0, description="Daily physical activity in minutes")
    primary_bedtime_app: str = Field(default="Instagram / Reddit", description="Primary bedtime app genre")
    morning_alarm_snoozes: int = Field(default=1, ge=0, le=15, description="Number of times morning alarm was snoozed")
    sleep_latency_min: float = Field(default=35.0, ge=5.0, le=180.0, description="Time taken to fall asleep in minutes")
    total_sleep_hours: float = Field(default=6.5, ge=2.0, le=12.0, description="Total nocturnal sleep hours")
    deep_sleep_pct: float = Field(default=21.0, ge=5.0, le=40.0, description="Percentage of sleep in deep slow-wave stage")
    rem_sleep_pct: float = Field(default=19.0, ge=5.0, le=40.0, description="Percentage of sleep in REM stage")

class CohortAPredictionResponse(BaseModel):
    predicted_fatigue_score: float = Field(description="Predicted next-day fatigue score (1.0 = vitalized, 10.0 = exhausted)")
    bedtime_intensity_index: float = Field(description="Calculated biophysical optical load index")
    screen_to_sleep_ratio: float = Field(description="Ratio of bedtime phone hours to nocturnal sleep duration")
    sleep_latency_ratio: float = Field(description="Sleep onset latency relative to restorative baseline")
    cognitive_arousal_weight: float = Field(description="App interactivity cognitive stimulation multiplier")
    digital_lifestyle_load: float = Field(description="Normalized latent DLL factor coordinate")
    predicted_phenotype: str = Field(description="Assigned behavioral phenotype cluster")
    risk_assessment: str = Field(description="Clinical / cognitive risk assessment summary")

class CohortBInput(BaseModel):
    age: int = Field(default=20, ge=13, le=35, description="Student age in years")
    gender: str = Field(default="Female", description="Gender (Female, Male, Non-binary)")
    education_level: str = Field(default="University", description="Education Level (High School, College, University)")
    daily_social_media_hours: float = Field(default=4.0, ge=0.0, le=16.0, description="Daily hours spent on social media platforms")
    daily_ai_tool_usage_hours: float = Field(default=2.0, ge=0.0, le=14.0, description="Daily hours spent interacting with generative AI tools")
    sleep_hours: float = Field(default=6.5, ge=2.0, le=14.0, description="Average nocturnal sleep duration in hours")
    physical_activity_hours: float = Field(default=1.2, ge=0.0, le=8.0, description="Daily moderate-to-vigorous exercise in hours")
    physical_health_score: float = Field(default=85.0, ge=0.0, le=100.0, description="General physical vitality score")

class CohortBPredictionResponse(BaseModel):
    predicted_mental_health_score: float = Field(description="Predicted student mental health score (0.0–100.0, higher is better)")
    total_digital_hours: float = Field(description="Summed daily digital exposure (Social Media + AI Tools)")
    screen_to_sleep_ratio: float = Field(description="Ratio of daily screen hours to nocturnal sleep duration")
    active_buffer_ratio: float = Field(description="Ratio of physical exercise buffer to total screen hours")
    digital_lifestyle_load: float = Field(description="Normalized latent DLL factor coordinate")
    predicted_phenotype: str = Field(description="Assigned behavioral phenotype cluster")
    risk_tier: str = Field(description="Mental health risk classification tier (Low Risk, Moderate Risk, High Risk)")
    target_outcome_disclosure: str = Field(description="Empirical target outcome scientific disclosure")

class PolicySimulationRequest(BaseModel):
    cohort_size: int = Field(default=100, ge=10, le=1000, description="Simulated student cohort size")
    weeks: int = Field(default=16, ge=4, le=32, description="Academic semester duration in weeks")
    exam_stress_multiplier: float = Field(default=1.0, ge=0.5, le=2.5, description="Midterm/final examination stress amplifier")
    apply_shield: bool = Field(default=False, description="Enable institutional wellbeing shielding protocol")
    epsilon: Optional[float] = Field(default=None, ge=0.01, le=10.0, description="Optional differential privacy budget epsilon for aggregate output perturbation")

class PolicySimulationResponse(BaseModel):
    weeks: List[int]
    stress_wave: List[float]
    mean_screen_hours: List[float]
    mean_sleep_hours: List[float]
    cumulative_sleep_debt: List[float]
    burnout_hazard_pct: float
    shielding_active: bool
    summary_findings: str
    differential_privacy_summary: Optional[Dict[str, Any]] = Field(default=None, description="Differentially private sanitized aggregate summary (populated when epsilon is specified)")


class PhenotypeProfile(BaseModel):
    cohort: str
    cluster_id: int
    phenotype_name: str
    population_share_pct: float
    latent_dll: float
    key_characteristics: Dict[str, Any]

class PhenotypesResponse(BaseModel):
    cohort_a_phenotypes: List[PhenotypeProfile]
    cohort_b_phenotypes: List[PhenotypeProfile]
