# Institutional Review Board (IRB) Protocol & Research Ethics Framework

**Project Title:** Digital Lifestyle & Sleep Matrix (DLSM): Latent Behavioral Phenotyping and Longitudinal Biophysical Simulation  
**Protocol Identification:** DLSM-IRB-2026-V1  
**Lead Investigator:** DLSM Principal Research Team  
**Review Status:** Protocol Prepared for Institutional Ethics Committee / IRB Review  
**Applicable Regulations:** US 45 CFR § 46 (Common Rule), FERPA (34 CFR Part 99), COPPA (15 U.S.C. §§ 6501–6506), EU GDPR (Regulation 2016/679, Articles 6 & 9)

---

## 1. Executive Summary & Protocol Overview

The Digital Lifestyle & Sleep Matrix (DLSM) research initiative evaluates the mechanistic relationships between nocturnal digital screen exposure, cognitive arousal, circadian chronotype, and restorative sleep architecture across collegiate and secondary educational cohorts.

Because predictive computational frameworks can inadvertently generate psychological labeling, behavioral profiling, or re-identification vulnerabilities, this document formalizes the **Ethical Architecture, Human Subject Protections, Regulatory Determinations, and Data Governance Protocols** governing all current and prospective DLSM analyses, deployments, and publications.

---

## 2. Regulatory Classification & Human Subjects Research Determination

### 2.1 Common Rule (45 CFR § 46) Evaluation

- **Classification:** **Exempt Category 4 (Secondary Research on Pre-existing Data)**.
- **Statutory Authority:** Under 45 CFR § 46.104(d)(4), secondary research uses of identifiable private information or identifiable biospecimens are exempt if:
  1. The data are publicly available or lawfully collected under prior research authorization;
  2. Information is recorded by the investigator in such a manner that the identity of the human subjects cannot readily be ascertained directly or through identifiers linked to the subjects;
  3. The investigator does not contact the subjects and will not re-identify subjects.
- **Application to DLSM:**
  - **Dataset A (General Adult Cohort, $N=1,000$):** Pre-collected cross-sectional biophysical telemetry.
  - **Dataset B (Student Mental Health & AI Usage Cohort, $N=1,000$):** De-identified survey records spanning secondary and tertiary students.
  - **Intervention Status:** Non-interventional, observational secondary modeling. No physical or pharmaceutical interventions are administered.

### 2.2 Prospective Deployment Thresholds

If the DLSM simulation engine or API is deployed prospectively in an active educational institution to collect real-time student telemetry:

- Full Institutional Review Board (Expedited or Convened Committee) review is **mandatory** prior to instrumentation.
- Prospective deployments cannot claim Category 4 exemption and require informed consent protocols as delineated in Section 4.

---

## 3. Vulnerable Populations & Minor Protection (Ages 13–17)

Dataset B incorporates student respondents aged 13 through 17. The protocol mandates multi-tier protections for adolescent participants:

### 3.1 Children’s Online Privacy Protection Act (COPPA, 15 U.S.C. §§ 6501–6506)

- **Zero Commercial Tracking:** DLSM code contains no third-party trackers, ad beacons, fingerprinting scripts, or commercial telemetry.
- **Parental/Guardian Assent Safeguard:** For any primary prospective data collection involving participants under 18:
  - Verifiable Parental Consent (VPC) must be collected prior to account creation or sensor telemetry collection.
  - Minor Assent forms must be authored in age-appropriate, transparent language explaining what screen and sleep metrics are observed.

### 3.2 Family Educational Rights and Privacy Act (FERPA, 34 CFR Part 99)

- **Air-Gapped Student Information Systems (SIS):** DLSM strictly disallows ingesting or mapping data to Official Educational Records (e.g., student GPA, transcript grades, attendance disciplinary logs, or IEP records).
- **Prohibition on Grade-Based Predictive Penalties:** The DLSM academic spillover index is purely a conceptual biophysical simulation. It must never be utilized by institutional personnel to assign academic grades or trigger academic probation.

---

## 4. Privacy Architecture, De-Identification & Mathematical Anonymity

DLSM enforces defense-in-depth mathematical privacy preservation to mitigate linkage and reconstruction attacks:

```
[ Raw Student Survey / Telemetry ]
               │
               ▼
[ Direct Identifier Strip ] ──► (Purges Student_ID, user_id, device IDs)
               │
               ▼
[ k-Anonymity Generalization ] ──► (Bins Age into 5-yr cohorts, restricts k >= 5)
               │
               ▼
[ Differential Privacy Noise ] ──► (Laplace / Gaussian noise calibrated to Δf / ε)
               │
               ▼
[ Research API / Cloud Dashboard / Public Repositories ]
```

### 4.1 Direct Identifier Removal

- All direct identifiers (`user_id`, `Student_ID`, names, email addresses, IP addresses, GPS coordinates, device MAC addresses) are stripped at the ingestion pipeline boundary (`src/dlsm/data/loader.py`).

### 4.2 $k$-Anonymity Guarantees ($k \ge 5$)

- Quasi-identifiers (Age, Gender, Education Level, Daily Screen Exposure) are generalized into discrete equivalence classes (`src/dlsm/privacy/anonymize.py`).
- Every quasi-identifier combination published or exported in research artifacts is guaranteed to contain at least $k=5$ indistinguishable individuals, preventing deanonymization via external population registry cross-referencing.

### 4.3 Differential Privacy for Simulation Queries

- Aggregate longitudinal simulation endpoints implement calibrated Laplace and Gaussian perturbation (`src/dlsm/privacy/differential_privacy.py`).
- With global sensitivity $\Delta f$ calculated across cohort sizes $N \ge 50$ and total privacy budget $\epsilon \le 1.0$, query results ensure that an adversary with infinite auxiliary knowledge cannot determine the presence or absence of a single student's record.

---

## 5. GDPR Special Category Data & Health Privacy (Article 9)

### 5.1 Special Category Classification

- Fatigue indicators, REM/deep sleep architecture, and subjective mental health ratings reflect health-adjacent cognitive states.
- Under EU GDPR Article 9(1), processing of biometric and health-related data is prohibited unless qualified by an explicit exemption.

### 5.2 Legal Basis for Processing (Article 9(2)(j))

- **Research Exemption:** Processing is conducted exclusively for scientific and statistical research purposes in the public interest.
- **Proportionality & Purpose Limitation:** Data collected is strictly limited to variables essential for testing circadian and digital load hypotheses.
- **Storage Limitation & Right to Erasure:** Aggregated model weights do not store individual participant records. In prospective settings, participants retain the right to withdraw and have raw records expunged within 30 days of request.

---

## 6. Algorithmic Fairness, Non-Discrimination & Anti-Surveillance Covenants

### 6.1 Prohibited Dual-Use Cases (Anti-Surveillance Covenant)

DLSM models and code are explicitly prohibited from being deployed for:

1. **Academic Discipline & Punitive Tracking:** Using screen time or sleep predictions to penalize students, withhold financial aid, or enforce compulsory study curfews.
2. **Workplace Employee Monitoring:** Ingesting employee mobile sensor data to rank workplace productivity or justify termination.
3. **Insurance Underwriting & Actuarial Rating:** Using predicted fatigue scores or sleep architecture efficiency to alter health or life insurance premiums.

### 6.2 Demographic Parity & Chronotype Fairness

- Models are audited across chronotype sub-populations (Morning Lark, Intermediate, Night Owl).
- Because late-phase chronotypes ("Night Owls") naturally experience social jetlag, thresholding models must not label normal circadian delay as inherent pathology.
- Evaluation metrics are reported disaggregated across demographic strata in the publication model cards (`docs/model_card.md`).

---

## 7. Software as a Medical Device (SaMD) & Clinical Non-Liability Boundary

### 7.1 FDA / CE MDR Regulatory Positioning

- DLSM is an **academic research modeling framework**, **NOT** Software as a Medical Device (SaMD), clinical decision support software (CDS), or a diagnostic medical device under FDA 21 U.S.C. § 360j(o) or EU Medical Device Regulation (MDR 2017/745).
- Predictions (e.g., fatigue score $1.0–10.0$, mental health score $0–100$) do not constitute DSM-5 psychiatric diagnoses (e.g., Major Depressive Disorder, Generalized Anxiety Disorder, Clinical Insomnia).

### 7.2 Mandatory Clinical Disclaimer

All user interfaces, API responses, and documentation artifacts must prominently feature the following disclosure:

> **Research Disclaimer:** _DLSM predictive scores and simulations are intended strictly for educational, scientific, and behavioral research purposes. They do not constitute clinical psychological or medical diagnoses, prognoses, or treatment plans. Individuals experiencing chronic exhaustion, severe sleep disruption, or mental health distress should consult a licensed healthcare professional._

### 7.3 Incidental Findings & Critical Risk Escalation Protocol

In prospective institutional pilots where live student surveys are evaluated:

- If a participant’s score crosses predefined acute distress thresholds (e.g., severe mental health crisis markers), the system **must not** attempt automated psychiatric triage.
- The interface must immediately display accessible, confidential, non-coercive support resources (e.g., 988 Suicide & Crisis Lifeline, university counseling contact directories).

---

## 8. Data Governance, Security & Cryptographic Integrity

To maintain research data integrity and prevent unauthorized exfiltration:

| Layer                       | Control Implemented                                                             | Verification Mechanism       |
| :-------------------------- | :------------------------------------------------------------------------------ | :--------------------------- |
| **API Transport Security**  | Optional env-driven `X-API-Key` authentication & sliding-window rate limiting   | `test_sec_01`, `test_sec_10` |
| **Model Weight Integrity**  | Pre-deserialization SHA-256 hash checks on all trained `.pkl` models            | `test_sec_06`                |
| **Container Isolation**     | Non-root execution (`USER dlsm`, UID 1001), automated container healthchecks    | `test_sec_08`                |
| **Supply-Chain Security**   | Cryptographically pinned dependency lockfile (`requirements.lock` with SHA-256) | `test_sec_12`                |
| **Differential Privacy**    | Calibrated Laplace & Gaussian mechanisms for longitudinal aggregates            | `test_sec_13`                |
| **Continuous Verification** | Automated security regression test suite integrated into CI/CD                  | `.github/workflows/ci.yml`   |

---

## 9. Ethics Committee Review & Protocol Audit Checklist

Before initiating external trials or submitting to institutional grant bodies, investigators must verify compliance with the following protocol checkpoints:

- [x] Secondary research data confirmed fully de-identified with no direct keys.
- [x] $k$-anonymity verification passing ($k \ge 5$, retention $> 95\%$).
- [x] Differential privacy engine active and verified for aggregate simulation endpoints.
- [x] Clear non-diagnostic clinical disclaimer embedded in all user interfaces and APIs.
- [x] Explicit prohibition against punitive administrative surveillance documented.
- [x] Minor protections (COPPA / FERPA) established for adolescent sub-cohorts.
- [x] Cryptographic model provenance verified against SHA-256 integrity ledger.

---

**Protocol Sign-off & Institutional Governance:**  
_DLSM Collaborative Research Consortium_  
_Principal Investigator Verification Date: Academic Year 2026_  
_Inquiries & Ethics Compliance: See repository root [SECURITY.md](file:///c:/Users/Lenovo/Downloads/DLSM/SECURITY.md) and [docs/RED_TEAM_REPORT.md](file:///c:/Users/Lenovo/Downloads/DLSM/docs/RED_TEAM_REPORT.md)._
