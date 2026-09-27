# Development Rules & Engineering Invariants (Rules.md)
## Digital Lifestyle Spillover Model (DLSM)
### *Authoritative AI Agent Constitution, Vibe Coding Governance & 30 Antigravity Invariants*

- **Document Version:** 1.0.0
- **Status:** ACTIVE & BINDING
- **Scope:** All AI agents, contributors, data engineers, ML engineers, and analytical pipelines.
- **Repository Root:** `c:/Users/Lenovo/Downloads/DLSM`

---

## 1. Core Operating Philosophy: The Vibe Coding Workflow

All work within the DLSM repository adheres strictly to the fundamental principle:

$$\boxed{\text{NEVER SKIP DIRECTLY FROM: } \text{IDEA} \longrightarrow \text{AI} \longrightarrow \text{DEPLOY}}$$

Before writing or modifying any implementation code, every agent or developer must:
1. **Understand First:** Audit schemas, examine empirical distributions, review scientific objectives, and inspect data boundaries.
2. **Design Before Execution:** Formalize hypotheses, define mathematical feature representations, establish baselines, and design leakage-free validation splits.
3. **Execute Incrementally:** Progress methodically through data ingestion, Pandera schema validation, feature engineering, latent extraction, baseline evaluation, ensemble modeling, SHAP explainability, and bootstrap mediation.
4. **Verify Rigorously:** Ensure zero data leakage, check 100% test pass rates, verify bootstrap stability, and link every dashboard metric back to serialized artifacts.

---

## 2. The 30 Antigravity Engineering Invariants

The following 30 rules are non-negotiable architectural constraints. Any violation halts the pipeline and invalidates experimental runs.

### Section I: Data Integrity & Cross-Dataset Governance
- **RULE-001 (Zero Row-Wise Merging):** Under NO circumstances concatenate or join Dataset A and Dataset B row-wise. Cohort A and Cohort B represent distinct, disjoint populations (cross-sectional bedtime phone users vs secondary/university students) with no shared entity identifiers. Synthesis occurs exclusively at the latent feature and inferential evidence levels.
- **RULE-002 (Zero Synthetic Entities):** Never fabricate synthetic primary keys, foreign keys, or pseudo-entity IDs to force cross-cohort record linkage.
- **RULE-003 (Empirical Schema Auditing):** Always inspect and audit real CSV schemas directly from the raw files before writing feature engineering or model training code. Never assume or hallucinate column names.
- **RULE-004 (Transparent Missingness Handling):** Never drop missing values silently (`dropna()`) without logging the exact missingness percentage and evaluating the missingness mechanism (MCAR vs MAR vs MNAR). (Audited Kaggle datasets: 0.00% missing).
- **RULE-005 (Immutable Pipeline Logging):** Every data transformation, cleaning step, and outlier clipping operation must be logged to a machine-readable audit report or log file.

### Section II: Preprocessing & Anti-Leakage Invariants
- **RULE-006 (Strict Pipeline Encapsulation):** Never invoke `fit_transform()` on validation or test sets. All feature scalers (`StandardScaler`, `RobustScaler`), categorical encoders (`OneHotEncoder`), and imputers must be encapsulated inside Scikit-learn `Pipeline` or `ColumnTransformer` objects, fitted strictly on training folds, and applied via `transform()` to evaluation folds.
- **RULE-007 (Holdout Isolation):** Never tune hyperparameters on the final holdout test set. All hyperparameter exploration (Optuna, GridSearchCV) must execute strictly within nested cross-validation folds on the development partition.
- **RULE-008 (Baseline Precedence):** Always establish a naive data-derived baseline (`DummyRegressor(strategy='mean')` or `DummyClassifier(strategy='most_frequent')`) before implementing complex machine learning models.
- **RULE-009 (Justified Complexity):** Never deploy tree ensembles or gradient boosted algorithms (Random Forest, XGBoost) without explicitly demonstrating statistical $\Delta \text{Performance}$ over regularized linear models (Ridge, Logistic Regression).
- **RULE-010 (Documented Feature Formulations):** Every engineered feature must have a documented mathematical formula, biophysical or behavioral rationale, and predefined bounds in `metadata/feature_dictionary.yaml`.

### Section III: Latent Construction & Unsupervised Clustering
- **RULE-011 (Interpretable Latent Dimensions):** Every latent dimension (e.g., Digital Lifestyle Load - DLL) must have inspectable, interpretable factor loadings. Component vectors must be verified for sign consistency with positive digital exposure.
- **RULE-012 (Bootstrap Latent Stability):** Never equate a mathematical principal component with a theoretical construct (DLL) without verifying:
  1. Eigenvalue $\lambda > 1.0$ (Kaiser-Guttman criterion).
  2. Proportion of explained variance $> 60\%$.
  3. Resampling stability over $\ge 1,000$ bootstrap iterations (mean cosine similarity $\bar{s} > 0.95$ with zero sign inversions).
  4. Concordance with exploratory Factor Analysis ($r > 0.90$).
- **RULE-013 (Empirical Phenotype Profiling):** Never assign descriptive cluster labels (e.g., "High-Load Nocturnally Disrupted") *a priori*. Labels may only be assigned after inspecting post-clustering centroids, empirical distributions, and statistical separation across all features.
- **RULE-014 (Non-Arbitrary Cluster Selection):** Do not arbitrarily choose cluster count $k$. Evaluate $k \in [2, 5]$ across multiple indices (Silhouette score, Calinski-Harabasz, Davies-Bouldin) and verify cluster stability via bootstrap Adjusted Rand Index ($\text{ARI} > 0.90$).

### Section IV: Explainable AI & Statistical Inference
- **RULE-015 (Observational Mediation Caveat):** Never claim causal mediation in cross-sectional observational data. All mediation pathways must be explicitly designated as *statistical mediation* compatible with hypothesized relationships, acknowledging potential unmeasured confounding and lack of temporal precedence.
- **RULE-016 (Holdout Attribution Evaluation):** Compute SHAP attributions and permutation feature importances strictly on holdout validation folds or test sets, never on training data where overfitted noise can inflate importance.
- **RULE-017 (In-Fold Resampling):** Any class rebalancing (SMOTE, class weighting) or distribution calibration must occur strictly within training folds to prevent target distribution leakage into evaluation folds.
- **RULE-018 (Bootstrap Uncertainty Intervals):** Always report 95% bootstrap confidence intervals for primary indirect effects, metric improvements, and latent stability parameters.
- **RULE-019 (Multiple Testing Correction):** When conducting multiple pairwise hypothesis tests or screening correlation matrices, apply Benjamini-Hochberg False Discovery Rate (FDR) adjustments controlling family-wise type I error at $\alpha = 0.05$.

### Section V: Engineering Rigor, Reproducibility & MLOps
- **RULE-020 (Deterministic Reproducibility):** Set global random seeds (`random_state=42`, `np.random.seed(42)`) across all stochastic operations (splitting, PCA bootstrapping, K-Means initialization, XGBoost training).
- **RULE-021 (Pinned Dependencies):** Pin all runtime environments and package dependencies in `requirements.txt` and `pyproject.toml`.
- **RULE-022 (Cryptographic Raw Data Hashing):** Compute and log SHA-256 cryptographic checksums for raw input datasets to guarantee immutability.
- **RULE-023 (Immutable Raw Data):** Never modify, overwrite, or truncate raw CSV files in place. All transformations must output to `data/interim/`, `data/processed/`, or `artifacts/`.
- **RULE-024 (Vectorized Computational Efficiency):** Implement transformations using vectorized Pandas and NumPy operations. Prohibit row-wise iterations (`iterrows()`, `apply()` with row loops) on large tabular frames.
- **RULE-025 (Empirical Weight Sensitivity):** Do not use arbitrary subjective weights in composite indices without conducting and documenting sensitivity analyses across varying weight configurations.
- **RULE-026 (Transparent Negative Findings):** Never suppress or conceal null results, negative findings, or failed hypotheses. If a feature does not improve cross-validation performance, record the negative result in the ablation matrix.
- **RULE-027 (Ablation-Driven Justification):** Supervised modeling must follow the 4-tier experimental ablation progression (Exp A: Raw, Exp B: Engineered, Exp C: Interactions, Exp D: Latent DLL). Every tier's incremental contribution must be quantified via $\Delta R^2$ or $\Delta \text{F1}$.
- **RULE-028 (Decoupled Artifact Governance):** All frontend dashboard components, visual charts, and summary cards must consume precomputed, serialized artifacts from `artifacts/`. The UI layer must never execute heavy training or cross-validation loops directly.
- **RULE-029 (Association vs Causation Distinction):** In all documentation, manuscripts, UI labels, and agent responses, strictly distinguish statistical association from causal determination. Avoid using causal verbs ("causes", "drives", "creates") unless describing theoretical hypotheses or simulation assumptions.
- **RULE-030 (Transparent Blocker Escalation):** If data topology or statistical assumptions cannot support a requested analysis, report the blocker and assumption failure transparently rather than applying ad-hoc workarounds.

---

## 3. Code Standards & Architectural Conventions

### 3.1 Python & PEP 8 Standards
- Target Python runtime: **Python 3.11+** (compatible with 3.13).
- Strictly adhere to PEP 8 formatting standards:
  - 4 spaces per indentation level (no tabs).
  - Explicit type annotations on all public functions, classes, and methods.
  - Descriptive docstrings conforming to the Google or NumPy docstring format.
  - Function lengths generally under 60 lines, single-responsibility principle.

### 3.2 Testing Standards
- Pytest must be maintained at **100% pass rate** at all times.
- Unit tests must cover:
  - Pandera schema validation (valid and invalid inputs).
  - Feature engineering transformers (handling zero division, boundary checks).
  - Latent DLL sign harmonization and stability checks.
  - Leakage prevention (ensuring test fold statistics do not alter train fold parameters).
  - Bootstrap statistical mediation calculations.

### 3.3 Artifact Directory Standards
All generated model binaries, metrics, and visual figures must reside in structured paths:
- `artifacts/models/`: Serialized pipelines, estimators, and scalers (`.pkl`).
- `artifacts/metrics/`: Ablation CSVs, latent analysis JSONs, mediation JSONs.
- `artifacts/shap/`: Precomputed SHAP feature attribution rankings (`.csv`).
- `artifacts/figures/`: Interactive standalone Plotly figures (`.html`).
- `artifacts/reports/`: Data audit logs and validation summaries.

---

## 4. Scientific Integrity Checklist for AI Agents

Before submitting code, reports, or PRs, verify:
- [ ] Has Dataset A and Dataset B remained strictly separate without row-wise merging?
- [ ] Were scalers and encoders fit strictly on training folds inside a `Pipeline`?
- [ ] Has a naive baseline been established before reporting tree ensemble metrics?
- [ ] Does PC1 meet the Kaiser-Guttman criterion ($\lambda > 1.0$) and $>60\%$ variance?
- [ ] Are cluster labels assigned strictly *after* inspecting centroid values?
- [ ] Are mediation findings explicitly described as observational statistical mediation?
- [ ] Are all dashboard figures and tables reading directly from `artifacts/`?
- [ ] Are all tests passing with zero errors (`pytest tests/ -v`)?
