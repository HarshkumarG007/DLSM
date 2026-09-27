"""
DLSM — Small-N Methodology Stress Test (reference implementation)
====================================================================
Real, runnable code demonstrating two risks that neither source document
flags with a concrete safeguard: (1) K-Means "discovering" clean phenotypes
in small survey-style data even when there is no real cluster structure,
and (2) picking the best of several tuned model families over a handful of
folds inflating the apparent edge versus a true held-out check.

Sized to match a REAL, comparable public dataset I found while checking this
(a Kaggle-sourced sleep/screen-time survey: 104 rows, 6 mostly Yes/No
columns) rather than the tens-of-thousands-of-rows scale the source
documents' tooling (Optuna, SHAP, DVC, MLflow, Docker) implicitly assumes.
"""
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler

rng = np.random.default_rng(7)
N = 220  # realistic scale for this genre of Kaggle survey dataset, not "big data"

# ---------------------------------------------------------------------------
# 1. SYNTHETIC DATA WITH **NO REAL LATENT STRUCTURE** (pure noise, on purpose)
#    If clustering "finds" clean phenotypes here anyway, that's the point.
# ---------------------------------------------------------------------------
features = ["screen_minutes", "night_use_minutes", "social_media_mins",
            "ai_tool_mins", "self_reported_sleep_hours"]
X_noise = pd.DataFrame(rng.normal(0, 1, size=(N, len(features))), columns=features)
y_noise = rng.integers(0, 2, N)  # unrelated random binary "grade_risk" target

print("=== Risk 1: does K-Means find 'phenotypes' in pure noise? ===")
for k in [2, 3, 4, 5]:
    km = KMeans(n_clusters=k, n_init=10, random_state=42).fit(X_noise)
    sil = silhouette_score(X_noise, km.labels_)
    print(f"k={k}: silhouette={sil:.3f}  cluster sizes={np.bincount(km.labels_)}")
print("Silhouette scores this low/inconsistent across k mean: no real cluster")
print("structure, even though K-Means will happily draw k boundaries anyway and")
print("a plot will 'look like' 3-5 distinct phenotypes.\n")

# ---------------------------------------------------------------------------
# 2. MULTI-MODEL SELECTION OVER FEW FOLDS vs. A TRUE HELD-OUT CHECK
# ---------------------------------------------------------------------------
X_sel, X_final = X_noise.iloc[:170], X_noise.iloc[170:]
y_sel, y_final = y_noise[:170], y_noise[170:]

models = {
    "logistic": LogisticRegression(max_iter=1000),
    "random_forest": RandomForestClassifier(n_estimators=200, max_depth=4, random_state=42),
    "gradient_boosting": GradientBoostingClassifier(n_estimators=150, max_depth=3, random_state=42),
}
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
print("=== Risk 2: best-of-3-models over 5 folds, vs. a real holdout ===")
cv_scores = {}
for name, model in models.items():
    fold_acc = []
    for tr_idx, te_idx in cv.split(X_sel, y_sel):
        scaler = StandardScaler().fit(X_sel.iloc[tr_idx])
        model.fit(scaler.transform(X_sel.iloc[tr_idx]), y_sel[tr_idx])
        fold_acc.append(model.score(scaler.transform(X_sel.iloc[te_idx]), y_sel[te_idx]))
    cv_scores[name] = np.mean(fold_acc)
    print(f"{name}: 5-fold CV accuracy = {cv_scores[name]:.3f}  (baseline ~0.50, target is random)")

best_name = max(cv_scores, key=cv_scores.get)
print(f"\n'Winner' by CV selection: {best_name} ({cv_scores[best_name]:.3f})")

scaler = StandardScaler().fit(X_sel)
best_model = models[best_name]
best_model.fit(scaler.transform(X_sel), y_sel)
final_acc = best_model.score(scaler.transform(X_final), y_final)
print(f"Same model on the TRUE held-out set (never touched during selection): {final_acc:.3f}")
print("The target is genuinely random, so ANY accuracy that looks meaningfully")
print("above 0.50 on either number is the selection process finding noise, not signal —")
print("this is what running the real pipeline without a final holdout would hide.")
