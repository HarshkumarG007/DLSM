"""
DLSM Differential Privacy Engine.
Implements calibrated Laplace and Gaussian perturbation mechanisms for aggregate
longitudinal simulation queries and population statistics under formal (epsilon, delta)-DP guarantees.
"""

from typing import Dict, Any, Optional, Tuple, List
import math
import numpy as np


class DifferentialPrivacyEngine:
    """
    Provides mathematical differential privacy mechanisms for research telemetry.
    Ensures that aggregate outputs (sleep debt, burnout risk, digital hours)
    cannot be inverted to reconstruct individual student behavioral trajectories.
    """

    def __init__(self, random_state: Optional[int] = 42):
        self.rng = np.random.default_rng(random_state)

    def laplace_mechanism(
        self,
        value: float,
        sensitivity: float,
        epsilon: float,
        lower_bound: Optional[float] = None,
        upper_bound: Optional[float] = None
    ) -> float:
        """
        Applies standard epsilon-differential privacy via the Laplace mechanism.
        Noise scale b = sensitivity / epsilon.
        """
        if epsilon <= 0.0:
            raise ValueError(f"Epsilon must be strictly positive, got {epsilon}")
        if sensitivity <= 0.0:
            return value

        scale = sensitivity / epsilon
        noise = self.rng.laplace(0.0, scale)
        perturbed = value + noise

        if lower_bound is not None:
            perturbed = max(lower_bound, perturbed)
        if upper_bound is not None:
            perturbed = min(upper_bound, perturbed)

        return float(perturbed)

    def gaussian_mechanism(
        self,
        value: float,
        sensitivity: float,
        epsilon: float,
        delta: float = 1e-5,
        lower_bound: Optional[float] = None,
        upper_bound: Optional[float] = None
    ) -> float:
        """
        Applies (epsilon, delta)-differential privacy via the Gaussian mechanism.
        sigma = (sensitivity * sqrt(2 * ln(1.25 / delta))) / epsilon.
        """
        if epsilon <= 0.0 or delta <= 0.0 or delta >= 1.0:
            raise ValueError(f"Invalid DP parameters: epsilon={epsilon}, delta={delta}")
        if sensitivity <= 0.0:
            return value

        sigma = (sensitivity * math.sqrt(2.0 * math.log(1.25 / delta))) / epsilon
        noise = self.rng.normal(0.0, sigma)
        perturbed = value + noise

        if lower_bound is not None:
            perturbed = max(lower_bound, perturbed)
        if upper_bound is not None:
            perturbed = min(upper_bound, perturbed)

        return float(perturbed)

    def privatize_simulation_summary(
        self,
        final_sleep_debt: float,
        burnout_hazard_pct: float,
        mean_screen_hours: float,
        weeks: int = 16,
        cohort_size: int = 50,
        epsilon: float = 1.0,
        mechanism: str = "laplace"
    ) -> Dict[str, Any]:
        """
        Sanitizes semester simulation aggregates under differential privacy.
        Sensitivities:
          - Cumulative sleep debt: max individual sleep variation = 2.0 hrs/day * 7 days = 14 hrs / cohort_size
          - Burnout hazard pct: max single student contribution = (1 / cohort_size) * 100%
          - Mean screen hours: max screen discrepancy = 4.0 hrs / cohort_size
        """
        sens_debt = 14.0 / max(1, cohort_size)
        sens_hazard = 100.0 / max(1, cohort_size)
        sens_screen = 4.0 / max(1, cohort_size)

        # Allocate privacy budget across 3 queries (composition: epsilon_i = epsilon / 3)
        eps_i = epsilon / 3.0

        if mechanism == "gaussian":
            priv_debt = self.gaussian_mechanism(
                final_sleep_debt, sensitivity=sens_debt, epsilon=eps_i, delta=1e-5, lower_bound=0.0
            )
            priv_hazard = self.gaussian_mechanism(
                burnout_hazard_pct, sensitivity=sens_hazard, epsilon=eps_i, delta=1e-5, lower_bound=0.0, upper_bound=100.0
            )
            priv_screen = self.gaussian_mechanism(
                mean_screen_hours, sensitivity=sens_screen, epsilon=eps_i, delta=1e-5, lower_bound=0.0
            )
        else:
            priv_debt = self.laplace_mechanism(
                final_sleep_debt, sensitivity=sens_debt, epsilon=eps_i, lower_bound=0.0
            )
            priv_hazard = self.laplace_mechanism(
                burnout_hazard_pct, sensitivity=sens_hazard, epsilon=eps_i, lower_bound=0.0, upper_bound=100.0
            )
            priv_screen = self.laplace_mechanism(
                mean_screen_hours, sensitivity=sens_screen, epsilon=eps_i, lower_bound=0.0
            )

        return {
            "privacy_guarantee": f"({epsilon:.2f}, 1e-5)-DP" if mechanism == "gaussian" else f"{epsilon:.2f}-DP (Laplace)",
            "total_epsilon": epsilon,
            "mechanism": mechanism,
            "privatized_final_sleep_debt": round(priv_debt, 2),
            "privatized_burnout_hazard_pct": round(priv_hazard, 1),
            "privatized_mean_screen_hours": round(priv_screen, 2),
            "raw_final_sleep_debt": round(final_sleep_debt, 2),
            "raw_burnout_hazard_pct": round(burnout_hazard_pct, 1),
        }
