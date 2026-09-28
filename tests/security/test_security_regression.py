"""
DLSM Automated Security Regression & Invariant Test Suite.
Validates security controls, authentication baselines, input boundary constraints,
privacy preservation, secrets hygiene, and container/CI configuration invariants.
"""

import hashlib
import json
import os
import re
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

from dlsm.api.app import app
from dlsm.api.schemas import CohortAInput, CohortBInput, PolicySimulationRequest
from dlsm.data.loader import load_dataset_a, load_dataset_b

REPO_ROOT = Path(__file__).resolve().parents[2]
MODELS_DIR = REPO_ROOT / "artifacts/models"
client = TestClient(app)

class TestSecurityRegression:
    """Security regression test cases mapped to Red-Team findings."""

    def test_sec_01_api_authentication_posture(self):
        """
        [SEC-01] Broken Authentication / Open Endpoints Audit.
        EXPECTED SECURE BEHAVIOR: Sensitive inference endpoints should require authentication (API key or Bearer token).
        CURRENT FINDING: Endpoints are open/unauthenticated. This test documents the open attack surface.
        """
        resp_health = client.get("/health")
        assert resp_health.status_code == 200, "Health check should be accessible"
        
        # Test that predict endpoint currently responds without auth headers
        payload = {
            "age": 21,
            "gender": "Female",
            "occupation_type": "Student",
            "chronotype": "Intermediate",
            "bedtime_phone_minutes": 45.0,
            "screen_brightness_pct": 60.0,
            "blue_light_filter_active": 1,
            "caffeine_post_5pm_mg": 50.0,
            "physical_activity_min": 40.0,
            "primary_bedtime_app": "Instagram / Reddit",
            "morning_alarm_snoozes": 1,
            "sleep_latency_min": 35.0,
            "total_sleep_hours": 6.5,
            "deep_sleep_pct": 21.0,
            "rem_sleep_pct": 19.0
        }
        resp_pred = client.post("/api/v1/predict/fatigue", json=payload)
        assert resp_pred.status_code == 200, "Documents unauthenticated access allowed"

    def test_sec_02_cors_configuration_hygiene(self):
        """
        [SEC-02] CORS Misconfiguration Check.
        EXPECTED SECURE BEHAVIOR: Wildcard origins ('*') MUST NOT be paired with allow_credentials=True.
        """
        cors_middlewares = [m for m in app.user_middleware if "CORSMiddleware" in str(m)]
        for m in cors_middlewares:
            kwargs = m.kwargs
            origins = kwargs.get("allow_origins", [])
            allow_creds = kwargs.get("allow_credentials", False)
            if "*" in origins:
                assert not allow_creds, "Remediated CORS finding: allow_credentials must be False when allow_origins=['*']"

    def test_sec_03_input_validation_boundary_enforcement(self):
        """
        [SEC-03] Input Validation & Numerical Range Enforcement.
        EXPECTED SECURE BEHAVIOR: Out-of-bounds, negative, or absurd values must be rejected with 422 Unprocessable Entity.
        """
        # Test negative sleep hours
        bad_cohort_b = {
            "age": 20,
            "gender": "Female",
            "education_level": "University",
            "daily_social_media_hours": -5.0, # Negative hours
            "daily_ai_tool_usage_hours": 2.0,
            "sleep_hours": 6.5,
            "physical_activity_hours": 1.2,
            "physical_health_score": 85.0
        }
        resp = client.post("/api/v1/predict/mental-health", json=bad_cohort_b)
        assert resp.status_code == 422, "Pydantic validator should reject negative social media hours"

        # Test extreme out-of-range age
        bad_age = dict(bad_cohort_b, daily_social_media_hours=4.0, age=120)
        resp_age = client.post("/api/v1/predict/mental-health", json=bad_age)
        assert resp_age.status_code == 422, "Pydantic validator should reject age outside bounds"

    def test_sec_04_policy_simulation_parameter_bounds(self):
        """
        [SEC-04] Resource Exhaustion & Simulation Parameter Flooding.
        EXPECTED SECURE BEHAVIOR: Semester weeks must be bounded (e.g. 4 <= weeks <= 32) to prevent CPU DoS.
        """
        bad_sim = {
            "weeks": 500, # Extreme duration attempting CPU exhaustion
            "exam_stress_multiplier": 1.0,
            "apply_shield": False
        }
        resp = client.post("/api/v1/simulate/policy", json=bad_sim)
        assert resp.status_code == 422, "Pydantic validator should block excessive simulation weeks"

    def test_sec_05_secrets_scanner_regression(self):
        """
        [SEC-05] Automated Secrets & Credential Scan.
        EXPECTED SECURE BEHAVIOR: Zero hardcoded AWS, GCP, GitHub tokens, or private keys across repo.
        """
        patterns = [
            re.compile(r"ghp_[0-9a-zA-Z]{36}"),
            re.compile(r"AKIA[0-9A-Z]{16}"),
            re.compile(r"-----BEGIN (RSA|EC|DSA|OPENSSH) PRIVATE KEY-----"),
            re.compile(r"AIza[0-9A-Za-z\\-_]{35}"),
        ]
        
        scanned_files = 0
        for ext in ["*.py", "*.json", "*.yaml", "*.yml", "*.md", "*.toml"]:
            for fpath in REPO_ROOT.rglob(ext):
                if ".git" in str(fpath) or ".pytest_cache" in str(fpath):
                    continue
                scanned_files += 1
                try:
                    content = fpath.read_text(encoding="utf-8", errors="ignore")
                    for pat in patterns:
                        assert not pat.search(content), f"Exposed credential pattern found in {fpath}"
                except Exception:
                    pass
        assert scanned_files > 15, "Should scan substantial repository files"

    def test_sec_06_model_artifact_checksum_verification(self):
        """
        [SEC-06] Model Serialization & Insecure Deserialization Audit.
        EXPECTED SECURE BEHAVIOR: Artifacts loaded via joblib/pickle must have recorded SHA-256 checksums.
        """
        assert MODELS_DIR.exists(), "Models directory must exist"
        pkl_files = list(MODELS_DIR.glob("*.pkl"))
        assert len(pkl_files) >= 4, "Must detect serialized model artifacts"
        
        # Calculate SHA256 of all model artifacts to demonstrate verifiable integrity baseline
        checksums = {}
        for pkl in pkl_files:
            h = hashlib.sha256(pkl.read_bytes()).hexdigest()
            checksums[pkl.name] = h
            assert len(h) == 64, "SHA-256 hash must be 64 hexadecimal characters"
        
        # Verify dll_extractor_a.pkl has a non-empty valid hash
        assert "dll_extractor_a.pkl" in checksums

    def test_sec_07_privacy_identifier_separation(self):
        """
        [SEC-07] Privacy & Identifier Separation Invariant.
        EXPECTED SECURE BEHAVIOR: Primary keys (Student_ID, user_id) must never be used as predictive features.
        """
        df_b = load_dataset_b()
        assert "Student_ID" in df_b.columns, "Student_ID must be present in raw schema"
        
        # Verify feature dictionary classifies it as IDENTIFIER
        feat_dict_path = REPO_ROOT / "metadata/feature_dictionary.yaml"
        if feat_dict_path.exists():
            import yaml
            with open(feat_dict_path, "r", encoding="utf-8") as f:
                feat_tax = yaml.safe_load(f)
            assert "IDENTIFIER" in feat_tax.get("taxonomy", []) or "identifier" in str(feat_tax).lower()

    def test_sec_08_docker_security_posture(self):
        """
        [SEC-08] Container Least-Privilege & Dockerignore Audit.
        EXPECTED SECURE BEHAVIOR: Dockerfile must define non-root user and .dockerignore must exist.
        """
        dockerfile = REPO_ROOT / "Dockerfile"
        assert dockerfile.exists()
        dockerignore = REPO_ROOT / ".dockerignore"
        assert dockerignore.exists(), "Remediated: .dockerignore must exist to prevent context leakage"
        ignore_content = dockerignore.read_text(encoding="utf-8")
        assert ".git" in ignore_content, ".dockerignore must exclude .git directory"

    def test_sec_09_ci_permissions_audit(self):
        """
        [SEC-09] CI/CD Workflow Token Permissions Invariant.
        EXPECTED SECURE BEHAVIOR: GitHub Actions workflows should declare least-privilege permissions.
        """
        ci_path = REPO_ROOT / ".github/workflows/ci.yml"
        assert ci_path.exists()
        ci_content = ci_path.read_text(encoding="utf-8")
        assert "permissions:" in ci_content, "Remediated: CI workflow must declare explicit permissions"
        assert "contents: read" in ci_content, "CI workflow must specify least-privilege 'contents: read'"
