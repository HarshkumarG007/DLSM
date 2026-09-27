# task.md — Task Breakdown

**Version:** 1.0 — 2026-09-27
**How to use:** work top to bottom. Nothing in Phase 2 onward starts until Phase 0 is genuinely done — not "probably fine," actually checked.

---

## Phase 0 — Schema Audit (blocks everything else)
- [ ] Upload the real Dataset A CSV (Sleep Debt & Screen Time)
- [ ] Upload the real Dataset B CSV (AI & Social Media Impact)
- [ ] Run a schema audit on each: column names, dtypes, missingness %, cardinality, a 10-row sample printed in full
- [ ] Compare the real schemas against every feature name proposed in the source planning documents; delete or rewrite any that assume a column that doesn't exist
- [ ] Write `docs/data_card_a.md` and `docs/data_card_b.md`: row count, column list with plain descriptions, known quality issues

## Phase 1 — Independent EDA
- [ ] Dataset A: distributions, missingness pattern (MCAR/MAR/MNAR judgment), outlier check
- [ ] Dataset B: same
- [ ] Report both honestly even if nothing interesting turns up — a boring EDA is still a complete deliverable

## Phase 2 — Cross-Dataset Construct Mapping
- [ ] For each construct (e.g., "nighttime digital engagement"), identify which real column(s) in each dataset plausibly operationalize it
- [ ] Explicitly list constructs that CANNOT be mapped from the real columns — this list matters as much as the ones that can
- [ ] No row-level join is created at any point in this phase (rules.md RULE-004)

## Phase 3 — Feature Engineering (only real columns, from here on)
- [ ] Engineer features named and defined per the audited schema, not the original proposal's assumed one
- [ ] Log which originally-proposed features had to be dropped or renamed and why (`memory.md`)

## Phase 4 — Supervised Modeling
- [ ] Reserve a final holdout split for each dataset, before any model selection begins
- [ ] Baseline (naive) → Logistic/Linear → Random Forest → (optional) gradient boosting
- [ ] Report CV score AND holdout score for every model, side by side
- [ ] Only proceed to SHAP/explainability for a model that clears the holdout bar meaningfully above baseline

## Phase 5 — Clustering / Phenotypes
- [ ] Run clustering across a range of k
- [ ] Report silhouette score and bootstrap label-stability for every k tried
- [ ] Only name/describe cluster archetypes if the stability check actually supports distinct, reproducible groups — otherwise report that no stable phenotype structure was found, honestly

## Phase 6 — Mediation Analysis
- [ ] Only attempt this if Phase 4 found a real (holdout-confirmed) association to explain
- [ ] Report bootstrapped confidence intervals, and the explicit statement that this tests a statistical pathway, not temporal/causal order

## Phase 7 — Dashboard
- [ ] Build only after Phases 4-6 have real, validated numbers to show
- [ ] Every panel includes its sample size and uncertainty measure per `design.md`

## Phase 8 — Write-Up
- [ ] State plainly what this analysis can and cannot support (PRD.md §3, §7)
- [ ] Compare findings to the real published literature on this topic, cited properly, not just asserted
