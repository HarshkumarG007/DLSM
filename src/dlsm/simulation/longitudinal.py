"""
Synthetic Longitudinal Panel Simulator for DLSM.
Models multi-week academic semester trajectories (Weeks 1 to 16),
simulating cumulative sleep debt compounding, exam wave stressors,
and burnout thresholds under varying digital lifestyle interventions.
"""

from typing import Dict, Any, List
import numpy as np
import pandas as pd


class LongitudinalPanelSimulator:
    """
    Simulates a 16-week collegiate semester trajectory.
    Tracks weekly digital load, bedtime optical dose, nocturnal sleep loss,
    cumulative sleep debt (hours), next-day fatigue, and psychological wellbeing.
    """

    def __init__(self, weeks: int = 16, random_state: int = 42):
        self.weeks = weeks
        self.random_state = random_state

    def simulate_semester(
        self,
        baseline_social_hours: float = 4.5,
        baseline_ai_hours: float = 2.5,
        baseline_bedtime_min: int = 60,
        baseline_sleep_hours: float = 6.5,
        baseline_activity_hours: float = 1.25,
        blue_light_filter: bool = False,
        primary_app_weight: float = 0.85,
        exam_intensity_multiplier: float = 1.0,
    ) -> pd.DataFrame:
        """
        Simulate weekly progression across 16 academic weeks.
        
        Stress peaks occur at:
        - Midterm Wave 1 (Weeks 6-7)
        - Final Exams Wave (Weeks 14-15)
        """
        np.random.seed(self.random_state)
        records = []
        cum_sleep_debt = 0.0

        for t in range(1, self.weeks + 1):
            # Academic stress wave function (two Gaussian spikes for midterms and finals)
            midterm_spike = 0.40 * np.exp(-((t - 7) ** 2) / (2 * 1.2 ** 2))
            final_spike = 0.70 * np.exp(-((t - 15) ** 2) / (2 * 1.5 ** 2))
            stress_factor = (1.0 + (midterm_spike + final_spike) * exam_intensity_multiplier)

            # Weekly stochastic fluctuation
            noise_digital = np.random.normal(0, 0.2)
            noise_sleep = np.random.normal(0, 0.15)

            # Evolving digital hours under stress
            social_h = max(0.5, baseline_social_hours * (1.0 + 0.20 * (stress_factor - 1.0)) + noise_digital)
            ai_h = max(0.5, baseline_ai_hours * stress_factor + noise_digital)
            tdh = social_h + ai_h
            
            # Bedtime phone minutes expand under exam cramming / bedtime procrastination
            bedtime_min = min(180, max(10, baseline_bedtime_min * (1.0 + 0.35 * (stress_factor - 1.0))))
            
            # Bedtime Intensity Index (BII)
            filter_discount = 0.30 if blue_light_filter else 0.0
            bii = (55.0 / 100.0) * bedtime_min * (1.0 - filter_discount) * primary_app_weight

            # Sleep truncation: screen displacement + stress arousal
            sleep_truncation = (0.25 * (tdh - (baseline_social_hours + baseline_ai_hours)) +
                                0.015 * (bedtime_min - baseline_bedtime_min) +
                                0.50 * (stress_factor - 1.0))
            weekly_sleep_hours = max(3.5, min(10.0, baseline_sleep_hours - sleep_truncation + noise_sleep))

            # Weekly sleep deficit against restorative target (8.0 hours)
            weekly_deficit = max(0.0, 8.0 - weekly_sleep_hours) * 7.0
            
            # Physical activity buffer recovery (1 hour of exercise recovers 2.5 hours of sleep debt)
            activity_h = max(0.1, baseline_activity_hours * (1.0 - 0.25 * (stress_factor - 1.0)))
            weekly_recovery = activity_h * 2.5
            
            # Cumulative debt compounding
            cum_sleep_debt = max(0.0, cum_sleep_debt + (weekly_deficit - weekly_recovery))

            # Relational ratios
            ssr = tdh / max(weekly_sleep_hours, 0.1)
            abr = activity_h / max(tdh, 0.1)

            # Latent DLL z-score
            dll_z = ((social_h - 4.54) / 2.31 * 0.58 +
                     (ai_h - 2.59) / 1.62 * 0.56 +
                     (tdh - 7.13) / 3.01 * 0.59)

            # Outcome trajectories: Fatigue (1-10) and Mental Health (32-92)
            fatigue = np.clip(3.79 + 0.70 * dll_z + 0.06 * cum_sleep_debt + 0.35 * (bii / 45.0 - 1.0), 1.0, 10.0)
            mental_health = np.clip(72.49 - 2.10 * dll_z - 0.18 * cum_sleep_debt - 1.40 * (ssr - 1.15) + 1.80 * (activity_h - 1.25), 30.0, 95.0)

            # Risk classification
            if cum_sleep_debt > 35.0 or ssr > 1.25 or fatigue > 6.5:
                risk_status = "Severe Burnout Risk"
            elif cum_sleep_debt > 18.0 or ssr > 0.90 or fatigue > 5.0:
                risk_status = "Elevated Fatigue"
            else:
                risk_status = "Circadian Protected"

            records.append({
                "Week": t,
                "Academic_Phase": "Midterms 1" if 6 <= t <= 7 else ("Finals" if 14 <= t <= 15 else "Regular Term"),
                "Total_Digital_Hours": round(tdh, 2),
                "Social_Media_Hours": round(social_h, 2),
                "AI_Tool_Hours": round(ai_h, 2),
                "Bedtime_Phone_Min": round(bedtime_min, 1),
                "Sleep_Hours": round(weekly_sleep_hours, 2),
                "Physical_Activity_Hours": round(activity_h, 2),
                "Cumulative_Sleep_Debt_Hours": round(cum_sleep_debt, 1),
                "Screen_to_Sleep_Ratio": round(ssr, 2),
                "Active_Buffer_Ratio": round(abr, 2),
                "Digital_Lifestyle_Load": round(dll_z, 2),
                "Predicted_Fatigue": round(fatigue, 2),
                "Predicted_Mental_Health": round(mental_health, 2),
                "Risk_Status": risk_status,
            })

        return pd.DataFrame(records)
