import json
from pathlib import Path

def create_notebook(title, cells, target_file):
    nb = {
        "cells": cells,
        "metadata": {
            "language_info": {"name": "python", "version": "3.11.0"}
        },
        "nbformat": 4,
        "nbformat_minor": 2
    }
    with open(target_file, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=2)

def make_cell(cell_type, source_text):
    cell = {
        "cell_type": cell_type,
        "metadata": {},
        "source": [line + "\n" for line in source_text.split("\n")]
    }
    if cell_type == "code":
        cell["outputs"] = []
        cell["execution_count"] = None
    return cell

def generate_all_notebooks():
    nb_dir = Path("notebooks")
    nb_dir.mkdir(parents=True, exist_ok=True)
    
    # Notebook 1: Audit Dataset A
    cells_1 = [
        make_cell("markdown", "# 01 - Dataset A Audit & Schema Discovery\nDigital Lifestyle Spillover Model (DLSM)\n\nAudit of Bedtime Screen Time & Sleep Debt Telemetry."),
        make_cell("code", "import pandas as pd\nimport json\n\ndf_a = pd.read_csv('../data/raw/dataset_a/bedtime_screentime_sleep_debt.csv')\nprint(f'Dataset A Shape: {df_a.shape}')\ndf_a.head()")
    ]
    create_notebook("01_audit_a", cells_1, nb_dir / "01_audit_a.ipynb")

    # Notebook 2: Audit Dataset B
    cells_2 = [
        make_cell("markdown", "# 02 - Dataset B Audit & Schema Discovery\nDigital Lifestyle Spillover Model (DLSM)\n\nAudit of Student AI & Social Media Health & Grades Dataset."),
        make_cell("code", "import pandas as pd\n\ndf_b = pd.read_csv('../data/raw/dataset_b/AI_SocialMedia_Student_Dataset.csv')\nprint(f'Dataset B Shape: {df_b.shape}')\ndf_b.head()")
    ]
    create_notebook("02_audit_b", cells_2, nb_dir / "02_audit_b.ipynb")

    # Notebook 3: Cross-Dataset Mapping
    cells_3 = [
        make_cell("markdown", "# 03 - Cross-Dataset Construct Mapping\nDigital Lifestyle Spillover Model (DLSM)\n\nMapping comparable latent constructs across Population A and Population B without row-wise merging (RULE-001)."),
        make_cell("code", "import yaml\nwith open('../metadata/feature_dictionary.yaml', 'r') as f:\n    feat_dict = yaml.safe_load(f)\nimport pandas as pd\npd.DataFrame(feat_dict['cross_dataset_correspondence'])")
    ]
    create_notebook("03_cross_dataset_mapping", cells_3, nb_dir / "03_cross_dataset_mapping.ipynb")

    # Notebook 4: Feature Engineering
    cells_4 = [
        make_cell("markdown", "# 04 - Domain Feature Engineering & Latent Load Extraction\nDigital Lifestyle Spillover Model (DLSM)\n\nConstructing optical indices, screen-to-sleep ratios, and Latent DLL."),
        make_cell("code", "import sys\nfrom pathlib import Path\nsys.path.insert(0, str(Path('..').resolve() / 'src'))\nimport pandas as pd\nfrom dlsm.features.engineer import DatasetAFeatureEngineer, DatasetBFeatureEngineer\nfrom dlsm.latent.dll import LatentDLLExtractor\n\ndf_a = pd.read_csv('../data/raw/dataset_a/bedtime_screentime_sleep_debt.csv')\nfe_a = DatasetAFeatureEngineer()\ndf_a_eng = fe_a.transform(df_a)\nprint('Dataset A engineered columns:', df_a_eng.columns.tolist())")
    ]
    create_notebook("04_feature_engineering", cells_4, nb_dir / "04_feature_engineering.ipynb")

    # Notebook 5: Clustering & Phenotype Discovery
    cells_5 = [
        make_cell("markdown", "# 05 - Behavioral Phenotype Discovery\nDigital Lifestyle Spillover Model (DLSM)\n\nUnsupervised profiling with K-Means, multi-metric k-selection, and bootstrap stability (ARI)."),
        make_cell("code", "import json\nwith open('../artifacts/metrics/clustering_phenotypes.json', 'r') as f:\n    cl_data = json.load(f)\nimport pandas as pd\npd.DataFrame(cl_data['dataset_a']['mean_profiles'])")
    ]
    create_notebook("05_clustering", cells_5, nb_dir / "05_clustering.ipynb")

    # Notebook 6: Supervised Modeling & Ablation
    cells_6 = [
        make_cell("markdown", "# 06 - Supervised Modeling & The Feature Ablation Study\nDigital Lifestyle Spillover Model (DLSM)\n\nComparing predictive performance across Exp A (Raw), Exp B (Eng), Exp C (Int), and Exp D (Full DLL)."),
        make_cell("code", "import pandas as pd\nablation_a = pd.read_csv('../artifacts/metrics/ablation_regression_dataset_a.csv')\nablation_b = pd.read_csv('../artifacts/metrics/ablation_regression_dataset_b.csv')\nprint('Dataset A Fatigue Prediction Ablation:')\ndisplay(ablation_a)\nprint('Dataset B Mental Health Prediction Ablation:')\ndisplay(ablation_b)")
    ]
    create_notebook("06_modeling", cells_6, nb_dir / "06_modeling.ipynb")

    # Notebook 7: Explainability (SHAP)
    cells_7 = [
        make_cell("markdown", "# 07 - Explainability (SHAP & Permutation Importance)\nDigital Lifestyle Spillover Model (DLSM)\n\nTreeExplainer global importance and feature attribution analysis."),
        make_cell("code", "import pandas as pd\nshap_a = pd.read_csv('../artifacts/shap/shap_importance_dataset_a.csv')\nshap_b = pd.read_csv('../artifacts/shap/shap_importance_dataset_b.csv')\nprint('Top 5 Features in Dataset A:')\ndisplay(shap_a.head(5))\nprint('Top 5 Features in Dataset B:')\ndisplay(shap_b.head(5))")
    ]
    create_notebook("07_xai", cells_7, nb_dir / "07_xai.ipynb")

    # Notebook 8: Statistical Mediation
    cells_8 = [
        make_cell("markdown", "# 08 - Statistical Mediation Pathways\nDigital Lifestyle Spillover Model (DLSM)\n\nBootstrap-based indirect effect estimation (5,000 resamples) with observational caveats."),
        make_cell("code", "import json\nwith open('../artifacts/metrics/mediation_analysis.json', 'r') as f:\n    med_data = json.load(f)\nimport pandas as pd\nprint('Mediation Summary in Dataset A:')\nprint(json.dumps(med_data['dataset_a']['latency_mediator'], indent=2))")
    ]
    create_notebook("08_mediation", cells_8, nb_dir / "08_mediation.ipynb")

    print("All 8 research notebooks successfully created in notebooks/")

if __name__ == "__main__":
    generate_all_notebooks()
