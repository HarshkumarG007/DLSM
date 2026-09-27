from pathlib import Path
import pandas as pd
from dlsm.utils.helpers import setup_logger

logger = setup_logger("dlsm.data.loader")

PATH_DATASET_A = Path("data/raw/dataset_a/bedtime_screentime_sleep_debt.csv")
PATH_DATASET_B = Path("data/raw/dataset_b/AI_SocialMedia_Student_Dataset.csv")

def load_dataset_a(path: Path | str = PATH_DATASET_A) -> pd.DataFrame:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Dataset A not found at: {p.resolve()}")
    df = pd.read_csv(p)
    logger.info(f"Loaded Dataset A ({p.name}) with shape {df.shape}")
    return df

def load_dataset_b(path: Path | str = PATH_DATASET_B) -> pd.DataFrame:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Dataset B not found at: {p.resolve()}")
    df = pd.read_csv(p)
    logger.info(f"Loaded Dataset B ({p.name}) with shape {df.shape}")
    return df

def get_student_cohort_a(df_a: pd.DataFrame) -> pd.DataFrame:
    """Extracts student sub-population from Dataset A for matched-cohort comparison."""
    if "occupation_type" not in df_a.columns:
        raise ValueError("Column 'occupation_type' required to filter student cohort in Dataset A.")
    student_df = df_a[df_a["occupation_type"] == "Student"].copy()
    logger.info(f"Extracted Student sub-cohort from Dataset A: {student_df.shape[0]} students ({student_df.shape[0]/len(df_a)*100:.1f}%)")
    return student_df
