from typing import List, Dict, Any, Tuple
import numpy as np
import pandas as pd
from sklearn.model_selection import KFold, StratifiedKFold
from sklearn.metrics import (
    mean_absolute_error,
    root_mean_squared_error,
    r2_score,
    roc_auc_score,
    f1_score,
    balanced_accuracy_score,
    precision_score,
    recall_score
)
from dlsm.models.pipeline import build_preprocessing_pipeline, get_regression_model, get_classification_model
from dlsm.utils.helpers import setup_logger

logger = setup_logger("dlsm.evaluation.ablation")

class AblationEvaluator:
    """
    Executes systematic feature ablation experiments (A -> B -> C -> D)
    strictly within cross-validation folds to prevent information leakage (RULE-006).
    """
    def __init__(self, random_state: int = 42, cv_folds: int = 5):
        self.random_state = random_state
        self.cv_folds = cv_folds

    def evaluate_regression(
        self,
        df: pd.DataFrame,
        feature_sets: Dict[str, Tuple[List[str], List[str]]],
        target_col: str,
        model_types: List[str] = ["baseline", "ridge", "random_forest", "xgboost"]
    ) -> pd.DataFrame:
        kf = KFold(n_splits=self.cv_folds, shuffle=True, random_state=self.random_state)
        results = []
        y = df[target_col].values
        
        for exp_id, (num_cols, cat_cols) in feature_sets.items():
            all_cols = num_cols + cat_cols
            X_df = df[all_cols].copy()
            
            for m_type in model_types:
                maes, rmses, r2s = [], [], []
                
                for train_idx, val_idx in kf.split(X_df, y):
                    X_train, X_val = X_df.iloc[train_idx], X_df.iloc[val_idx]
                    y_train, y_val = y[train_idx], y[val_idx]
                    
                    preprocessor = build_preprocessing_pipeline(num_cols, cat_cols)
                    model = get_regression_model(m_type, self.random_state)
                    
                    # Encapsulated Pipeline fit
                    X_tr_proc = preprocessor.fit_transform(X_train)
                    X_va_proc = preprocessor.transform(X_val)
                    
                    model.fit(X_tr_proc, y_train)
                    preds = model.predict(X_va_proc)
                    
                    maes.append(mean_absolute_error(y_val, preds))
                    rmses.append(root_mean_squared_error(y_val, preds))
                    r2s.append(r2_score(y_val, preds))
                    
                res_record = {
                    "experiment": exp_id,
                    "model": m_type,
                    "feature_count": len(all_cols),
                    "mae_mean": round(float(np.mean(maes)), 4),
                    "mae_std": round(float(np.std(maes)), 4),
                    "rmse_mean": round(float(np.mean(rmses)), 4),
                    "rmse_std": round(float(np.std(rmses)), 4),
                    "r2_mean": round(float(np.mean(r2s)), 4),
                    "r2_std": round(float(np.std(r2s)), 4),
                }
                results.append(res_record)
                logger.info(f"[{exp_id}] [{m_type}] R2: {res_record['r2_mean']:.4f} (+/- {res_record['r2_std']:.4f}), MAE: {res_record['mae_mean']:.4f}")
                
        res_df = pd.DataFrame(results)
        return res_df

    def evaluate_classification(
        self,
        df: pd.DataFrame,
        feature_sets: Dict[str, Tuple[List[str], List[str]]],
        target_col: str,
        model_types: List[str] = ["baseline", "logistic", "random_forest", "xgboost"]
    ) -> pd.DataFrame:
        skf = StratifiedKFold(n_splits=self.cv_folds, shuffle=True, random_state=self.random_state)
        results = []
        y_raw = df[target_col].values
        classes = np.unique(y_raw)
        class_to_idx = {c: i for i, c in enumerate(classes)}
        y = np.array([class_to_idx[c] for c in y_raw])
        
        for exp_id, (num_cols, cat_cols) in feature_sets.items():
            all_cols = num_cols + cat_cols
            X_df = df[all_cols].copy()
            
            for m_type in model_types:
                f1s, bal_accs, aucs = [], [], []
                
                for train_idx, val_idx in skf.split(X_df, y):
                    X_train, X_val = X_df.iloc[train_idx], X_df.iloc[val_idx]
                    y_train, y_val = y[train_idx], y[val_idx]
                    
                    preprocessor = build_preprocessing_pipeline(num_cols, cat_cols)
                    model = get_classification_model(m_type, self.random_state)
                    
                    X_tr_proc = preprocessor.fit_transform(X_train)
                    X_va_proc = preprocessor.transform(X_val)
                    
                    model.fit(X_tr_proc, y_train)
                    preds = model.predict(X_va_proc)
                    
                    f1s.append(f1_score(y_val, preds, average="weighted"))
                    bal_accs.append(balanced_accuracy_score(y_val, preds))
                    
                    try:
                        probs = model.predict_proba(X_va_proc)
                        if len(classes) == 2:
                            auc = roc_auc_score(y_val, probs[:, 1])
                        else:
                            auc = roc_auc_score(y_val, probs, multi_class="ovr", average="weighted")
                        aucs.append(auc)
                    except Exception:
                        aucs.append(0.50)
                        
                res_record = {
                    "experiment": exp_id,
                    "model": m_type,
                    "feature_count": len(all_cols),
                    "f1_mean": round(float(np.mean(f1s)), 4),
                    "f1_std": round(float(np.std(f1s)), 4),
                    "balanced_acc_mean": round(float(np.mean(bal_accs)), 4),
                    "balanced_acc_std": round(float(np.std(bal_accs)), 4),
                    "roc_auc_mean": round(float(np.mean(aucs)), 4),
                    "roc_auc_std": round(float(np.std(aucs)), 4),
                }
                results.append(res_record)
                logger.info(f"[{exp_id}] [{m_type}] F1: {res_record['f1_mean']:.4f}, AUC: {res_record['roc_auc_mean']:.4f}")
                
        res_df = pd.DataFrame(results)
        return res_df
