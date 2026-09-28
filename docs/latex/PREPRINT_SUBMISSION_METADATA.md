# Preprint Submission Metadata Dossier
### *Digital Lifestyle Spillover Model (DLSM)*
**Target Repositories:** arXiv (`cs.AI` / `cs.CY` / `q-bio.NC`), medRxiv (Digital Health / Epidemiology), TechRxiv (IEEE)  
**Submission Package Archive:** `docs/latex/dlsm_preprint_package.zip` (4.05 MB)  
**Primary Manuscript TeX Source:** `docs/latex/manuscript.tex`  
**Reference Bibliography:** `docs/latex/references.bib`  

---

## 1. Core Bibliographic Metadata (Copy-Paste Ready)

### 1.1 Article Title
```text
Digital Lifestyle Spillover Model (DLSM): A Multi-Cohort AI/ML Research Framework for Student Digital Behavior, Sleep Architecture, and Psychological Wellbeing
```

### 1.2 Running / Short Title (for Headers & Footers)
```text
Digital Lifestyle Spillover Model (DLSM)
```

### 1.3 Author Information & Affiliations
- **Author 1 (Lead & Corresponding Author):**
  - **Full Name:** Harsh Kumar Gupta
  - **Email:** `hrslsha007@gmail.com`
  - **Primary Affiliation:** Advanced AI/ML Systems & Cognitive Informatics Laboratory
  - **Secondary Affiliation:** Antigravity AI Research Core
  - **Country:** India
  - **Role:** Conceptualization, Methodology, Software, Formal Analysis, Writing – Original Draft & Review
- **Consortium / Research Group (Optional):**
  - **Collaborative Group:** DLSM Cognitive & Behavioral Informatics Consortium
  - **Repository URL:** [https://github.com/HarshkumarG007/DLSM](https://github.com/HarshkumarG007/DLSM)
  - **Live Web Application:** [https://dlsm-research.streamlit.app](https://dlsm-research.streamlit.app)

---

## 2. Abstract Text

### 2.1 Full Abstract (for medRxiv, TechRxiv, BioRxiv & Journal Submission)
```text
Modern student life is defined by pervasive digital interaction spanning social media feeds, algorithmic video, and generative artificial intelligence tools. While aggregate screen-time has traditionally served as a crude proxy in behavioral studies, it fails to capture critical dimensions such as temporal exposure concentration, biophysical optical intensity, and behavioral composition. Here, we present the Digital Lifestyle Spillover Model (DLSM), a rigorous, cross-dataset AI/ML research framework designed to synthesize latent digital behavior constructs across two disjoint, non-concatenated observational cohorts (N_total = 24,500): Dataset A (N = 8,500, polysomnographic lifestyle telemetry) and Dataset B (N = 16,000, student AI and social media academic wellbeing; Target disclosure: Dataset B contains no grades or GPA column; Mental_Health_Score serves as the empirical supervised target, while downstream academic impacts are framed conceptually based on cognitive spillover literature).

Rather than executing an invalid row-wise merge across distinct populations, DLSM constructs independent, comparable latent dimensions of Digital Lifestyle Load (DLL) via Principal Component Analysis (PCA) with Factor Analysis (FA) sensitivity checking and 1,000 bootstrap resample stability validation. Across both populations, a single dominant latent factor emerged accounting for >65% of behavioral variance (65.97% in Dataset A, 71.30% in Dataset B) with near-perfect Factor Analysis concordance (r > 0.98) and bootstrap cosine similarity stability (mean similarity = 1.0000). Unsupervised behavioral profiling identified two reproducible phenotypes in each cohort (Bootstrap Adjusted Rand Index ARI > 0.98): a High-Load Nocturnally Disrupted profile vs a Regulated Circadian Restorative profile in Cohort A, and an Intensive Dual-Screen Digital Load profile vs a Balanced Digital Moderates profile in Cohort B.

In a systematic 4-tier feature ablation experiment across linear models, Random Forests, and XGBoost, domain-engineered relational features—most notably the Screen-to-Sleep Ratio and Active Buffer Ratio—dominated model explainability, accounting for 56.47% of total SHAP predictive attribution in Cohort B, while raw aggregate hours accounted for under 10%. Non-parametric bootstrap mediation analysis (5,000 resamples) demonstrated that sleep architecture parameters statistically mediate 45.67% to 50.85% of the total association between digital load and next-day fatigue in Cohort A (ab = 0.5479, 95% CI: [0.4998, 0.5954]), and 18.40% of the relationship between digital load and student mental health in Cohort B (ab = -0.3950, 95% CI: [-0.4321, -0.3581]). Crucially, side-by-side benchmarking against a Gaussian noise control demonstrated that DLSM's cluster topology reflects genuine empirical structure (ARI > 0.98 vs 0.269 on noise). While cross-sectional constraints preclude causal certainty, these findings provide quantitative evidence that relational lifestyle composition contains far greater predictive signal than isolated exposure volume.
```

### 2.2 Compact Abstract (< 1,920 Characters, arXiv Form Compliant)
```text
Aggregate screen-time is widely used to study student wellbeing, yet it obscures critical dimensions such as temporal concentration, optical intensity, and behavioral composition. We present the Digital Lifestyle Spillover Model (DLSM), an AI/ML framework analyzing digital lifestyle, restorative sleep architecture, and psychological wellbeing across two disjoint cohorts (N = 24,500). Rejecting invalid row-wise dataset concatenation, DLSM constructs independent latent factors of Digital Lifestyle Load (DLL) explaining >65% of behavioral variance across cohorts, verified via 1,000 bootstrap resamples (cosine similarity = 1.0000) and Factor Analysis sensitivity checking (r > 0.98). Unsupervised clustering identifies distinct, highly stable behavioral phenotypes in both populations (Bootstrap Adjusted Rand Index > 0.98). In systematic 4-tier ablation benchmarking across linear models, Random Forests, and XGBoost, domain-engineered relational features—particularly the Screen-to-Sleep Ratio and Active Buffer Ratio—accounted for 56.47% of SHAP attribution, outperforming raw hourly exposure. Non-parametric bootstrap mediation analysis (5,000 resamples) demonstrates that sleep architecture parameters statistically mediate 45.67%-50.85% of the digital load-to-fatigue association in Cohort A and 18.40% of the digital load-to-mental health relationship in Cohort B. Benchmarking against Gaussian noise controls confirms authentic empirical cluster topology. While observational limits preclude causal claims, results demonstrate that relational lifestyle composition carries significantly higher predictive signal than raw exposure duration. Code, models, and interactive dashboard are open source.
```
*(Character count: ~1,850 characters — strictly within arXiv's 1,920-character limit).*

---

## 3. Repository Classification & Subject Taxonomies

### 3.1 arXiv (Cornell University)
- **Primary Subject Category:** `cs.AI` (Artificial Intelligence)
- **Cross-List Categories:**
  - `cs.CY` (Computers and Society)
  - `cs.LG` (Machine Learning)
  - `cs.HC` (Human-Computer Interaction)
  - `q-bio.NC` (Quantitative Biology: Neurons and Cognition)
- **ACM Computing Classification (2012):**
  - *Applied computing ~ Health informatics*
  - *Applied computing ~ Psychology*
  - *Computing methodologies ~ Supervised learning / Machine learning approaches*
  - *Security and privacy ~ Mathematical foundations of cryptography / Differential privacy*
- **Comments Field:**
  ```text
  12 pages, 9 figures, 6 tables. Full source code, differential privacy engine, reproducible pipelines, and interactive deployment available at https://github.com/HarshkumarG007/DLSM
  ```

### 3.2 medRxiv (Cold Spring Harbor Laboratory / BMJ / Yale)
- **Subject Category:** `Epidemiology` or `Public and Global Health` or `Digital Health`
- **Manuscript Type:** Research Article
- **Has this manuscript been published elsewhere?** No
- **Clinical Trial Registration:** Not Applicable (Observational Secondary Analysis)
- **Data Availability:** "All data analyzed in this study are derived from pre-existing de-identified research cohorts. Code, trained models, and anonymized datasets are available at https://github.com/HarshkumarG007/DLSM."

### 3.3 TechRxiv (IEEE)
- **Primary Field of Interest:** `Engineering in Medicine and Biology`
- **Secondary Fields of Interest:**
  - `Computing and Processing (Computer Science)`
  - `Human-Centered Computing`
  - `Signal Processing`
- **Keywords:**
  ```text
  Circadian disruption, digital lifestyle load, sleep architecture, latent factor modeling, behavioral phenotypes, machine learning, XGBoost, SHAP explainability, statistical mediation, differential privacy, adolescent health informatics
  ```

---

## 4. Legal, Ethical & Regulatory Disclosures

### 4.1 Ethics Approval & Human Subjects Protection
```text
The study protocol was evaluated under 45 CFR § 46.104(d)(4) (Common Rule, Exempt Category 4: Secondary Research on Pre-existing De-identified Data). Direct identifiers were purged prior to analysis. Adolescent sub-cohorts (ages 13–17) are governed by COPPA and FERPA protections ensuring zero commercial tracking and complete air-gapping from institutional educational records. A comprehensive Institutional Review Board (IRB) Protocol & Research Ethics Framework is formalized in docs/ETHICS_IRB_PROTOCOL.md.
```

### 4.2 Conflict of Interest / Financial Disclosure
```text
The authors declare that they have no competing financial interests, commercial affiliations, or personal relationships that could have appeared to influence the work reported in this paper.
```

### 4.3 Funding Statement
```text
This research received no specific grant from any funding agency in the public, commercial, or not-for-profit sectors. Computational resources and development sandbox environments were independently maintained.
```

### 4.4 License & Distribution
- **Recommended License:** Creative Commons Attribution 4.0 International (CC-BY 4.0).
- Allows unencumbered academic dissemination, quotation, and reproducibility while preserving full author attribution.

---

## 5. Submission Package Manifest (`dlsm_preprint_package.zip`)

The archive `docs/latex/dlsm_preprint_package.zip` is pre-packaged and self-contained for direct upload:

| File in Archive | Description | Role in TeX Engine |
| :--- | :--- | :--- |
| `main.tex` | Alias entry point for arXiv / Overleaf root detection | Main compilation root |
| `manuscript.tex` | Primary complete manuscript source code | Core LaTeX manuscript body |
| `references.bib` | Curated BibTeX database with peer-reviewed literature | Bibliography citation source |
| `README.md` | One-click Overleaf and local compilation guide | Author instructions |
| `figures/01_dashboard_overview.png` | Architecture & Multi-Cohort Analytical Overview | Figure 1 in text |
| `figures/02_latent_dll_construction.png` | Latent Factor Scree & Cosine Stability Curves | Figure 2 in text |
| `figures/03_behavioral_phenotypes.png` | Phenotype Clusters (Radar & PCA Projection) | Figure 3 in text |
| `figures/04_model_explainability_shap.png` | SHAP Summary Plots (Beeswarm & Feature Importance) | Figure 4 in text |
| `figures/05_statistical_mediation.png` | Bootstrap Indirect Effect Distributions | Figure 5 in text |
| `figures/06_lifestyle_policy_simulator.png` | 16-Week Longitudinal Simulation Trajectories | Figure 6 in text |
| `figures/07_executive_report_export.png` | Executive Governance Report Template | Figure 7 in text |
| `figures/08_longitudinal_simulation.png` | Policy Shielding Comparative Dynamics | Figure 8 in text |
| `figures/09_optuna_pareto_frontier.png` | Multi-Objective Hyperparameter Optimization Pareto Frontier | Figure 9 in text |

---

## 6. One-Click Upload Instructions

### 6.1 arXiv Upload
1. Log in at [arxiv.org/submit](https://arxiv.org/submit).
2. Select **Upload Files** and provide `docs/latex/dlsm_preprint_package.zip`.
3. arXiv automatically extracts the zip and recognizes `main.tex`.
4. In the Metadata step, copy-paste the **Title**, **Compact Abstract** (Section 2.2), and select `cs.AI` as Primary.
5. In the Comments step, enter: `12 pages, 9 figures, 6 tables. Reproducible code at https://github.com/HarshkumarG007/DLSM`.
6. Preview the generated PDF and confirm submission.

### 6.2 medRxiv Upload
1. Log in at [medrxiv.org](https://www.medrxiv.org).
2. Create New Submission and upload the compiled PDF (`manuscript.pdf`) or TeX bundle.
3. Paste the **Full Abstract** (Section 2.1).
4. Select Category: `Digital Health` or `Epidemiology`.
5. Enter the Ethics & Data Availability statements from Section 4.

### 6.3 TechRxiv (IEEE) Upload
1. Log in at [techrxiv.org](https://www.techrxiv.org).
2. Upload `manuscript.pdf` and select **Preprint**.
3. Paste the Title, Full Abstract, and Keywords from Section 3.3.
4. Select Field: `Engineering in Medicine and Biology`.
