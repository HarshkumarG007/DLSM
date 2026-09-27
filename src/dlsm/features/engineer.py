from typing import Tuple, List, Dict, Any
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

AROUSAL_WEIGHTS_A = {
    "TikTok / Reels": 1.00,
    "YouTube": 0.80,
    "Instagram / Reddit": 0.75,
    "Streaming (Netflix/Hulu)": 0.60,
    "Messaging / Chat": 0.50,
    "News / Reading": 0.30
}

class DatasetAFeatureEngineer(BaseEstimator, TransformerMixin):
    """
    Transforms Dataset A by constructing theoretically grounded domain and interaction features.
    Adheres to RULE-010: Every engineered feature has a documented mathematical definition.
    """
    def __init__(self, include_interactions: bool = True):
        self.include_interactions = include_interactions
        self.feature_names_ = []

    def fit(self, X: pd.DataFrame, y=None):
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        df = X.copy()
        
        # 1. Optical/Biophysical Load discounted by blue light filter
        df["bedtime_intensity_index"] = (
            (df["screen_brightness_pct"] / 100.0)
            * df["bedtime_phone_minutes"]
            * (1.0 - 0.30 * df["blue_light_filter_active"])
        )
        
        # 2. Ratio of pre-sleep screen exposure (converted to hours) to total sleep hours
        df["screen_to_sleep_ratio"] = (df["bedtime_phone_minutes"] / 60.0) / (df["total_sleep_hours"] + 1e-5)
        
        # 3. Sleep architecture efficiency (combined proportion of restorative Slow-wave + REM stages)
        df["sleep_architecture_efficiency"] = (df["deep_sleep_pct"] + df["rem_sleep_pct"]) / 100.0
        
        # 4. App cognitive arousal weighting
        df["cognitive_arousal_weight"] = df["primary_bedtime_app"].map(AROUSAL_WEIGHTS_A).fillna(0.60)
        df["arousal_weighted_bedtime_exposure"] = df["bedtime_phone_minutes"] * df["cognitive_arousal_weight"]
        
        # 5. Sleep latency penalty index (latency relative to duration)
        df["sleep_latency_ratio"] = (df["sleep_latency_min"] / 60.0) / (df["total_sleep_hours"] + 1e-5)

        if self.include_interactions:
            # 6. Interaction: Stimulant caffeine x digital cognitive arousal
            df["caffeine_screen_interaction"] = df["caffeine_post_5pm_mg"] * df["bedtime_phone_minutes"]
            
            # 7. Interaction: Screen duration x screen brightness
            df["brightness_screen_interaction"] = df["screen_brightness_pct"] * df["bedtime_phone_minutes"]
            
            # 8. Interaction: Screen exposure x nocturnal sleep duration
            df["screen_sleep_interaction"] = (df["bedtime_phone_minutes"] / 60.0) * df["total_sleep_hours"]

        return df


class DatasetBFeatureEngineer(BaseEstimator, TransformerMixin):
    """
    Transforms Dataset B by constructing student digital load, composition, and lifestyle buffering features.
    Adheres to RULE-010: Every engineered feature has a documented mathematical definition.
    """
    def __init__(self, include_interactions: bool = True):
        self.include_interactions = include_interactions

    def fit(self, X: pd.DataFrame, y=None):
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        df = X.copy()
        
        # 1. Total daily digital hours across social media and AI tools
        df["total_digital_hours"] = df["Daily_Social_Media_Hours"] + df["Daily_AI_Tool_Usage_Hours"]
        
        # 2. Digital composition ratio: AI tool usage relative to total digital exposure
        df["digital_composition_ratio"] = df["Daily_AI_Tool_Usage_Hours"] / (df["total_digital_hours"] + 1e-5)
        
        # 3. Screen-to-sleep ratio: total daily screen hours relative to nocturnal sleep duration
        df["screen_to_sleep_ratio"] = df["total_digital_hours"] / (df["Sleep_Hours"] + 1e-5)
        
        # 4. Lifestyle buffer ratio: physical activity hours relative to sedentary digital exposure
        df["active_buffer_ratio"] = df["Physical_Activity_Hours"] / (df["total_digital_hours"] + 1e-5)
        
        # 5. Sleep deficit index (relative to 8.0 hour standard recommendation for students)
        df["sleep_deficit_hours"] = np.maximum(0.0, 8.0 - df["Sleep_Hours"])

        if self.include_interactions:
            # 6. Interaction: Social media volume x Sleep duration
            df["social_sleep_interaction"] = df["Daily_Social_Media_Hours"] * df["Sleep_Hours"]
            
            # 7. Interaction: AI tool usage x Sleep duration
            df["ai_sleep_interaction"] = df["Daily_AI_Tool_Usage_Hours"] * df["Sleep_Hours"]
            
            # 8. Interaction: Social media volume x Physical activity buffer
            df["social_physical_interaction"] = df["Daily_Social_Media_Hours"] * df["Physical_Activity_Hours"]

        return df
