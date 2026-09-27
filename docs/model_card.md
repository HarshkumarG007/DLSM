# DLSM Model Cards

## 1. Dataset A Next-Day Fatigue Model Card
- **Model Type:** Extreme Gradient Boosting (`XGBRegressor`)
- **Version:** 1.0.0
- **Primary Task:** Continuous prediction of self-reported cognitive fatigue ($1.0 - 10.0$)
- **Input Features ($P=25$):** Full DLSM framework (Raw Demographics, Biophysical Bedtime Intensity Index, Screen-to-Sleep Ratio, Restorative Sleep Architecture, Caffeine Interaction, and Latent DLL).
- **Training Data:** $N = 8,500$ observational telemetry records.
- **Validation Scheme:** 5-Fold Cross-Validation with strict pipeline isolation.
- **Performance:**
  - $R^2 = 0.9545 \pm 0.0018$
  - $\text{MAE} = 0.4128 \pm 0.0060$
  - $\text{RMSE} = 0.5723 \pm 0.0040$
- **Top Attributions (SHAP):** `sleep_latency_ratio` ($34.98\%$), `total_sleep_hours` ($26.17\%$), `morning_alarm_snoozes` ($19.78\%$).
- **Intended Use:** Academic and research analysis of lifestyle circadian spillover. Not for clinical medical diagnosis.

---

## 2. Dataset B Student Mental Health Model Card
- **Model Type:** Ridge Regression (`Ridge`) / Extreme Gradient Boosting (`XGBRegressor`)
- **Version:** 1.0.0
- **Primary Task:** Continuous prediction of student mental health index ($32.56 - 91.76$)
- **Input Features ($P=16$):** Full DLSM framework (Demographics, Total Digital Hours, AI Composition Ratio, Screen-to-Sleep Ratio, Active Buffer Ratio, Modality Interactions, and Latent DLL).
- **Training Data:** $N = 16,000$ student survey records.
- **Validation Scheme:** 5-Fold Cross-Validation with strict pipeline isolation.
- **Performance:**
  - $R^2 = 0.2460 \pm 0.0147$
  - $\text{MAE} = 6.3534 \pm 0.0768$
  - $\text{RMSE} = 8.0252 \pm 0.1176$
- **Top Attributions (SHAP):** `screen_to_sleep_ratio` ($37.09\%$), `active_buffer_ratio` ($19.38\%$), `Sleep_Hours` ($7.70\%$).
- **Ethical Considerations:** Predictions must not be used to restrict student access to educational or AI tools.
