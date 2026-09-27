import pytest
from fastapi.testclient import TestClient
from dlsm.api.app import app

@pytest.fixture
def client():
    return TestClient(app)

def test_api_root(client):
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "operational"
    assert "/api/v1/predict/fatigue" in data["endpoints"]

def test_api_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["models_loaded"] is True

def test_api_phenotypes(client):
    response = client.get("/api/v1/phenotypes")
    assert response.status_code == 200
    data = response.json()
    assert len(data["cohort_a_phenotypes"]) == 2
    assert len(data["cohort_b_phenotypes"]) == 2
    assert "High-Load Nocturnally Disrupted" in [p["phenotype_name"] for p in data["cohort_a_phenotypes"]]

def test_api_predict_fatigue(client):
    payload = {
        "age": 21,
        "gender": "Female",
        "occupation_type": "Student",
        "chronotype": "Intermediate",
        "bedtime_phone_minutes": 60.0,
        "screen_brightness_pct": 75.0,
        "blue_light_filter_active": 0,
        "caffeine_post_5pm_mg": 90.0,
        "physical_activity_min": 20.0,
        "primary_bedtime_app": "Instagram / Reddit",
        "morning_alarm_snoozes": 3,
        "sleep_latency_min": 45.0,
        "total_sleep_hours": 5.2,
        "deep_sleep_pct": 18.0,
        "rem_sleep_pct": 17.0
    }
    response = client.post("/api/v1/predict/fatigue", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "predicted_fatigue_score" in data
    assert data["predicted_fatigue_score"] > 1.0
    assert "bedtime_intensity_index" in data
    assert "predicted_phenotype" in data

def test_api_predict_mental_health(client):
    payload = {
        "age": 20,
        "gender": "Female",
        "education_level": "University",
        "daily_social_media_hours": 5.5,
        "daily_ai_tool_usage_hours": 3.0,
        "sleep_hours": 6.0,
        "physical_activity_hours": 1.0,
        "physical_health_score": 80.0
    }
    response = client.post("/api/v1/predict/mental-health", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "predicted_mental_health_score" in data
    assert "active_buffer_ratio" in data
    assert "target_outcome_disclosure" in data
    assert "Mental_Health_Score" in data["target_outcome_disclosure"]

def test_api_simulate_policy(client):
    payload = {
        "cohort_size": 50,
        "weeks": 16,
        "exam_stress_multiplier": 1.0,
        "apply_shield": True
    }
    response = client.post("/api/v1/simulate/policy", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert len(data["weeks"]) == 16
    assert data["shielding_active"] is True
    assert data["burnout_hazard_pct"] == 0.0
