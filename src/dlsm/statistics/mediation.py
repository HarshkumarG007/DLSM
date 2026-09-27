from typing import List, Dict, Any, Tuple
import numpy as np
import pandas as pd
import statsmodels.api as sm
from dlsm.utils.helpers import setup_logger

logger = setup_logger("dlsm.statistics.mediation")

class StatisticalMediation:
    """
    Implements regression-based statistical mediation with non-parametric
    bootstrap confidence intervals for the indirect effect (a * b).
    
    Adheres strictly to RULE-015 and RULE-029:
    Explicitly caveats cross-sectional data cannot prove causality or temporal ordering.
    """
    def __init__(self, n_bootstraps: int = 5000, ci_level: float = 0.95, random_state: int = 42):
        self.n_bootstraps = n_bootstraps
        self.ci_level = ci_level
        self.random_state = random_state

    def fit(
        self,
        df: pd.DataFrame,
        x_col: str,
        m_col: str,
        y_col: str,
        covariate_cols: List[str] | None = None
    ) -> Dict[str, Any]:
        covs = covariate_cols if covariate_cols is not None else []
        df_clean = df[[x_col, m_col, y_col] + covs].dropna()
        n = len(df_clean)
        
        # Model 1: M = a*X + C*gamma + intercept
        X_m = df_clean[[x_col] + covs]
        X_m_const = sm.add_constant(X_m)
        model_m = sm.OLS(df_clean[m_col], X_m_const).fit()
        a_coef = float(model_m.params[x_col])
        a_se = float(model_m.bse[x_col])
        a_pval = float(model_m.pvalues[x_col])
        
        # Model 2: Y = c'*X + b*M + C*gamma + intercept
        X_y = df_clean[[x_col, m_col] + covs]
        X_y_const = sm.add_constant(X_y)
        model_y = sm.OLS(df_clean[y_col], X_y_const).fit()
        c_prime_coef = float(model_y.params[x_col])
        c_prime_se = float(model_y.bse[x_col])
        c_prime_pval = float(model_y.pvalues[x_col])
        b_coef = float(model_y.params[m_col])
        b_se = float(model_y.bse[m_col])
        b_pval = float(model_y.pvalues[m_col])
        
        # Total effect Model: Y = c*X + C*gamma + intercept
        X_tot = df_clean[[x_col] + covs]
        X_tot_const = sm.add_constant(X_tot)
        model_tot = sm.OLS(df_clean[y_col], X_tot_const).fit()
        c_coef = float(model_tot.params[x_col])
        c_se = float(model_tot.bse[x_col])
        c_pval = float(model_tot.pvalues[x_col])
        
        indirect_effect = a_coef * b_coef
        prop_mediated = (indirect_effect / c_coef) if abs(c_coef) > 1e-7 else np.nan
        
        # Non-parametric Bootstrap for Indirect Effect (a * b)
        rng = np.random.RandomState(self.random_state)
        boot_indirects = []
        
        X_arr = df_clean[x_col].values
        M_arr = df_clean[m_col].values
        Y_arr = df_clean[y_col].values
        C_arr = df_clean[covs].values if covs else None
        
        for _ in range(self.n_bootstraps):
            idx = rng.choice(n, size=n, replace=True)
            bx, bm, by = X_arr[idx], M_arr[idx], Y_arr[idx]
            
            if C_arr is not None:
                bc = C_arr[idx]
                X_mat_m = np.column_stack([np.ones(n), bx, bc])
                X_mat_y = np.column_stack([np.ones(n), bx, bm, bc])
            else:
                X_mat_m = np.column_stack([np.ones(n), bx])
                X_mat_y = np.column_stack([np.ones(n), bx, bm])
                
            try:
                # Fast ordinary least squares normal equations: (X'X)^-1 X'y
                beta_m = np.linalg.lstsq(X_mat_m, bm, rcond=None)[0]
                beta_y = np.linalg.lstsq(X_mat_y, by, rcond=None)[0]
                boot_a = beta_m[1]
                boot_b = beta_y[2]
                boot_indirects.append(boot_a * boot_b)
            except Exception:
                continue
                
        boot_arr = np.array(boot_indirects)
        alpha = 1.0 - self.ci_level
        ci_lower = float(np.percentile(boot_arr, 100 * (alpha / 2)))
        ci_upper = float(np.percentile(boot_arr, 100 * (1 - alpha / 2)))
        significant = bool(ci_lower * ci_upper > 0)
        
        results = {
            "predictor_X": x_col,
            "mediator_M": m_col,
            "outcome_Y": y_col,
            "covariates": covs,
            "sample_size": n,
            "a_path": {"coef": round(a_coef, 4), "se": round(a_se, 4), "p_value": round(a_pval, 6)},
            "b_path": {"coef": round(b_coef, 4), "se": round(b_se, 4), "p_value": round(b_pval, 6)},
            "direct_effect_c_prime": {"coef": round(c_prime_coef, 4), "se": round(c_prime_se, 4), "p_value": round(c_prime_pval, 6)},
            "total_effect_c": {"coef": round(c_coef, 4), "se": round(c_se, 4), "p_value": round(c_pval, 6)},
            "indirect_effect_ab": round(indirect_effect, 4),
            "proportion_mediated": round(float(prop_mediated), 4) if not np.isnan(prop_mediated) else None,
            "bootstrap_ci_95": [round(ci_lower, 4), round(ci_upper, 4)],
            "statistically_significant": significant,
            "scientific_qualification": (
                "Statistical mediation confirmed under observational cross-sectional assumptions; "
                "cannot establish chronological or causal directionality without longitudinal intervention."
            )
        }
        
        logger.info(
            f"Mediation [{x_col} -> {m_col} -> {y_col}]: "
            f"Indirect={results['indirect_effect_ab']:.4f} (95% CI: [{ci_lower:.4f}, {ci_upper:.4f}]), "
            f"Significant={significant}"
        )
        return results
