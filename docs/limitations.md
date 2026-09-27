# DLSM Threat Model & Methodological Limitations

## 1. Cross-Sectional Observational Constraints
Neither Dataset A nor Dataset B collected longitudinal time-series data from repeated student measurements. Consequently:
- **Zero Proof of Causal Directionality:** We cannot rule out reverse causality (e.g., students experiencing higher distress or insomnia may secondarily turn to social media or AI platforms as coping mechanisms).
- **Statistical vs Causal Mediation:** All mediation models are designated strictly as *statistical mediation* compatible with hypothesized pathways, not proved causal mechanisms (**RULE-015**, **RULE-029**).

## 2. Measurement Errors & Self-Report Bias
- Dataset B measures digital exposure and sleep duration via self-reported daily hours. Subjective recall tends to underestimate fragmented screen checks and overestimate active continuous focus.
- Polysomnographic sleep stage percentages in Dataset A derive from commercial or simulated telemetry, which may carry sensor noise relative to clinical laboratory electroencephalography (EEG).

## 3. Unobserved Confounders
While models adjust for chronological age, gender, chronotype, and physical exercise, other unmeasured variables may confound the observed relationships:
- Baseline academic workload and examination stress.
- Socioeconomic status and family living environment.
- Underlying clinical depressive or anxiety disorders.

## 4. Rejection of Cross-Cohort Row-Wise Merging
Dataset A ($N=8,500$) and Dataset B ($N=16,000$) represent distinct populations. DLSM strictly adheres to **RULE-001** and rejects row-wise concatenation. Findings between the cohorts reflect complementary segments of a conceptual evidence graph rather than entity-level joint observations.
