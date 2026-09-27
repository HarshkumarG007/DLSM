# PRD.md — Product Requirements Document

**Project:** Digital Lifestyle Spillover Model (DLSM)
**Version:** 1.0 — 2026-09-27
**Status:** Step 1 of the Vibe Coding Workflow — pre-development, pre-data-audit

---

## 1. Product Overview

An exploratory, cross-dataset data science project examining whether digital-behavior patterns (screen time, night use, social media/AI use) show statistical association with sleep and, separately, with student health/academic outcomes -- using two disjoint public Kaggle datasets that do not share subjects.

## 2. Core Problem

Two real, related questions currently sit in two different datasets that don't share people. The project's actual contribution is a defensible way to relate findings from one population to findings from another, without pretending they're the same subjects -- not a bigger model, a more honest bridge.

## 3. Who This Is For (decide this explicitly before continuing)

This document defaults to treating the project as a rigorous, honestly-scoped exploratory analysis for a portfolio/learning purpose -- not a claim to original peer-reviewed science. That default matters: real published work on this exact question (social media/screen use vs. academic performance, samples of 550-1,170 participants) describes its own findings as showing a moderate influence, not a dramatic or settled one, with the best-performing model in one such study reaching roughly 81% accuracy against baseline (source cited in the accompanying chat response). Two small Kaggle CSVs are not going to out-power that literature. If the actual goal is to publish this as a genuine research contribution, that's a different, higher evidentiary bar than what follows, and worth stating explicitly rather than discovering later.

## 4. What This Product Is Not

- Not a causal claim generator. Every output states association, never "causes."
- Not a data-merging exercise. Datasets A and B are never joined row-for-row -- see rules.md RULE-004.
- Not a foregone conclusion. "Digital use is harmful" is a hypothesis to test, not the framing to build features around -- see design.md on neutral naming.

## 5. MVP Features (in order -- later ones are blocked by earlier ones)

| # | Feature | Blocked by |
|---|---|---|
| 1 | Schema audit of both real CSVs (columns, dtypes, missingness, cardinality) | Nothing -- this is first |
| 2 | Independent EDA of each dataset | #1 |
| 3 | Cross-dataset construct mapping (conceptual, not row-level) | #2 |
| 4 | Baseline to tuned supervised models, each with a genuine final holdout | #3 |
| 5 | Clustering, gated on a stability check (silhouette + bootstrap agreement), not just "does K-Means run" | #3 |
| 6 | Mediation analysis, heavily caveated | #4, #5 |
| 7 | Streamlit dashboard presenting findings with their actual evidentiary weight stated, not hidden | #6 |

## 6. Explicit Non-Goal (until the real schemas are seen)

No feature name, formula, or cluster archetype is finalized before the actual CSVs are uploaded and audited. Both source planning documents for this project already state this principle and then violate it in their own detail (e.g., a melatonin_suppression_risk = brightness x time x (1 - filter_active) formula assumes device-sensor columns that a small self-report survey dataset of this kind essentially never contains -- a comparable real Kaggle sleep/screen-time dataset found while preparing this document has 104 rows and 6 mostly Yes/No columns, nothing like brightness sensor logs). Don't repeat that mistake here.

## 7. Success Criteria

- Every reported number traces to a script that ran against the real data, not an assumed schema.
- Every supervised model result is reported alongside its true-holdout number, not just cross-validation.
- Every cluster claim is reported alongside its stability metric.
- The final write-up states plainly what this analysis can and cannot support, calibrated against the comparable published literature, not just an internal disclaimer.
