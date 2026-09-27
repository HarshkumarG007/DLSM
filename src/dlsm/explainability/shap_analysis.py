from typing import List, Dict, Any, Tuple
import numpy as np
import pandas as pd
import shap
from sklearn.inspection import permutation_importance
from dlsm.utils.helpers import setup_logger

logger = setup_logger("dlsm.explainability.shap_analysis")

class ModelExplainer:
    """
    Computes SHAP global importance, dependence values, and permutation importance
    for tree ensembles. Adheres strictly to RULE-014 and RULE-016.
    """
    def __init__(self, model, feature_names: List[str], random_state: int = 42):
        self.model = model
        self.feature_names = feature_names
        self.random_state = random_state
        self.explainer: shap.TreeExplainer | None = None
        self.shap_values_: np.ndarray | None = None
        self.global_importance_: pd.DataFrame | None = None

    def fit_shap(self, X_sample: np.ndarray, max_eval_samples: int = 1000) -> pd.DataFrame:
        if len(X_sample) > max_eval_samples:
            rng = np.random.RandomState(self.random_state)
            idx = rng.choice(len(X_sample), size=max_eval_samples, replace=False)
            X_eval = X_sample[idx]
        else:
            X_eval = X_sample
            
        self.explainer = shap.TreeExplainer(self.model)
        shap_res = self.explainer(X_eval)
        
        # Handle multiclass vs single target
        if len(shap_res.values.shape) == 3:
            # Multi-class: mean across classes
            mean_abs_shap = np.mean(np.abs(shap_res.values), axis=(0, 2))
        else:
            mean_abs_shap = np.mean(np.abs(shap_res.values), axis=0)
            
        df_imp = pd.DataFrame({
            "feature": self.feature_names,
            "mean_abs_shap": mean_abs_shap
        }).sort_values(by="mean_abs_shap", ascending=False).reset_index(drop=True)
        
        # Compute relative percentage attribution
        tot = df_imp["mean_abs_shap"].sum()
        df_imp["relative_attribution_pct"] = (df_imp["mean_abs_shap"] / (tot + 1e-12) * 100).round(2)
        
        self.shap_values_ = shap_res.values
        self.global_importance_ = df_imp
        
        logger.info(f"SHAP explanation completed. Top feature: {df_imp.iloc[0]['feature']} ({df_imp.iloc[0]['relative_attribution_pct']}%)")
        return df_imp

    def compute_permutation_importance(self, X_val: np.ndarray, y_val: np.ndarray, n_repeats: int = 10) -> pd.DataFrame:
        """Evaluates permutation importance strictly on hold-out validation/test data (RULE-016)."""
        perm_res = permutation_importance(
            self.model, X_val, y_val, n_repeats=n_repeats, random_state=self.random_state, n_jobs=-1
        )
        df_perm = pd.DataFrame({
            "feature": self.feature_names,
            "perm_importance_mean": perm_res.importances_mean,
            "perm_importance_std": perm_res.importances_std
        }).sort_values(by="perm_importance_mean", ascending=False).reset_index(drop=True)
        
        return df_perm
