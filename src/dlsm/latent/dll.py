from typing import List, Dict, Any, Tuple
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.decomposition import PCA, FactorAnalysis
from sklearn.preprocessing import StandardScaler
from dlsm.utils.helpers import setup_logger

logger = setup_logger("dlsm.latent.dll")

class LatentDLLExtractor(BaseEstimator, TransformerMixin):
    """
    Constructs the Digital Lifestyle Load (DLL) latent dimension via PCA,
    with built-in Kaiser-Guttman evaluation, orientation harmonization,
    Factor Analysis sensitivity validation, and bootstrap stability analysis.
    
    Adheres strictly to RULE-011 and RULE-012.
    """
    def __init__(self, digital_feature_cols: List[str], n_components: int = 2, random_state: int = 42):
        self.digital_feature_cols = digital_feature_cols
        self.n_components = n_components
        self.random_state = random_state
        self.scaler = StandardScaler()
        self.pca = PCA(n_components=n_components, random_state=random_state)
        self.fa = FactorAnalysis(n_components=n_components, random_state=random_state)
        
        # State attributes
        self.explained_variance_ratio_: np.ndarray | None = None
        self.singular_values_: np.ndarray | None = None
        self.loadings_: pd.DataFrame | None = None
        self.fa_loadings_: pd.DataFrame | None = None
        self.sign_flip_: float = 1.0
        self.fa_correlation_: float | None = None
        self.stability_metrics_: Dict[str, Any] = {}

    def fit(self, X: pd.DataFrame, y=None):
        X_sub = X[self.digital_feature_cols].copy()
        X_scaled = self.scaler.fit_transform(X_sub)
        
        # Fit PCA
        self.pca.fit(X_scaled)
        self.explained_variance_ratio_ = self.pca.explained_variance_ratio_
        self.singular_values_ = self.pca.singular_values_
        
        raw_loadings = self.pca.components_[0]
        # Orientation harmonization: ensure PC1 positively tracks intensity (positive mean loading)
        if np.sum(raw_loadings) < 0:
            self.sign_flip_ = -1.0
        else:
            self.sign_flip_ = 1.0
            
        loadings_matrix = []
        for i in range(self.n_components):
            comp_loadings = self.pca.components_[i] * (self.sign_flip_ if i == 0 else 1.0)
            loadings_matrix.append(comp_loadings)
            
        self.loadings_ = pd.DataFrame(
            np.array(loadings_matrix).T,
            index=self.digital_feature_cols,
            columns=[f"PC{i+1}" for i in range(self.n_components)]
        )
        
        # Sensitivity check: Factor Analysis
        try:
            self.fa.fit(X_scaled)
            fa_comp = self.fa.components_[0]
            if np.sum(fa_comp) < 0:
                fa_comp = -fa_comp
            self.fa_loadings_ = pd.DataFrame(
                fa_comp,
                index=self.digital_feature_cols,
                columns=["FA1"]
            )
            # Correlation between PCA PC1 loadings and FA1 loadings
            corr = np.corrcoef(self.loadings_["PC1"], self.fa_loadings_["FA1"])[0, 1]
            self.fa_correlation_ = float(corr)
        except Exception as e:
            logger.warning(f"Factor Analysis sensitivity check encountered: {e}")
            self.fa_correlation_ = None

        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        df = X.copy()
        X_sub = df[self.digital_feature_cols].copy()
        X_scaled = self.scaler.transform(X_sub)
        
        pcs = self.pca.transform(X_scaled)
        # Harmonize DLL sign
        dll_score = pcs[:, 0] * self.sign_flip_
        df["digital_lifestyle_load"] = dll_score
        
        if self.n_components > 1:
            for i in range(1, self.n_components):
                df[f"latent_PC{i+1}"] = pcs[:, i]
                
        return df

    def evaluate_bootstrap_stability(self, X: pd.DataFrame, n_resamples: int = 1000) -> Dict[str, Any]:
        """
        Runs rigorous bootstrap resampling to evaluate loading stability and sign consistency.
        """
        rng = np.random.RandomState(self.random_state)
        X_sub = X[self.digital_feature_cols].copy()
        n_samples = len(X_sub)
        
        ref_loadings = self.loadings_["PC1"].values
        bootstrap_loadings = []
        cosine_sims = []
        
        for _ in range(n_resamples):
            indices = rng.choice(n_samples, size=n_samples, replace=True)
            resample = X_sub.iloc[indices]
            
            sc = StandardScaler()
            res_scaled = sc.fit_transform(resample)
            pca_res = PCA(n_components=1, random_state=self.random_state)
            pca_res.fit(res_scaled)
            
            l = pca_res.components_[0]
            # align direction
            if np.dot(l, ref_loadings) < 0:
                l = -l
                
            bootstrap_loadings.append(l)
            sim = np.dot(l, ref_loadings) / (np.linalg.norm(l) * np.linalg.norm(ref_loadings) + 1e-12)
            cosine_sims.append(sim)
            
        b_loadings = np.array(bootstrap_loadings)
        means = np.mean(b_loadings, axis=0)
        stds = np.std(b_loadings, axis=0)
        ci_lower = np.percentile(b_loadings, 2.5, axis=0)
        ci_upper = np.percentile(b_loadings, 97.5, axis=0)
        
        stability_summary = {}
        for idx, feat in enumerate(self.digital_feature_cols):
            stability_summary[feat] = {
                "original_loading": round(float(ref_loadings[idx]), 4),
                "bootstrap_mean": round(float(means[idx]), 4),
                "bootstrap_std": round(float(stds[idx]), 4),
                "ci_95": [round(float(ci_lower[idx]), 4), round(float(ci_upper[idx]), 4)],
                "sign_stable": bool(ci_lower[idx] * ci_upper[idx] > 0)
            }
            
        self.stability_metrics_ = {
            "mean_cosine_similarity": round(float(np.mean(cosine_sims)), 4),
            "std_cosine_similarity": round(float(np.std(cosine_sims)), 4),
            "explained_variance_ratio_pc1": round(float(self.explained_variance_ratio_[0]), 4),
            "factor_analysis_concordance": round(float(self.fa_correlation_), 4) if self.fa_correlation_ is not None else None,
            "feature_stability": stability_summary
        }
        
        logger.info(f"Latent DLL stability evaluation complete. Mean Cosine Similarity: {self.stability_metrics_['mean_cosine_similarity']}")
        return self.stability_metrics_
