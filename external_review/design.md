# design.md — Design System

**Version:** 1.0 — 2026-09-27
**Scope note:** unlike a chat-bot interface, this project has a real visual surface (the Streamlit dashboard), so this file keeps its standard brief rather than needing reinterpretation.

---

## 1. Core Design Principles

1. **Every chart earns its place by showing uncertainty, not just a point estimate.** A bar chart of cluster sizes without a silhouette score annotation is incomplete by this project's own rules.
2. **Colorblind-accessible by default**, not as an afterthought.
3. **Tufte's data-ink ratio**: no decorative gradients, no 3D effects, no chart-junk. The finding should be legible without the styling doing any persuasive work on its own.
4. **Neutral visual framing matches neutral naming (rules.md RULE-005).** Don't render "high digital use" clusters in alarming red and "low use" in reassuring green before the data has said anything about which is actually associated with worse outcomes.

## 2. Color Palette

| Role | Color | Note |
|---|---|---|
| Primary categorical (up to 4 groups) | Okabe-Ito palette (`#E69F00`, `#56B4E9`, `#009E73`, `#D55E00`) | Colorblind-safe, standard in scientific visualization |
| Neutral background | `#FFFFFF` / `#0E1117` (Streamlit's own light/dark defaults) | Don't fight the framework's theme system |
| Emphasis (a single highlighted result) | `#333333` (dark grey), not red/green | Avoids implying good/bad before the finding warrants it |

## 3. Typography & Layout

- Streamlit's default font stack — no custom font loading for an internal analysis tool.
- One finding per section, in this order: **claim → chart → uncertainty/caveat → sample size.** Sample size is never omitted, given how load-bearing it is here (see `PRD.md` §3).

## 4. Chart Type Guidelines

| Data shape | Chart |
|---|---|
| Distribution of a single continuous variable | Histogram + KDE overlay |
| Correlation among many variables | Heatmap, Spearman by default (state if Pearson is used instead and why) |
| Cluster visualization | 2D PCA or UMAP projection, always shown alongside the silhouette score in the same figure caption, not a separate page |
| Model comparison across the baseline→tuned progression | Grouped bar chart: CV score vs. **holdout score** side by side for every model — never holdout alone or CV alone |
| SHAP summary | Standard SHAP beeswarm/violin plot — don't reskin it |

## 5. What to Avoid

- No pie charts (RULE-016).
- No single number ("Digital Lifestyle Load: 7.2") presented without its scale, distribution, and what a high vs. low score means in context.
- No dashboard interactivity (adjustable feature weights, live re-clustering) before the underlying models/clusters are validated — an interactive toy on top of an unvalidated model just makes the invalid result easier to explore, not more correct.
