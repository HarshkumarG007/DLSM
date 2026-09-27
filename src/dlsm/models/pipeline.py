from typing import List, Dict, Any, Tuple
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.dummy import DummyRegressor, DummyClassifier
from sklearn.linear_model import Ridge, LogisticRegression
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from xgboost import XGBRegressor, XGBClassifier

def build_preprocessing_pipeline(
    numeric_features: List[str],
    categorical_features: List[str]
) -> ColumnTransformer:
    """Encapsulates scaling and encoding inside an isolated transformer to prevent data leakage (RULE-006)."""
    transformers = []
    if numeric_features:
        transformers.append(
            ("num", StandardScaler(), numeric_features)
        )
    if categorical_features:
        transformers.append(
            ("cat", OneHotEncoder(drop="first", handle_unknown="ignore", sparse_output=False), categorical_features)
        )
    return ColumnTransformer(transformers=transformers, remainder="drop")

def get_regression_model(model_type: str, random_state: int = 42):
    if model_type == "baseline":
        return DummyRegressor(strategy="mean")
    elif model_type == "ridge":
        return Ridge(alpha=1.0, random_state=random_state)
    elif model_type == "random_forest":
        return RandomForestRegressor(n_estimators=100, max_depth=8, random_state=random_state, n_jobs=-1)
    elif model_type == "xgboost":
        return XGBRegressor(n_estimators=150, max_depth=5, learning_rate=0.05, subsample=0.8, random_state=random_state, n_jobs=-1)
    else:
        raise ValueError(f"Unknown regression model type: {model_type}")

def get_classification_model(model_type: str, random_state: int = 42):
    if model_type == "baseline":
        return DummyClassifier(strategy="most_frequent")
    elif model_type == "logistic":
        return LogisticRegression(C=1.0, max_iter=1000, random_state=random_state)
    elif model_type == "random_forest":
        return RandomForestClassifier(n_estimators=100, max_depth=8, random_state=random_state, n_jobs=-1)
    elif model_type == "xgboost":
        return XGBClassifier(n_estimators=150, max_depth=5, learning_rate=0.05, subsample=0.8, random_state=random_state, n_jobs=-1, eval_metric="mlogloss")
    else:
        raise ValueError(f"Unknown classification model type: {model_type}")
