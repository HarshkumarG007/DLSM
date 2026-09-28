# Security Policy & Vulnerability Disclosure

## 1. Overview & Security Architecture

The **Digital Lifestyle Spillover Model (DLSM)** research initiative maintains a proactive security, privacy, and ML-integrity defense-in-depth posture. DLSM processes biophysical and student behavioral telemetry to evaluate cognitive fatigue and mental wellbeing.

All security controls are continuously audited against an automated 13-part invariant regression suite (`tests/security/test_security_regression.py`) enforced on every pull request and push to `main`.

---

## 2. Supported Versions

Security updates, dependency patches, and vulnerability remediations are actively maintained for the following versions:

| Version | Supported | Status |
| :--- | :---: | :--- |
| `1.0.x` (Current `main`) | :white_check_mark: | Actively supported with automated CI/CD security regression |
| `< 1.0.0` | :x: | Deprecated / Development prototypes |

---

## 3. Reporting a Vulnerability

We welcome responsible security disclosures from independent researchers, auditors, and academic peers.

### 3.1 Disclosure Process
- **Contact:** Please email vulnerability disclosures privately to:  
  **`hrslsha007@gmail.com`**
- **Subject Line:** `[DLSM Security Advisory] <Brief Description>`
- **Information to Include:**
  - Description of the vulnerability and attack vector.
  - Proof-of-concept (PoC) script, HTTP request, or reproduction steps.
  - Affected components (`src/dlsm/api/`, `app/`, `artifacts/models/`, `Dockerfile`, etc.).
  - Assessment of potential impact (e.g., data leakage, model extraction, denial of service).

### 3.2 Response Service Level Agreements (SLAs)
- **Initial Acknowledgment:** Within **24 hours**.
- **Triage & Impact Assessment:** Within **48 hours**.
- **Remediation & Fix Deployment:** Within **7 days** for Critical/High severity issues.
- **Coordinated Disclosure:** Public disclosure occurs only after a patch is validated and deployed.

---

## 4. Key Defensive Security Controls

| Category | Defensive Mechanism | Implementation Reference |
| :--- | :--- | :--- |
| **API Authentication** | Optional environment-driven `X-API-Key` header verification on inference routes | `src/dlsm/api/app.py:verify_api_key` |
| **Rate Limiting** | Sliding-window memory rate limiter mitigating model extraction / DoS bursts | `src/dlsm/api/app.py:SlidingWindowRateLimiter` |
| **Model Integrity** | SHA-256 cryptographic pre-deserialization validation on all serialized `.pkl` models | `artifacts/models/checksums.json`, `helpers.py` |
| **Container Security** | Least-privilege non-root execution (`USER dlsm`, UID 1001) & active container `HEALTHCHECK` | `Dockerfile`, `test_sec_08` |
| **Context Isolation** | Strict `.dockerignore` eliminating `.git/` history and environment secrets leakage | `.dockerignore`, `test_sec_08` |
| **Data Privacy** | Strict $k$-anonymity ($k \ge 5$) on exported data & direct identifier stripping | `src/dlsm/privacy/anonymize.py`, `test_sec_11` |
| **Differential Privacy** | Calibrated Laplace & Gaussian mechanisms for aggregate longitudinal queries | `src/dlsm/privacy/differential_privacy.py`, `test_sec_13` |
| **Supply Chain Security** | Cryptographically pinned dependency lockfile (`requirements.lock` with SHA-256) | `requirements.lock`, `test_sec_12` |
| **CI/CD Hardening** | Explicit least-privilege token permissions (`contents: read`) across all workflows | `.github/workflows/ci.yml`, `manuscript.yml` |

---

## 5. Ethical AI & Data Privacy Governance

- **Human Subjects Research:** Evaluated under **45 CFR § 46 Exempt Category 4** (secondary research with pre-existing de-identified datasets).
- **Minor Protections:** Adolescent participants (ages 13–17) are protected under **COPPA** (zero commercial tracking or ad beacons) and **FERPA** (strict air-gapping preventing linkage to official educational records or grade penalties).
- **Anti-Surveillance Covenant:** DLSM models are strictly prohibited from being utilized for punitive academic discipline, employee workplace surveillance, or health insurance underwriting.
- **Protocol Documentation:** See complete [Institutional Review Board (IRB) Protocol & Research Ethics Framework](docs/ETHICS_IRB_PROTOCOL.md) and [Comprehensive Red-Team Security Assessment](docs/RED_TEAM_REPORT.md).
