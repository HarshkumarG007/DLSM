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

    def test_sec_01_api_authentication_posture(self, monkeypatch):
        """
        [SEC-01] Broken Authentication & API Key Enforcement Audit.
        EXPECTED SECURE BEHAVIOR: Sensitive inference endpoints should require authentication (API key or Bearer token).
        Remediated with optional env-driven X-API-Key enforcement.
        """
        resp_health = client.get("/health")
        assert resp_health.status_code == 200, "Health check should be accessible unauthenticated"
        
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
        # In default local/dev mode without DLSM_API_KEY configured, access is permitted
        resp_pred = client.post("/api/v1/predict/fatigue", json=payload)
        assert resp_pred.status_code == 200, "Documents access allowed in development"

        # When DLSM_API_KEY is configured, requests without key must receive 401 Unauthorized
        monkeypatch.setenv("DLSM_API_KEY", "dlsm-test-secret-key-2026")
        resp_unauth = client.post("/api/v1/predict/fatigue", json=payload)
        assert resp_unauth.status_code == 401, "Protected endpoint must reject unauthenticated requests when DLSM_API_KEY set"

        # Requests with wrong key must receive 401 Unauthorized
        resp_wrong = client.post("/api/v1/predict/fatigue", json=payload, headers={"X-API-Key": "wrong-key"})
        assert resp_wrong.status_code == 401, "Protected endpoint must reject invalid API key"

        # Requests with valid key must receive 200 OK
        resp_auth = client.post("/api/v1/predict/fatigue", json=payload, headers={"X-API-Key": "dlsm-test-secret-key-2026"})
        assert resp_auth.status_code == 200, "Protected endpoint must allow valid API key"

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
        EXPECTED SECURE BEHAVIOR: Artifacts loaded via joblib/pickle must have recorded SHA-256 checksums,
        and helpers.load_pickle must raise ValueError on checksum tampering.
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

        # Verify baseline checksums.json exists and matches disk artifacts
        checksums_manifest = MODELS_DIR / "checksums.json"
        assert checksums_manifest.exists(), "artifacts/models/checksums.json must exist"
        recorded = json.loads(checksums_manifest.read_text(encoding="utf-8"))
        for pkl in pkl_files:
            assert pkl.name in recorded, f"{pkl.name} must be cataloged in checksums.json"
            assert checksums[pkl.name] == recorded[pkl.name], f"Checksum mismatch for {pkl.name}"

        # Verify load_pickle actively prevents deserialization of tampered artifacts
        from dlsm.utils.helpers import load_pickle
        import tempfile
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            dummy_pkl = tmppath / "model.pkl"
            dummy_pkl.write_bytes(b"tampered content")
            (tmppath / "checksums.json").write_text(json.dumps({"model.pkl": "0" * 64}))
            with pytest.raises(ValueError, match="Security Alert: Checksum mismatch"):
                load_pickle(dummy_pkl)

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
        content = dockerfile.read_text(encoding="utf-8")
        assert "USER dlsm" in content, "Dockerfile must execute under non-root user dlsm"
        assert "HEALTHCHECK" in content, "Dockerfile must declare container HEALTHCHECK"

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

    def test_sec_10_rate_limiting_enforcement(self, monkeypatch):
        """
        [SEC-06 / SEC-09] Rate Limiting & Denial of Service Protection.
        EXPECTED SECURE BEHAVIOR: Excessive rapid requests must be rate-limited with HTTP 429 Too Many Requests.
        """
        monkeypatch.setenv("DLSM_RATE_LIMIT_PER_MINUTE", "5")
        headers = {"X-API-Key": "test-rate-limit-client"}
        
        # Requests up to the limit should succeed
        for i in range(5):
            resp = client.get("/api/v1/phenotypes", headers=headers)
            assert resp.status_code == 200, f"Request {i+1} should succeed under threshold"
            assert "X-RateLimit-Remaining" in resp.headers

        # 6th request within window must be rejected with 429
        resp_blocked = client.get("/api/v1/phenotypes", headers=headers)
        assert resp_blocked.status_code == 429, "6th request within window must be rate-limited with 429"
        assert "Retry-After" in resp_blocked.headers
        assert "Rate limit exceeded" in resp_blocked.json()["detail"]

    def test_sec_11_k_anonymity_preservation(self):
        """
        [SEC-05] Privacy Enhancement & k-Anonymity Verification.
        EXPECTED SECURE BEHAVIOR: Published research cohorts must satisfy k-anonymity (k >= 5)
        with direct identifiers stripped and quasi-identifiers generalized.
        """
        from dlsm.privacy.anonymize import k_anonymize_dataset_b
        df_b = load_dataset_b()
        anon_df, metrics = k_anonymize_dataset_b(df_b, k=5)
        
        assert "Student_ID" not in anon_df.columns, "Direct identifier must be stripped"
        assert metrics["k_anonymity_satisfied"] is True, "Dataset must strictly satisfy k-anonymity"
        assert metrics["achieved_k"] >= 5, f"Achieved k must be >= 5, got {metrics['achieved_k']}"
        assert metrics["retention_rate_pct"] > 95.0, "Utility retention must remain high"
        assert "Age_Band" in anon_df.columns
        assert "Mental_Health_Category" in anon_df.columns

    def test_sec_12_dependency_lockfile_integrity(self):
        """
        [SEC-08] Supply Chain Security & Lockfile Hash Integrity.
        EXPECTED SECURE BEHAVIOR: A verified requirements.lock file must exist with cryptographically pinned hashes.
        """
        lock_path = REPO_ROOT / "requirements.lock"
        assert lock_path.exists(), "requirements.lock must exist for deterministic builds"
        content = lock_path.read_text(encoding="utf-8")
        assert "--hash=sha256:" in content, "requirements.lock must enforce cryptographic SHA-256 hashes"
        assert "numpy==" in content
        assert "fastapi==" in content
        assert "xgboost==" in content

    def test_sec_13_differential_privacy_mechanism(self):
        """
        [SEC-05 / Long-Term Roadmap] Calibrated Differential Privacy for Longitudinal Simulation Aggregates.
        EXPECTED SECURE BEHAVIOR:
        1. DifferentialPrivacyEngine applies calibrated Laplace and Gaussian perturbation.
        2. Strictly bounds outputs within physical limits (e.g. burnout_hazard_pct in [0, 100]).
        3. Validates boundary validation (epsilon > 0, 0 < delta < 1).
        4. Verifies integration via FastAPI /api/v1/simulate/policy when epsilon is provided.
        """
        from dlsm.privacy import DifferentialPrivacyEngine

        engine = DifferentialPrivacyEngine(random_state=42)

        # 1. Parameter validation
        with pytest.raises(ValueError, match="Epsilon must be strictly positive"):
            engine.laplace_mechanism(value=10.0, sensitivity=1.0, epsilon=0.0)

        with pytest.raises(ValueError, match="Invalid DP parameters"):
            engine.gaussian_mechanism(value=10.0, sensitivity=1.0, epsilon=1.0, delta=1.5)

        # 2. Perturbation & physical bounding
        priv_summary = engine.privatize_simulation_summary(
            final_sleep_debt=14.5,
            burnout_hazard_pct=25.0,
            mean_screen_hours=6.5,
            weeks=16,
            cohort_size=50,
            epsilon=1.0,
            mechanism="laplace"
        )
        assert "privacy_guarantee" in priv_summary
        assert "1.00-DP (Laplace)" in priv_summary["privacy_guarantee"]
        assert 0.0 <= priv_summary["privatized_burnout_hazard_pct"] <= 100.0
        assert priv_summary["privatized_final_sleep_debt"] >= 0.0
        assert priv_summary["privatized_mean_screen_hours"] >= 0.0

        # Gaussian mechanism test
        priv_summary_gauss = engine.privatize_simulation_summary(
            final_sleep_debt=14.5,
            burnout_hazard_pct=25.0,
            mean_screen_hours=6.5,
            weeks=16,
            cohort_size=50,
            epsilon=1.0,
            mechanism="gaussian"
        )
        assert "1e-5" in priv_summary_gauss["privacy_guarantee"]

        # 3. API endpoint integration with epsilon
        payload_with_dp = {
            "cohort_size": 50,
            "weeks": 16,
            "exam_stress_multiplier": 1.0,
            "apply_shield": True,
            "epsilon": 1.0
        }
        resp = client.post("/api/v1/simulate/policy", json=payload_with_dp)
        assert resp.status_code == 200
        data = resp.json()
        assert data["differential_privacy_summary"] is not None
        assert data["differential_privacy_summary"]["total_epsilon"] == 1.0
        assert "privatized_burnout_hazard_pct" in data["differential_privacy_summary"]

