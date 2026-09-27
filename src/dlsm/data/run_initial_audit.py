import json
import yaml
import numpy as np
import pandas as pd
from pathlib import Path

def audit_dataset(df: pd.DataFrame, dataset_name: str, file_name: str) -> dict:
    row_count, col_count = df.shape
    columns_audit = []
    
    for col in df.columns:
        s = df[col]
        dtype_str = str(s.dtype)
        unique_cnt = int(s.nunique(dropna=True))
        missing_cnt = int(s.isna().sum())
        missing_pct = float((missing_cnt / row_count) * 100.0) if row_count > 0 else 0.0
        
        is_num = pd.api.types.is_numeric_dtype(s)
        
        if is_num:
            s_clean = s.dropna()
            minimum = float(s_clean.min()) if len(s_clean) > 0 else None
            maximum = float(s_clean.max()) if len(s_clean) > 0 else None
            mean_val = float(s_clean.mean()) if len(s_clean) > 0 else None
            median_val = float(s_clean.median()) if len(s_clean) > 0 else None
            std_val = float(s_clean.std()) if len(s_clean) > 0 else None
        else:
            minimum = None
            maximum = None
            mean_val = None
            median_val = None
            std_val = None
            
        # Example values (up to 5 unique non-null samples)
        example_vals = s.dropna().unique()[:5].tolist()
        # Convert any numpy types to python native types
        example_vals = [x.item() if hasattr(x, "item") else x for x in example_vals]
        
        col_info = {
            "dataset_name": dataset_name,
            "file_name": file_name,
            "row_count": row_count,
            "column_count": col_count,
            "column_name": col,
            "dtype": dtype_str,
            "unique_count": unique_cnt,
            "missing_count": missing_cnt,
            "missing_percentage": round(missing_pct, 4),
            "minimum": round(minimum, 4) if minimum is not None else None,
            "maximum": round(maximum, 4) if maximum is not None else None,
            "mean": round(mean_val, 4) if mean_val is not None else None,
            "median": round(median_val, 4) if median_val is not None else None,
            "std": round(std_val, 4) if std_val is not None else None,
            "example_values": example_vals
        }
        columns_audit.append(col_info)
        
    return {
        "dataset_name": dataset_name,
        "file_name": file_name,
        "row_count": row_count,
        "column_count": col_count,
        "columns": columns_audit
    }

def main():
    path_a = Path("data/raw/dataset_a/bedtime_screentime_sleep_debt.csv")
    path_b = Path("data/raw/dataset_b/AI_SocialMedia_Student_Dataset.csv")
    
    print(f"Loading {path_a}...")
    df_a = pd.read_csv(path_a)
    print(f"Dataset A loaded: {df_a.shape}")
    
    print(f"Loading {path_b}...")
    df_b = pd.read_csv(path_b)
    print(f"Dataset B loaded: {df_b.shape}")
    
    audit_a = audit_dataset(df_a, "Dataset A (Bedtime Screen Time & Sleep Debt)", path_a.name)
    audit_b = audit_dataset(df_b, "Dataset B (AI & Social Media Impact on Students)", path_b.name)
    
    with open("metadata/dataset_a_audit.json", "w", encoding="utf-8") as f:
        json.dump(audit_a, f, indent=2)
        
    with open("metadata/dataset_b_audit.json", "w", encoding="utf-8") as f:
        json.dump(audit_b, f, indent=2)
        
    print("\n--- DATASET A COLUMNS ---")
    for c in audit_a["columns"]:
        print(f"  {c['column_name']} ({c['dtype']}): unique={c['unique_count']}, missing={c['missing_percentage']}%, range=[{c['minimum']}, {c['maximum']}], mean={c['mean']}, examples={c['example_values'][:3]}")
        
    print("\n--- DATASET B COLUMNS ---")
    for c in audit_b["columns"]:
        print(f"  {c['column_name']} ({c['dtype']}): unique={c['unique_count']}, missing={c['missing_percentage']}%, range=[{c['minimum']}, {c['maximum']}], mean={c['mean']}, examples={c['example_values'][:3]}")

if __name__ == "__main__":
    main()
