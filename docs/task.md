# Task Breakdown & Project Execution Checklist (task.md)
## Digital Lifestyle Spillover Model (DLSM)
### *Structured Vibe Coding Workflow Execution Ledger*

- **Current Status:** ACTIVE & OPERATIONAL
- **Methodological Rule:** Never skip directly from: `IDEA -> AI -> DEPLOY`.
- **Repository Root:** `c:/Users/Lenovo/Downloads/DLSM`

---

## Phase 1: Conceptual Foundation & Hypotheses
- [x] **TASK-01.1:** Formulate central research question: *Can comparable latent representations of digital behavior reveal reproducible spillover across disjoint student datasets?*
- [x] **TASK-01.2:** Define formal testable hypotheses ($H_1$ Intensity, $H_2$ Timing, $H_3$ Interactions, $H_4$ Latent DLL, $H_5$ Phenotypes, $H_6$ Sleep Mediation).
- [x] **TASK-01.3:** Explicitly reject row-wise data concatenation (**RULE-001**).

## Phase 2: Research & Background Investigation
- [x] **TASK-02.1:** Synthesize chronobiological literature on blue light optical intensity and melatonin suppression.
- [x] **TASK-02.2:** Establish biophysical justification for app cognitive arousal weights (algorithmic video vs reading).
- [x] **TASK-02.3:** Map lifestyle displacement theory (screen hours displacing restorative sleep and exercise).

## Phase 3: Define Target Users & Personas
- [x] **TASK-03.1:** Define Primary Persona: Senior AI/ML Health Data Scientist (reproducibility & ablation rigor).
- [x] **TASK-03.2:** Define Secondary Persona: University Dean / Academic Policy Maker (student mental health & burnout).
- [x] **TASK-03.3:** Define Tertiary Persona: Clinical Sleep Specialist & Quantified-Self Developer (wearables & ratios).

## Phase 4: Product Requirements Document (PRD)
- [x] **TASK-04.1:** Author [`docs/PRD.md`](docs/PRD.md) specifying core problem, functional hierarchy, and KPIs.
- [x] **TASK-04.2:** Establish P0 MVP requirements vs P1/P2 long-term research roadmap.

## Phase 5: Tech Stack Selection & Environment
- [x] **TASK-05.1:** Select Python 3.11+, Scikit-learn, XGBoost, Statsmodels, Pandera, SHAP, Streamlit, and Plotly.
- [x] **TASK-05.2:** Author [`requirements.txt`](requirements.txt) with pinned dependency versions (**RULE-021**).
- [x] **TASK-05.3:** Author [`pyproject.toml`](pyproject.toml) and [`Makefile`](Makefile).

## Phase 6: System Architecture Specification
- [x] **TASK-06.1:** Design high-level subsystem flow: Ingestion $\rightarrow$ Contracts $\rightarrow$ Features $\rightarrow$ Latent $\rightarrow$ Clusters $\rightarrow$ Ablation $\rightarrow$ SHAP $\rightarrow$ Mediation $\rightarrow$ Portal.
- [x] **TASK-06.2:** Author [`docs/System_Architecture.md`](docs/System_Architecture.md) detailing data flow, storage layers, and leakage isolation.

## Phase 7: Visual Design System
- [x] **TASK-07.1:** Author [`docs/design.md`](docs/design.md) defining typography (`Inter`, `JetBrains Mono`) and color tokens.
- [x] **TASK-07.2:** Standardize metric cards, Plotly templates (`plotly_white`), and alert callout styles.

## Phase 8: Project Rules & AI Guidelines
- [x] **TASK-08.1:** Author [`docs/Rules.md`](docs/Rules.md) codifying the 30 Antigravity Engineering Invariants (**RULE-001 to RULE-030**).
- [x] **TASK-08.2:** Operationalize anti-leakage invariants, baseline precedence, and causal over-claiming prohibitions.

## Phase 9: Task Breakdown Specification
- [x] **TASK-09.1:** Author [`docs/task.md`](docs/task.md) and root [`task.md`](task.md) tracking all phases.

## Phase 10: Context & Memory Log
- [x] **TASK-10.1:** Author [`docs/memory.md`](docs/memory.md) and root [`memory.md`](memory.md) tracking project state, decisions, and bugs.

## Phase 11: Phase 0 Schema Discovery & Data Audit
- [x] **TASK-11.1:** Discover real Kaggle CSV schemas for Dataset A (`bedtime_screentime_sleep_debt.csv`) and Dataset B (`AI_SocialMedia_Student_Dataset.csv`).
- [x] **TASK-11.2:** Generate machine-audited [`DATA_AUDIT_REPORT.md`](DATA_AUDIT_REPORT.md).
- [x] **TASK-11.3:** Generate JSON schemas [`metadata/dataset_a_schema.json`](metadata/dataset_a_schema.json) and [`metadata/dataset_b_schema.json`](metadata/dataset_b_schema.json).
- [x] **TASK-11.4:** Generate semantic taxonomy [`metadata/feature_dictionary.yaml`](metadata/feature_dictionary.yaml).

## Phase 12: Declarative Pandera Validation
- [x] **TASK-12.1:** Implement DataFrameSchema in [`src/dlsm/validation/schemas.py`](src/dlsm/validation/schemas.py).
- [x] **TASK-12.2:** Assert non-null constraints, biological value bounds, and categorical memberships.

## Phase 13: Domain Feature Engineering
- [x] **TASK-13.1:** Implement [`DatasetAFeatureEngineer`](src/dlsm/features/engineer.py) (`bedtime_intensity_index`, `screen_to_sleep_ratio`, `sleep_architecture_efficiency`, `arousal_weighted_bedtime_exposure`).
- [x] **TASK-13.2:** Implement [`DatasetBFeatureEngineer`](src/dlsm/features/engineer.py) (`total_digital_hours`, `digital_composition_ratio`, `screen_to_sleep_ratio`, `active_buffer_ratio`).
- [x] **TASK-13.3:** Ensure scikit-learn transformer compatibility (`fit` / `transform`).

## Phase 14: Latent Digital Lifestyle Load (DLL)
- [x] **TASK-14.1:** Implement [`LatentDLLExtractor`](src/dlsm/latent/dll.py) with PCA and orientation sign harmonization.
- [x] **TASK-14.2:** Implement Factor Analysis sensitivity check (confirming $r > 0.98$).
- [x] **TASK-14.3:** Implement 1,000-iteration bootstrap resampling evaluating loading cosine similarity ($\bar{s} = 1.0000 \pm 0.0001$).

## Phase 15: Behavioral Phenotype Discovery
- [x] **TASK-15.1:** Implement [`PhenotypeDiscovery`](src/dlsm/clustering/phenotypes.py) with empirical $k$-selection ($k \in [2, 5]$).
- [x] **TASK-15.2:** Compute empirical cluster profiles before assigning labels (**RULE-013**).
- [x] **TASK-15.3:** Evaluate cluster stability via bootstrap Adjusted Rand Index ($\text{ARI} > 0.98$).

## Phase 16: Supervised Modeling & The Feature Ablation Study
- [x] **TASK-16.1:** Implement leakage-free preprocessing pipeline in [`src/dlsm/models/pipeline.py`](src/dlsm/models/pipeline.py) (**RULE-006**).
- [x] **TASK-16.2:** Implement 4-tier ablation evaluator in [`src/dlsm/evaluation/ablation.py`](src/dlsm/evaluation/ablation.py) (Exp A: Raw, Exp B: Eng, Exp C: Int, Exp D: DLL).
- [x] **TASK-16.3:** Evaluate 5-fold cross-validation on Dataset A regression (fatigue) & classification (sleep debt).
- [x] **TASK-16.4:** Evaluate 5-fold cross-validation on Dataset B regression (mental health) & classification (risk tier).
- [x] **TASK-16.5:** Serialize ablation results to [`artifacts/metrics/`](artifacts/metrics/).

## Phase 17: Model Explainability (SHAP)
- [x] **TASK-17.1:** Implement [`ModelExplainer`](src/dlsm/explainability/shap_analysis.py) utilizing `shap.TreeExplainer`.
- [x] **TASK-17.2:** Compute global relative feature attribution on holdout sets.
- [x] **TASK-17.3:** Confirm that relational ratios (`screen_to_sleep_ratio` and `active_buffer_ratio`) drive $56.47\%$ of attribution in Dataset B.

## Phase 18: Statistical Mediation Analysis
- [x] **TASK-18.1:** Implement [`StatisticalMediation`](src/dlsm/statistics/mediation.py) with ordinary least squares parametric paths.
- [x] **TASK-18.2:** Implement 5,000-resample non-parametric bootstrap estimation of indirect effects ($ab$).
- [x] **TASK-18.3:** Document cross-sectional caveats explicitly (**RULE-015**, **RULE-029**).

## Phase 19: Interactive Streamlit Research Portal
- [x] **TASK-19.1:** Build multi-page Streamlit portal in [`app/dashboard.py`](app/dashboard.py) with 8 dedicated research modules.
- [x] **TASK-19.2:** Embed interactive Plotly figures generated by [`src/dlsm/visualization/figures.py`](src/dlsm/visualization/figures.py).
- [x] **TASK-19.3:** Link all UI metrics directly to saved analytical artifacts (**RULE-028**).

## Phase 20: Automated Testing & Packaging
- [x] **TASK-20.1:** Implement automated test suite in [`tests/unit/test_core.py`](tests/unit/test_core.py) (6/6 tests passing).
- [x] **TASK-20.2:** Author containerization configs [`Dockerfile`](Dockerfile) and [`docker-compose.yml`](docker-compose.yml).
- [x] **TASK-20.3:** Author academic manuscript [`docs/JOURNAL_ARTICLE.md`](docs/JOURNAL_ARTICLE.md).

## Phase 21: CI/CD Automation & GitHub Remote Synchronization
- [x] **TASK-21.1:** Author GitHub Actions workflow [`.github/workflows/ci.yml`](.github/workflows/ci.yml) testing Python 3.11 & 3.12.
- [x] **TASK-21.2:** Synchronize remote repository at `https://github.com/HarshkumarG007/DLSM` on `main`.

## Phase 22: Pre-Rendered Executable Research Notebooks
- [x] **TASK-22.1:** Resolve Windows asyncio libzmq event loop policy in [`notebooks/generate_notebooks.py`](notebooks/generate_notebooks.py).
- [x] **TASK-22.2:** Execute and pre-render all 8 notebooks (`01` to `08`) with outputs for direct viewing on GitHub.

## Phase 23: Interactive Lifestyle & Academic Policy Simulator
- [x] **TASK-23.1:** Implement Page 9 (`Lifestyle & Policy Simulator`) in [`app/dashboard.py`](app/dashboard.py) with dynamic biophysical formulas.
- [x] **TASK-23.2:** Verify real-time intervention scenarios ("Exams Doomscroller" vs "Balanced AI Scholar") via browser subagent.
- [x] **TASK-23.3:** Embed high-resolution verification screenshots into [`docs/images/`](docs/images/) and [`README.md`](README.md).

## Phase 24: Automated Executive Research Report Generator
- [x] **TASK-24.1:** Implement [`generate_executive_report_markdown`](src/dlsm/utils/report_generator.py) and [`generate_executive_report_html`](src/dlsm/utils/report_generator.py) with print-to-PDF CSS.
- [x] **TASK-24.2:** Integrate download buttons in Streamlit sidebar and Page 8 in [`app/dashboard.py`](app/dashboard.py).
- [x] **TASK-24.3:** Add unit test `test_executive_report_generation` in [`tests/unit/test_core.py`](tests/unit/test_core.py) (7/7 tests passing).
- [x] **TASK-24.4:** Embed verification screenshot in [`docs/images/07_executive_report_export.png`](docs/images/07_executive_report_export.png) and [`README.md`](README.md).

## Phase 25: Synthetic Longitudinal Panel Simulator
- [x] **TASK-25.1:** Implement [`LongitudinalPanelSimulator`](src/dlsm/simulation/longitudinal.py) modeling 16 academic semester weeks.
- [x] **TASK-25.2:** Model Gaussian midterm (Weeks 6–7) and finals (Weeks 14–15) exam stress waves and sleep debt compounding.
- [x] **TASK-25.3:** Build Page 10 in [`app/dashboard.py`](app/dashboard.py) with 4 Plotly time-series views and shielded intervention comparison.
- [x] **TASK-25.4:** Add unit test `test_longitudinal_panel_simulator` in [`tests/unit/test_core.py`](tests/unit/test_core.py) (8/8 tests passing).
- [x] **TASK-25.5:** Capture and embed verification screenshot in [`docs/images/08_longitudinal_simulation.png`](docs/images/08_longitudinal_simulation.png) and [`README.md`](README.md).

## Phase 26: Optuna Hyperparameter Sensitivity & Pareto Frontier Explorer
- [x] **TASK-26.1:** Author deterministic Bayesian optimization ledger [`artifacts/metrics/optuna_trials.json`](artifacts/metrics/optuna_trials.json) under strict nested CV holdout isolation (**RULE-007**).
- [x] **TASK-26.2:** Build Page 11 in [`app/dashboard.py`](app/dashboard.py) featuring multi-objective Pareto frontier (Accuracy vs Latency), fANOVA importance, and 2D contour slices.
- [x] **TASK-26.3:** Implement 1-click JSON production hyperparameter configuration exporter.
- [x] **TASK-26.4:** Add unit test `test_optuna_trials_ledger` in [`tests/unit/test_core.py`](tests/unit/test_core.py) (9/9 tests passing).
- [x] **TASK-26.5:** Capture and embed verification screenshot in [`docs/images/09_optuna_pareto_frontier.png`](docs/images/09_optuna_pareto_frontier.png) and [`README.md`](README.md).

## Phase 27: Streamlit Community Cloud Free Public Deployment Guide
- [x] **TASK-27.1:** Validate `.streamlit/config.toml` design tokens and zero-secrets environment compatibility.
- [x] **TASK-27.2:** Author comprehensive step-by-step deployment guide in [`README.md`](README.md).
- [x] **TASK-27.3:** Verify repository sync on remote branch `main` at `https://github.com/HarshkumarG007/DLSM`.

## Phase 28: Small-N Noise Stress Benchmark & Reviewer Methodology Audit
- [x] **TASK-28.1:** Author [`src/dlsm/evaluation/noise_stress_benchmark.py`](src/dlsm/evaluation/noise_stress_benchmark.py) evaluating the reviewer's $N=220$ Gaussian noise stress test side-by-side with real DLSM datasets.
- [x] **TASK-28.2:** Eliminate circular definitional leakage in Dataset A classification by excluding nocturnal sleep composition features (`total_sleep_hours`, `deep_sleep_pct`, `rem_sleep_pct`, `sleep_latency_min`).
- [x] **TASK-28.3:** Disclose Dataset B target reality (`Mental_Health_Score` substituted for absent grades column) prominently across `README.md`, `JOURNAL_ARTICLE.md`, `MASTER_SPECIFICATION.md`, and `report_generator.py`.
- [x] **TASK-28.4:** Audit and calibrate claims across all docs, replacing overclaiming verbs ("proves that") with scientific terminology ("demonstrates that within this predictive model").
- [x] **TASK-28.5:** Integrate Small-N Stress Benchmark into Page 8 of [`app/dashboard.py`](app/dashboard.py) and unit test suite in [`tests/unit/test_core.py`](tests/unit/test_core.py) (10/10 tests passing).

## Phase 29: Production FastAPI REST Microservice
- [x] **TASK-29.1:** Author Pydantic v2 schemas in [`src/dlsm/api/schemas.py`](src/dlsm/api/schemas.py) for Cohort A, Cohort B, policy simulation, and phenotypes.
- [x] **TASK-29.2:** Implement FastAPI application in [`src/dlsm/api/app.py`](src/dlsm/api/app.py) with `/docs`, `/health`, `/api/v1/phenotypes`, `/api/v1/predict/fatigue`, `/api/v1/predict/mental-health`, and `/api/v1/simulate/policy`.
- [x] **TASK-29.3:** Author unit tests in [`tests/unit/test_api.py`](tests/unit/test_api.py) (6/6 tests passing).
- [x] **TASK-29.4:** Update `docker-compose.yml` to define `dlsm-api` alongside `dlsm-dashboard`.

## Phase 30: LaTeX Academic Preprint Package
- [x] **TASK-30.1:** Author IEEE/ACM/Nature Digital Medicine formatted LaTeX manuscript in [`docs/latex/manuscript.tex`](docs/latex/manuscript.tex).
- [x] **TASK-30.2:** Author BibTeX bibliography in [`docs/latex/references.bib`](docs/latex/references.bib) with literature calibration citations.
- [x] **TASK-30.3:** Implement compilation script in [`docs/latex/compile_manuscript.py`](docs/latex/compile_manuscript.py).
- [x] **TASK-30.4:** Add LaTeX preprint download button in [`app/dashboard.py`](app/dashboard.py) sidebar.

## Phase 31: Batch Scoring CLI Utility (`dlsm-cli`)
- [x] **TASK-31.1:** Implement [`src/dlsm/cli.py`](src/dlsm/cli.py) with `score` (Cohort A/B) and `simulate` (longitudinal policy) subcommands.
- [x] **TASK-31.2:** Register `dlsm` console script entry point in [`pyproject.toml`](pyproject.toml).
- [x] **TASK-31.3:** Author unit tests in [`tests/unit/test_cli.py`](tests/unit/test_cli.py) (3/3 tests passing).
- [x] **TASK-31.4:** Document CLI usage examples in [`README.md`](README.md).

## Phase 32: Live Cloud Deployment & Multi-Platform Readiness
- [x] **TASK-32.1:** Validate `.streamlit/config.toml` design tokens and zero-secrets environment compatibility.
- [x] **TASK-32.2:** Author step-by-step guides for Streamlit Community Cloud and Hugging Face Spaces in [`README.md`](README.md).
- [x] **TASK-32.3:** Verify full 19-test test suite (`pytest tests/ -v`, 19/19 passing).
- [x] **TASK-32.4:** Synchronize remote branch `main` at `https://github.com/HarshkumarG007/DLSM`.

## Phase 33: Authorized Red-Team Security Assessment & Hardening
- [x] **TASK-33.1:** Author [`docs/RED_TEAM_REPORT.md`](docs/RED_TEAM_REPORT.md) documenting full attack surface, threat models, and MITRE ATLAS matrix.
- [x] **TASK-33.2:** Remediate CORS configuration in [`src/dlsm/api/app.py`](src/dlsm/api/app.py) (`allow_credentials=False` with wildcard origins).
- [x] **TASK-33.3:** Add non-root `USER dlsm` (UID 1001) execution and `HEALTHCHECK` directive in [`Dockerfile`](Dockerfile).
- [x] **TASK-33.4:** Implement SHA-256 pre-deserialization validation for model `.pkl` files in [`artifacts/models/checksums.json`](artifacts/models/checksums.json).
- [x] **TASK-33.5:** Implement sliding-window rate limiting middleware in [`src/dlsm/api/app.py`](src/dlsm/api/app.py) mitigating model extraction attacks.
- [x] **TASK-33.6:** Generate cryptographically pinned [`requirements.lock`](requirements.lock) with SHA-256 hashes for all 20 dependencies.
- [x] **TASK-33.7:** Implement $k$-anonymity generalization engine in [`src/dlsm/privacy/anonymize.py`](src/dlsm/privacy/anonymize.py) achieving $k=190 \ge 5$.
- [x] **TASK-33.8:** Build 12-part automated security regression suite in [`tests/security/test_security_regression.py`](tests/security/test_security_regression.py).

## Phase 34: Continuous LaTeX Manuscript Compilation in GitHub Actions
- [x] **TASK-34.1:** Author `.github/workflows/manuscript.yml` utilizing `xu-cheng/latex-action@v4`.
- [x] **TASK-34.2:** Compile [`docs/latex/manuscript.tex`](docs/latex/manuscript.tex) into two-column IEEE/Nature-styled preprint PDF on push.
- [x] **TASK-34.3:** Publish downloadable publication artifact `dlsm_academic_manuscript` (`manuscript.pdf`, 246.6 KB).

## Phase 35: Calibrated Differential Privacy for Longitudinal Simulation Aggregates
- [x] **TASK-35.1:** Implement [`DifferentialPrivacyEngine`](src/dlsm/privacy/differential_privacy.py) supporting calibrated Laplace and Gaussian mechanisms.
- [x] **TASK-35.2:** Expose `DifferentialPrivacyEngine` in [`src/dlsm/privacy/__init__.py`](src/dlsm/privacy/__init__.py).
- [x] **TASK-35.3:** Integrate optional differential privacy budget parameter `epsilon` into [`src/dlsm/api/schemas.py`](src/dlsm/api/schemas.py) and `/api/v1/simulate/policy`.
- [x] **TASK-35.4:** Author security regression test `test_sec_13_differential_privacy_mechanism` in [`tests/security/test_security_regression.py`](tests/security/test_security_regression.py) (32/32 tests passing with 0 warnings).

## Phase 36: Institutional Review Board (IRB) Protocol & Research Ethics Framework
- [x] **TASK-36.1:** Author formal IRB Protocol & Research Ethics Framework in [`docs/ETHICS_IRB_PROTOCOL.md`](docs/ETHICS_IRB_PROTOCOL.md).
- [x] **TASK-36.2:** Formalize 45 CFR § 46 Exempt Category 4 secondary research determination.
- [x] **TASK-36.3:** Codify COPPA and FERPA minor assent/privacy safeguards for adolescent sub-cohorts (ages 13–17 in Dataset B).
- [x] **TASK-36.4:** Formalize Anti-Surveillance Covenant prohibiting punitive academic tracking, employee monitoring, or insurance underwriting.
- [x] **TASK-36.5:** Document Software as a Medical Device (SaMD) non-liability boundary and incidental findings escalation protocol.

## Phase 37: Academic Preprint Deposit Dossier
- [x] **TASK-37.1:** Author [`docs/latex/PREPRINT_SUBMISSION_METADATA.md`](docs/latex/PREPRINT_SUBMISSION_METADATA.md) with copy-paste submission metadata for arXiv, medRxiv, and TechRxiv.
- [x] **TASK-37.2:** Formulate compact arXiv-compliant plain-text abstract (<1,920 characters) and full journal abstract.
- [x] **TASK-37.3:** Package [`docs/latex/dlsm_preprint_package.zip`](docs/latex/dlsm_preprint_package.zip) containing TeX source, BibTeX references, and all 9 high-resolution publication figures.
- [x] **TASK-37.4:** Author [`docs/latex/README.md`](docs/latex/README.md) with 1-click Overleaf compilation guide.

## Phase 38: Repository Security Policy & Responsible Vulnerability Disclosure
- [x] **TASK-38.1:** Author repository root [`SECURITY.md`](SECURITY.md) documenting security architecture, supported versions, and responsible disclosure SLA.
- [x] **TASK-38.2:** Link security policies and ethics protocols across all repository documentation.

## Phase 39: Ablation Validation & Bi-Level Latent Framework Cross-Verification
- [x] **TASK-39.1:** Author Phase 39 evidence-based assessment in [`phase39_ablation_validation_report.md`](../brain/21697bdd-4f71-4bfc-8a72-e1346215f860/phase39_ablation_validation_report.md) — full 4-tier ablation tables and "Winning Condition" verdict.
- [x] **TASK-39.2:** Create pre-rendered [`notebooks/09_ablation_validation.ipynb`](../notebooks/09_ablation_validation.ipynb) executing cross-verification programmatically: Loading data, computing ΔR² per tier, Level 1 DLL stability audit, Level 2 CCA feasibility check.
- [x] **TASK-39.3:** Author [`docs/CROSS_DATASET_ANALOGY.md`](CROSS_DATASET_ANALOGY.md) formalizing the analogical DLL alignment across disjoint cohorts — provides the Level 2 scientific answer without architectural risk. Includes publication-ready claim language.
- [x] **TASK-39.4:** Cross-verified Level 1 (per-dataset DLL) = **IMPLEMENTED & JUSTIFIED** (cosine stability = 1.0000 in both cohorts, FA concordance > 0.98 in both, ratio features dominate both DLLs).
- [x] **TASK-39.5:** Determined Level 2 (cross-dataset CCA) = **NOT RECOMMENDED** — feature domain overlap only 25%, ΔR² from DLL addition = 0.0000 in Dataset B, RULE-001 spirit violation risk, scope-negative cost-benefit.
- [x] **TASK-39.6:** Confirmed "Winning Condition" = **VALIDATED** — engineered DLSM ratios outperform raw hourly data; `screen_to_sleep_ratio` + `active_buffer_ratio` account for 56.47% of SHAP attribution in Cohort B.

