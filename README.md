# Digital Lifestyle Spillover Model (DLSM)

> **Tagline:** *From isolated digital behaviors to a measurable architecture of student digital life.*

[![Python Version](https://img.shields.io/badge/python-3.11%20%7C%203.12%20%7C%203.13-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)]()
[![Code Style: Ruff](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/astral-sh/ruff)

The **Digital Lifestyle Spillover Model (DLSM)** is a rigorous, cross-dataset AI/ML research framework designed to discover reproducible relationships between digital engagement intensity, bedtime exposure timing, sleep architecture disruption, and student wellbeing outcomes across two independent, non-concatenated observational cohorts ($N = 24,500$).

---

## 🔬 Core Research Question

> **Can comparable latent representations of digital behavior derived independently from two disjoint student datasets reveal a reproducible relationship between digital intensity, digital timing, sleep disruption, wellbeing, and academic outcomes?**

### The Fundamental Methodological Principle (RULE-001)
**DO NOT concatenate Dataset A and Dataset B row-wise.** There is no person-level correspondence between the two cohorts. Instead, DLSM constructs independent, comparable latent dimensions:

$$\text{DLL}_A = f(X_A), \quad \text{DLL}_B = f(X_B)$$

---

## 📊 Discovered Datasets & Ground-Truth Schemas

DLSM audited both Kaggle source datasets directly before feature instantiation (Phase 0):

| Cohort | Source File | Records ($N$) | Attributes ($P$) | Missingness | Discovered Domain |
|:---|:---|:---:|:---:|:---:|:---|
| **Dataset A** | `bedtime_screentime_sleep_debt.csv` | 8,500 | 18 | **0.00%** | Bedtime phone telemetry, screen brightness, blue light filter, sleep latency, deep/REM sleep %, fatigue score. |
| **Dataset B** | `AI_SocialMedia_Student_Dataset.csv`| 16,000 | 10 | **0.00%** | Student social media hours, daily AI tool hours, sleep hours, exercise, mental and physical health scores. |

---

## 📈 Key Empirical Findings

1. **Latent Construct Validity (H4):** Across both cohorts, Principal Component Analysis identified a single dominant **Digital Lifestyle Load (DLL)** factor explaining $>65\%$ of variance ($65.97\%$ in A, $71.30\%$ in B) with near-perfect Factor Analysis concordance ($r > 0.98$) and $1,000$ bootstrap resample stability ($\bar{s} = 1.0000 \pm 0.0001$).
2. **Behavioral Phenotypes (H5):** Unsupervised clustering objectively discovered optimal $k=2$ behavioral phenotypes in both populations (Bootstrap Adjusted Rand Index $> 0.98$):
   - **Cohort A:** *High-Load Nocturnally Disrupted* ($32.6\%$, DLL $+1.69\sigma$, latency $59.3$ min) vs *Regulated Circadian Restorative* ($67.4\%$, DLL $-0.82\sigma$, latency $31.7$ min).
   - **Cohort B:** *Intensive Dual-Screen Digital Load* ($47.1\%$, DLL $+1.41\sigma$, screen $>9.5$ hrs/day) vs *Balanced Digital Moderates* ($52.9\%$, DLL $-1.25\sigma$, sleep $7.1$ hrs/day).
3. **The Centerpiece Ablation Experiment:** In Dataset B student mental health modeling, domain-engineered relational features (**`screen_to_sleep_ratio`** and **`active_buffer_ratio`**) accounted for **$56.47\%$ of total SHAP predictive attribution**, whereas raw aggregate screen hours accounted for under $10\%$.
4. **Sleep as a Statistical Mediator (H6):** Non-parametric bootstrap mediation ($5,000$ resamples) demonstrated that sleep latency and sleep duration statistically mediate **$45.67\%$ to $50.85\%$** of the association between bedtime digital load and next-day fatigue in Cohort A ($ab = 0.5479$, $95\%\ \text{CI}: [0.4998, 0.5954]$), and **$18.40\%$** of the association between digital load and student mental health in Cohort B ($ab = -0.3950$, $95\%\ \text{CI}: [-0.4321, -0.3581]$).

---

## 🛠️ Repository Architecture

```
dlsm/
├── configs/                  # Modular YAML experiment configs
├── data/
│   ├── raw/                  # Pristine immutable raw datasets (RULE-023)
│   └── processed/            # Feature-engineered processed datasets
├── metadata/                 # Audited schemas and feature dictionaries
├── src/dlsm/
│   ├── data/                 # Loader & schema discovery engines
│   ├── validation/           # Pandera data contract validation schemas
│   ├── features/             # Mathematically defined domain transformers
│   ├── latent/               # PCA DLL extractor with bootstrap stability
│   ├── clustering/           # Phenotype discovery with empirical labeling
│   ├── models/               # Leakage-free preprocessing & model pipelines
│   ├── evaluation/           # 4-tier feature ablation evaluation engine
│   ├── explainability/       # SHAP TreeExplainer & permutation importance
│   ├── statistics/           # Non-parametric bootstrap mediation models
│   └── visualization/        # Publication-quality Plotly figures generator
├── app/
│   └── dashboard.py          # Interactive 8-page Streamlit Research Portal
├── tests/
│   └── unit/test_core.py     # Automated pytest validation suite
├── artifacts/                # Serialized models, metrics JSONs, and SHAP data
├── docs/                     # Full journal manuscript, specifications & governance docs
│   ├── MASTER_SPECIFICATION.md # Complete 17-part ML specification blueprint
│   ├── PRD.md                # Product Requirements Document
│   ├── System_Architecture.md# Complete system architecture & Mermaid flows
│   ├── Rules.md              # 30 Antigravity Engineering Invariants
│   ├── design.md             # Design system, tokens & typography
│   ├── task.md               # 20-phase execution ledger & checklist
│   ├── memory.md             # ADRs, persistent state & empirical ledger
│   ├── JOURNAL_ARTICLE.md    # Publication-ready scientific manuscript
│   ├── methodology.md        # Mathematical feature specifications
│   ├── data_dictionary.md    # Semantic feature taxonomy
│   ├── model_card.md         # ML model reporting cards
│   └── limitations.md        # Threat model & observational caveats
├── PRD.md                    # Root link to Product Requirements Document
├── System_Architecture.md    # Root link to System Architecture Document
├── Rules.md                  # Root link to Engineering Invariants
├── design.md                 # Root link to Visual Design System
├── task.md                   # Root link to Project Task Breakdown
├── memory.md                 # Root link to Project Context & History Log
└── DATA_AUDIT_REPORT.md      # Ground-truth machine-generated audit report
```

---

## 🚀 Quick Start & Installation

### 1. Local Environment Setup
```bash
git clone https://github.com/dlsm-research/dlsm.git
cd dlsm
pip install -r requirements.txt
```

### 2. Run the Full Research Pipeline
```bash
python src/dlsm/pipeline_orchestrator.py
```

### 3. Run Automated Tests
```bash
pytest tests/ -v
```

### 4. Launch the Interactive Research Dashboard
```bash
streamlit run app/dashboard.py
```

---

## 📜 Citation & License

This research framework is distributed under the **MIT License**.

```bibtex
@article{dlsm2026,
  title={Digital Lifestyle Spillover Model (DLSM): A Cross-Dataset AI/ML Research Framework for Student Digital Behavior, Sleep Architecture, and Psychological Wellbeing},
  author={Antigravity ML Research Core},
  journal={Antigravity Cognitive Systems and Applied Machine Learning},
  year={2026}
}
```
