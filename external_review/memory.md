# memory.md — Project Context & History Log

---

## Current Status

**Phase:** Step 1 of Vibe Coding Workflow complete (PRD, architecture, rules, design, task breakdown written). No real CSVs uploaded yet, no code run against real data.
**Last updated:** 2026-09-27

## Key Technical Decisions

| Date | Decision | Why |
|---|---|---|
| 2026-09-27 | Schema audit made the explicit, blocking first task, ahead of any feature engineering | Both source planning documents specify features (e.g., a melatonin-suppression formula assuming brightness/filter-active columns) that a small self-report survey dataset of this genre almost certainly doesn't contain — verified against a comparable real Kaggle dataset (104 rows, 6 mostly Yes/No columns) found while preparing this document |
| 2026-09-27 | Mandatory final-holdout requirement added to every supervised model result | A quick synthetic stress test on pure-noise data sized like a real comparable dataset (N=220) still produced a "best" cross-validated model at 59% accuracy against a 50% baseline, with the true holdout coming back even higher (68%) — on a target with zero real signal. Small-N accuracy numbers are not trustworthy without this check |
| 2026-09-27 | Mandatory cluster stability check (silhouette + bootstrap) added | Same stress test: K-Means on pure noise still produced silhouette scores around 0.14-0.16 and reasonably balanced cluster sizes for k=2 through 5 — visually indistinguishable from a "real" phenotype discovery without the score reported alongside it |
| 2026-09-27 | Neutral feature/cluster naming convention adopted | Names like "phone_dependency_proxy" or "digital_intrusion_score" imply the conclusion before the analysis runs |
| 2026-09-27 | Project defaults to "exploratory portfolio analysis," not "novel research contribution" framing | Real published work on this topic (550-1,170 participant studies) reports "moderate" associations, not dramatic ones — two sub-300KB Kaggle CSVs should be held to at least that level of epistemic humility |
| 2026-09-27 | MLOps tooling (DVC/MLflow/Docker) downgraded from mandatory to optional | Disproportionate to the actual data scale; a plain experiments.csv log is the default |

## Known Risks (standing checklist)

- [ ] Real schemas not yet seen — every feature/construct name in this doc set is provisional until Phase 0 of `task.md` completes
- [ ] Small N may mean no supervised model clears the holdout bar at all, and no cluster passes the stability check — both are valid, complete, reportable outcomes, not failures to route around
- [ ] Framing risk: any output shared publicly on "AI/social media harms students" needs the evidentiary-weight caveat attached every time, not just once in an introduction that gets skipped

## Major Bugs

*(none yet — no code run against real data)*

## Architectural Changes

*(none yet — initial architecture)*
