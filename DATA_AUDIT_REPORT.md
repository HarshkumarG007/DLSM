# DATA AUDIT REPORT — Digital Lifestyle Spillover Model (DLSM)
**Execution Phase:** Phase 0 — Schema Discovery & Data Quality Validation  
**Date of Execution:** 2026-09-27  
**System Engine:** Antigravity AI ML Research Engineering Framework  
**Repository Working Directory:** `c:/Users/Lenovo/Downloads/DLSM`  

---

## 1. Executive Summary & Audit Mandate

In strict compliance with **RULE-001**, **RULE-002**, and **RULE-003**:
1. **No row-wise merging:** Dataset A and Dataset B originate from distinct data generation processes and disjoint populations. Under no circumstances are individual records merged row-wise.
2. **Zero Schema Fabrication:** Prior to feature engineering, the ground-truth CSV schemas have been discovered directly from the actual Kaggle files:
   - **Dataset A:** `bedtime_screentime_sleep_debt.csv` (8,500 records, 18 columns, 992.74 KB)
   - **Dataset B:** `AI_SocialMedia_Student_Dataset.csv` (16,000 records, 10 columns, 977.75 KB)
3. **Data Integrity:** Both datasets were checked for missing values, duplicates, out-of-bound anomalies, and type mismatches. **Zero missing values (0.00%)** were detected across all 24,500 cumulative rows and 28 cumulative columns.

---

## 2. Dataset A: Bedtime Screen Time & Sleep Debt Telemetry

- **Source File:** `data/raw/dataset_a/bedtime_screentime_sleep_debt.csv`
- **Observations ($N$):** 8,500
- **Variables ($P$):** 18
- **Duplicate Rows:** 0 (0.00%)
- **Overall Missingness:** 0 / 153,000 cells (0.00%)

### 2.1 Complete Variable Profile

| Column Name | Type | Semantic Taxonomy Role | Unique | Missing (%) | Min | Max | Mean | Median | Std | Example Values |
|:---|:---|:---|---:|---:|---:|---:|---:|---:|---:|:---|
| `user_id` | `object` | **IDENTIFIER** | 8500 | 0.0% | — | — | — | — | — | USR-00001, USR-00002, USR-00003 |
| `age` | `int64` | **DEMOGRAPHIC** | 48 | 0.0% | 18.0 | 65.0 | 34.3556 | 32.0 | 11.5843 | 29, 58, 41 |
| `gender` | `object` | **DEMOGRAPHIC** | 3 | 0.0% | — | — | — | — | — | Female, Non-Binary, Male |
| `occupation_type` | `object` | **POTENTIAL_CONFOUNDER** | 5 | 0.0% | — | — | — | — | — | Healthcare / Shift Worker, Student, Remote Tech |
| `chronotype` | `object` | **POTENTIAL_CONFOUNDER** | 3 | 0.0% | — | — | — | — | — | Intermediate, Night Owl, Morning Lark |
| `bedtime_phone_minutes` | `int64` | **DIGITAL_TIMING** | 179 | 0.0% | 1.0 | 180.0 | 59.25 | 51.0 | 36.932 | 179, 163, 100 |
| `primary_bedtime_app` | `object` | **DIGITAL_PURPOSE** | 6 | 0.0% | — | — | — | — | — | Instagram / Reddit, YouTube, TikTok / Reels |
| `screen_brightness_pct` | `int64` | **DIGITAL_INTENSITY** | 91 | 0.0% | 10.0 | 100.0 | 55.1539 | 55.0 | 19.8505 | 54, 76, 59 |
| `blue_light_filter_active` | `int64` | **BEHAVIORAL** | 2 | 0.0% | 0.0 | 1.0 | 0.4678 | 0.0 | 0.499 | 1, 0 |
| `caffeine_post_5pm_mg` | `int64` | **POTENTIAL_CONFOUNDER** | 218 | 0.0% | 0.0 | 250.0 | 33.2225 | 0.0 | 51.9356 | 0, 92, 45 |
| `physical_activity_min` | `int64` | **BEHAVIORAL** | 107 | 0.0% | 0.0 | 112.0 | 35.7014 | 35.0 | 20.8194 | 21, 72, 23 |
| `sleep_latency_min` | `float64` | **SLEEP** | 893 | 0.0% | 6.0 | 123.3 | 40.6715 | 37.6 | 17.4449 | 84.4, 86.7, 70.5 |
| `total_sleep_hours` | `float64` | **SLEEP** | 640 | 0.0% | 3.2 | 9.8 | 6.2662 | 6.33 | 1.4463 | 3.2, 4.06, 6.99 |
| `deep_sleep_pct` | `float64` | **SLEEP** | 172 | 0.0% | 8.1 | 28.0 | 21.7357 | 21.9 | 3.0694 | 23.5, 18.0, 18.1 |
| `rem_sleep_pct` | `float64` | **SLEEP** | 170 | 0.0% | 9.6 | 27.0 | 19.1059 | 19.1 | 2.5465 | 22.2, 21.5, 20.5 |
| `morning_alarm_snoozes` | `int64` | **SLEEP** | 8 | 0.0% | 0.0 | 7.0 | 2.766 | 3.0 | 1.6954 | 7, 1, 4 |
| `next_day_fatigue_score` | `float64` | **TARGET** | 91 | 0.0% | 1.0 | 10.0 | 3.7947 | 3.2 | 2.6852 | 10.0, 1.7, 5.3 |
| `sleep_debt_category` | `object` | **TARGET** | 4 | 0.0% | — | — | — | — | — | Severe Sleep Debt, Mild Deficit, Moderate Debt |

### 2.2 Dataset A Categorical Distributions
- **`gender`**: Female: 4,347 (51.1%), Male: 3,905 (45.9%), Non-Binary: 248 (2.9%)
- **`occupation_type`**: Corporate 9-to-5: 2,838 (33.4%), Remote Tech: 2,142 (25.2%), **Student: 1,622 (19.1%)**, Healthcare / Shift Worker: 997 (11.7%), Freelance / Creative: 901 (10.6%)
- **`chronotype`**: Intermediate: 3,880 (45.6%), Night Owl: 2,455 (28.9%), Morning Lark: 2,165 (25.5%)
- **`primary_bedtime_app`**: TikTok / Reels: 2,198 (25.9%), YouTube: 1,928 (22.7%), Instagram / Reddit: 1,630 (19.2%), Streaming: 1,301 (15.3%), Messaging / Chat: 847 (10.0%), News / Reading: 596 (7.0%)
- **`sleep_debt_category`** (Classification Target): Moderate Debt: 4,462 (52.5%), Mild Deficit: 2,004 (23.6%), Optimal Recovery: 1,387 (16.3%), Severe Sleep Debt: 647 (7.6%)

---

## 3. Dataset B: AI & Social Media Impact on Student Health

- **Source File:** `data/raw/dataset_b/AI_SocialMedia_Student_Dataset.csv`
- **Observations ($N$):** 16,000
- **Variables ($P$):** 10
- **Duplicate Rows:** 0 (0.00%)
- **Overall Missingness:** 0 / 160,000 cells (0.00%)

### 3.1 Complete Variable Profile

| Column Name | Type | Semantic Taxonomy Role | Unique | Missing (%) | Min | Max | Mean | Median | Std | Example Values |
|:---|:---|:---|---:|---:|---:|---:|---:|---:|---:|:---|
| `Student_ID` | `object` | **IDENTIFIER** | 16000 | 0.0% | — | — | — | — | — | STU_00001, STU_00002, STU_00003 |
| `Age` | `int64` | **DEMOGRAPHIC** | 13 | 0.0% | 13.0 | 25.0 | 19.0388 | 19.0 | 3.7653 | 19, 16, 25 |
| `Gender` | `object` | **DEMOGRAPHIC** | 3 | 0.0% | — | — | — | — | — | Male, Non-binary, Female |
| `Education_Level` | `object` | **ACADEMIC** | 3 | 0.0% | — | — | — | — | — | College, High School, University |
| `Daily_Social_Media_Hours` | `float64` | **DIGITAL_INTENSITY** | 1106 | 0.0% | 0.0 | 14.0 | 4.5418 | 4.5 | 2.403 | 5.32, 5.21, 3.61 |
| `Daily_AI_Tool_Usage_Hours` | `float64` | **DIGITAL_INTENSITY** | 762 | 0.0% | 0.0 | 9.5 | 2.5906 | 2.52 | 1.6794 | 1.21, 3.89, 2.65 |
| `Sleep_Hours` | `float64` | **SLEEP** | 752 | 0.0% | 2.0 | 11.15 | 6.5454 | 6.54 | 1.2705 | 7.3, 7.81, 6.34 |
| `Physical_Activity_Hours` | `float64` | **BEHAVIORAL** | 462 | 0.0% | 0.0 | 5.0 | 1.2484 | 1.13 | 1.0386 | 1.41, 2.48, 0.06 |
| `Mental_Health_Score` | `float64` | **TARGET** | 3743 | 0.0% | 32.56 | 91.76 | 72.4932 | 73.75 | 9.2448 | 74.06, 76.13, 65.01 |
| `Physical_Health_Score` | `float64` | **HEALTH** | 3433 | 0.0% | 48.03 | 99.98 | 88.0205 | 89.455 | 9.691 | 98.9, 89.94, 76.75 |

### 3.2 Dataset B Categorical Distributions
- **`Gender`**: Male: 7,744 (48.4%), Female: 7,628 (47.7%), Non-binary: 628 (3.9%)
- **`Education_Level`**: High School: 6,083 (38.0%), University: 5,027 (31.4%), College: 4,890 (30.6%)

---

## 4. Cross-Dataset Correspondence Matrix

The following matrix documents the empirical mapping between conceptual constructs across both disjoint populations:

| Analytical Construct | Dataset A Feature(s) | Dataset B Feature(s) | Comparability Status | Alignment Transformation | Methodological Rationale |
|:---|:---|:---|:---|:---|:---|
| **Digital Intensity** | `screen_brightness_pct`, `bedtime_phone_minutes` | `Daily_Social_Media_Hours`, `Daily_AI_Tool_Usage_Hours` | **Conceptual / Latent** | Within-dataset Z-score standardization | Captures physical and temporal magnitude of digital screen exposure. |
| **Digital Timing / Bedtime Concentration** | `bedtime_phone_minutes` (pre-sleep) | *Absent* | **Dataset A Specific** | Standardized $z$-score in A | Only Dataset A records nocturnal usage specifically before sleep. |
| **Digital Composition / Purpose** | `primary_bedtime_app` (arousal weighting) | `Daily_AI_Tool_Usage_Hours` vs `Daily_Social_Media_Hours` | **Domain-Specific** | Ratio & categorical arousal indexing | Evaluates passive/arousal-inducing content vs active cognitive tool use. |
| **Sleep Duration** | `total_sleep_hours` (mean 6.27h) | `Sleep_Hours` (mean 6.55h) | **Direct Biological** | Standardized hours | Direct metric alignment in nocturnal sleep hours. |
| **Sleep Quality / Architecture** | `sleep_latency_min`, `deep_sleep_pct`, `rem_sleep_pct`, `morning_alarm_snoozes` | *Absent* | **Dataset A Specific** | Multi-indicator sleep disruption index | Dataset A provides physiological sleep stages; Dataset B captures only gross duration. |
| **Physical Activity** | `physical_activity_min` (mean 35.7 min) | `Physical_Activity_Hours` (mean 1.25 hr) | **Direct Behavioral** | Unit conversion: $	ext{hr} = rac{	ext{min}}{60}$ | Both measure physical exercise as a critical lifestyle buffer. |
| **Demographics** | `age`, `gender`, `occupation_type` | `Age`, `Gender`, `Education_Level` | **Direct Demographic** | Categorical encoding, standardization | Enables demographic adjustment and student sub-cohort analysis. |
| **Target Outcomes** | `next_day_fatigue_score` (1-10), `sleep_debt_category` | `Mental_Health_Score` (32.6-91.8), `Physical_Health_Score` (48.0-100) | **Domain End-points** | Continuous regression & stratified risk categories | Examines the downstream cognitive and psychological impacts of digital load. |

---

## 5. Audit Verdict & Clearance for Phase 1

1. **Schema Integrity Verified:** All columns match discovered variables without any synthetic fabrication.
2. **Zero Missingness:** No imputation artifacts are introduced by missing values.
3. **Distribution Checks:** All continuous variables exhibit plausible biological and behavioral bounds (e.g., sleep 2-11h, bedtime screen time 1-180 min, age 13-65).
4. **Phase 1 Pipeline Clearance Granted:** Proceed to measurement model construction, feature engineering pipelines, PCA latent representations, and statistical validation.
