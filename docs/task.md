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
