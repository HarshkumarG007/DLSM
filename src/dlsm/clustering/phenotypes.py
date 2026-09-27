from typing import List, Dict, Any, Tuple
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.mixture import GaussianMixture
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score, adjusted_rand_score
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from dlsm.utils.helpers import setup_logger

logger = setup_logger("dlsm.clustering.phenotypes")

class PhenotypeDiscovery:
    """
    Unsupervised behavioral phenotype discovery across digital engagement,
    sleep parameters, and lifestyle habits.
    
    Adheres strictly to RULE-013: Empirical profile evaluation before label assignment.
    """
    def __init__(self, feature_cols: List[str], k_range: Tuple[int, int] = (2, 6), random_state: int = 42):
        self.feature_cols = feature_cols
        self.k_range = range(k_range[0], k_range[1] + 1)
        self.random_state = random_state
        self.scaler = StandardScaler()
        self.best_k_: int = 3
        self.best_model_: KMeans | None = None
        self.k_metrics_: Dict[int, Dict[str, float]] = {}
        self.cluster_profiles_: pd.DataFrame | None = None
        self.stability_ari_: float | None = None
        self.pca_projection_: np.ndarray | None = None

    def evaluate_k_selection(self, df: pd.DataFrame, sample_size_for_silhouette: int = 4000) -> Dict[int, Dict[str, float]]:
        X_sub = df[self.feature_cols].copy()
        X_scaled = self.scaler.fit_transform(X_sub)
        
        # Subsample for silhouette efficiency if dataset is large
        if len(X_scaled) > sample_size_for_silhouette:
            rng = np.random.RandomState(self.random_state)
            sub_idx = rng.choice(len(X_scaled), size=sample_size_for_silhouette, replace=False)
            X_eval = X_scaled[sub_idx]
        else:
            X_eval = X_scaled

        best_score = -1.0
        best_k = self.k_range[0]
        
        for k in self.k_range:
            km = KMeans(n_clusters=k, random_state=self.random_state, n_init=10)
            labels = km.fit_predict(X_scaled)
            labels_eval = labels[sub_idx] if len(X_scaled) > sample_size_for_silhouette else labels
            
            sil = float(silhouette_score(X_eval, labels_eval))
            ch = float(calinski_harabasz_score(X_scaled, labels))
            db = float(davies_bouldin_score(X_scaled, labels))
            
            self.k_metrics_[k] = {
                "k": k,
                "silhouette_score": round(sil, 4),
                "calinski_harabasz": round(ch, 2),
                "davies_bouldin": round(db, 4),
                "inertia": round(float(km.inertia_), 2)
            }
            
            # Select k based on maximizing silhouette score
            if sil > best_score:
                best_score = sil
                best_k = k
                
        self.best_k_ = best_k
        logger.info(f"Optimal k selected: {self.best_k_} (Silhouette: {best_score:.4f})")
        return self.k_metrics_

    def fit_predict(self, df: pd.DataFrame) -> Tuple[np.ndarray, pd.DataFrame]:
        X_sub = df[self.feature_cols].copy()
        X_scaled = self.scaler.fit_transform(X_sub)
        
        self.best_model_ = KMeans(n_clusters=self.best_k_, random_state=self.random_state, n_init=20)
        labels = self.best_model_.fit_predict(X_scaled)
        
        # Calculate cluster profiles in original feature units and z-scores
        df_copy = df.copy()
        df_copy["cluster_id"] = labels
        
        mean_profiles = df_copy.groupby("cluster_id")[self.feature_cols].mean()
        size_series = df_copy["cluster_id"].value_counts().sort_index()
        pct_series = (size_series / len(df_copy) * 100).round(2)
        
        mean_profiles["cluster_size"] = size_series
        mean_profiles["cluster_pct"] = pct_series
        self.cluster_profiles_ = mean_profiles
        
        # 2D PCA projection for visualization
        pca_2d = PCA(n_components=2, random_state=self.random_state)
        self.pca_projection_ = pca_2d.fit_transform(X_scaled)
        
        return labels, self.cluster_profiles_

    def evaluate_cluster_stability(self, df: pd.DataFrame, n_resamples: int = 50) -> float:
        """Evaluates bootstrap cluster stability using Adjusted Rand Index (ARI)."""
        rng = np.random.RandomState(self.random_state)
        X_sub = df[self.feature_cols].copy()
        X_scaled = self.scaler.transform(X_sub)
        n_samples = len(X_scaled)
        
        ref_labels = self.best_model_.predict(X_scaled)
        ari_scores = []
        
        for _ in range(n_resamples):
            idx = rng.choice(n_samples, size=int(0.85 * n_samples), replace=False)
            X_sample = X_scaled[idx]
            
            km_sub = KMeans(n_clusters=self.best_k_, random_state=self.random_state, n_init=10)
            km_sub.fit(X_sample)
            
            # Predict on full set to compare partition consistency
            pred_labels = km_sub.predict(X_scaled)
            ari = adjusted_rand_score(ref_labels, pred_labels)
            ari_scores.append(ari)
            
        self.stability_ari_ = round(float(np.mean(ari_scores)), 4)
        logger.info(f"Cluster stability evaluation across {n_resamples} resamples: Mean ARI = {self.stability_ari_}")
        return self.stability_ari_
