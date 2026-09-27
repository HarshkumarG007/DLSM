# rules.md — Development Rules & AI Guidelines

**Version:** 1.0 — 2026-09-27

---

## 1. Non-Negotiable Methodological Rules

- **RULE-001:** No feature, interaction term, or formula is written until the real CSV schema for that dataset has been audited (columns, dtypes, missingness). A plausible-sounding formula for a column that doesn't exist is not a placeholder — delete it, don't keep it as an aspiration.
- **RULE-002:** Every supervised model result is reported with its performance on a final holdout set that was set aside before model selection began and touched exactly once. A cross-validation score alone, especially from a dataset in the hundreds-of-rows range, is not sufficient evidence of a real effect — small-N CV accuracy can swing several points in either direction on pure noise.
- **RULE-003:** Every clustering result is reported with its silhouette score and a bootstrap label-stability check. A visually clean PCA/UMAP plot is not evidence of real structure by itself.
- **RULE-004:** Dataset A and Dataset B are never joined row-for-row. There is no shared identifier and no legitimate way to fabricate one. Cross-dataset synthesis happens at the level of comparable constructs, described in prose and shown side-by-side, never as a merged table.
- **RULE-005:** Every derived feature and cluster gets a neutral, descriptive name until analysis substantiates a stronger label. Prefer `self_reported_night_screen_minutes` over `phone_dependency_proxy`; prefer `cluster_2` over `"high-risk phenotype"` until the data — not the variable name — makes that case.
- **RULE-006:** Never state or imply causation. "Associated with," "correlated with," "predictive of in this sample" — never "causes," "leads to," "results in."
- **RULE-007:** State the evidentiary weight of the whole project plainly in every summary: small, self-reported, cross-sectional, convenience-sampled Kaggle data from two non-overlapping populations. This is exploratory pattern-finding, not a contribution to the (already larger, already more rigorous) published literature on this topic.
- **RULE-008:** A null or messy result is a valid, complete, reportable finding — it does not get minimized, buried, or "fixed" by trying another model family until something looks better.

## 2. Statistical & Engineering Rules

- **RULE-009:** Never `fit_transform` on test/holdout data — fit on train, `transform` only elsewhere.
- **RULE-010:** Never drop NaNs without logging the percentage dropped and considering whether missingness looks MCAR, MAR, or MNAR — a systematic pattern in who skips a question is itself a finding, not noise to discard.
- **RULE-011:** Always establish and report a naive baseline (majority class / mean) before any model result is presented — every accuracy number is read relative to it.
- **RULE-012:** Use `random_state=42` (or an explicitly logged seed) everywhere randomness occurs, for reproducibility.
- **RULE-013:** No absolute/hardcoded file paths — everything through `configs/data.yaml`.
- **RULE-014:** Multicollinearity checked (VIF) before interpreting any linear model's coefficients.
- **RULE-015:** Permutation importance and SHAP are computed on validation/holdout data, never on training data.
- **RULE-016:** Every visualization has a title, labeled axes, and a legend where relevant; no pie charts where a bar chart would show the same comparison more clearly.
- **RULE-017:** Mediation analysis results are reported with bootstrapped confidence intervals, and explicitly flagged as testing a statistical pathway under stated assumptions, not establishing temporal or causal order that cross-sectional data can't support.
- **RULE-018:** MLOps tooling (DVC, MLflow, Docker) is optional, adopted only if it earns its complexity against two sub-300KB CSVs — see `architecture.md` §6.
- **RULE-019:** Any claim comparing this project's findings to "the literature" must cite a real, checkable source — not an invented statistic.
- **RULE-020:** A phase in `task.md` is complete only when its acceptance criterion is genuinely true, checked by actually running the code — not narrated as "should be fine."

## 3. What To Avoid

- Do not build the Streamlit dashboard before at least one model has cleared its final-holdout bar — there should be a real number to show, not a placeholder.
- Do not report a "Digital Lifestyle Load" composite score without also reporting its PCA explained variance and loadings, so a reader can judge whether it's capturing something real or mostly noise.
- Do not adopt Optuna, full multi-model tournaments, or deep learning approaches before confirming that simpler models (logistic/RF) don't already explain most of the signal — see `architecture.md` §4's baseline-first ordering.
