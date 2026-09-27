# DLSM Data Dictionary & Semantic Taxonomy

## Semantic Roles Taxonomy (Prompt Section 3.3)
- `IDENTIFIER`: Unique entity primary keys. Excluded from predictive modeling.
- `DEMOGRAPHIC`: Age, gender, education level, occupation.
- `DIGITAL_INTENSITY`: Magnitude of optical or hourly digital exposure.
- `DIGITAL_TIMING`: Temporal concentration of digital behavior (bedtime usage).
- `DIGITAL_PURPOSE`: Modality, application genre, or cognitive arousal type.
- `SLEEP`: Polysomnography, sleep duration, sleep latency, sleep debt.
- `HEALTH`: Physical health, somatic vitality, mental health index.
- `ACADEMIC`: Educational tier, student level.
- `BEHAVIORAL`: Physical exercise, alarm snoozing, filter switching.
- `TARGET`: Downstream supervised regression or classification endpoints.
- `POTENTIAL_CONFOUNDER`: Evening caffeine, age, chronotype.
- `UNKNOWN`: Unclassified or ambiguous variables (permitted by schema audit).

---

## Dataset A Variable Specifications
| Name | Type | Semantic Role | Range / Allowed | Description |
|:---|:---|:---|:---|:---|
| `user_id` | String | `IDENTIFIER` | Alphanumeric | Unique participant tracking ID |
| `age` | Integer | `DEMOGRAPHIC` | 18 – 65 | Participant age in years |
| `gender` | String | `DEMOGRAPHIC` | Female, Male, Non-Binary | Self-reported gender identity |
| `occupation_type` | String | `POTENTIAL_CONFOUNDER` | 5 Categories | Employment profile |
| `chronotype` | String | `POTENTIAL_CONFOUNDER` | 3 Categories | Circadian preference |
| `bedtime_phone_minutes`| Integer | `DIGITAL_TIMING` | 1 – 180 min | Active bedtime smartphone usage |
| `primary_bedtime_app` | String | `DIGITAL_PURPOSE` | 6 Genres | Dominant app genre before sleep |
| `screen_brightness_pct`| Integer | `DIGITAL_INTENSITY` | 10 – 100% | Optical display brightness |
| `blue_light_filter_active`| Binary | `BEHAVIORAL` | 0 or 1 | Active blue light filter status |
| `caffeine_post_5pm_mg` | Integer | `POTENTIAL_CONFOUNDER` | 0 – 250 mg | Evening caffeine consumption |
| `physical_activity_min`| Integer | `BEHAVIORAL` | 0 – 112 min | Daily moderate-to-vigorous activity |
| `sleep_latency_min` | Float | `SLEEP` | 6.0 – 123.3 min | Minutes to sleep onset |
| `total_sleep_hours` | Float | `SLEEP` | 3.2 – 9.8 hrs | Nocturnal sleep duration |
| `deep_sleep_pct` | Float | `SLEEP` | 8.1 – 28.0% | Slow-wave restorative sleep % |
| `rem_sleep_pct` | Float | `SLEEP` | 9.6 – 27.0% | REM sleep % |
| `morning_alarm_snoozes`| Integer | `SLEEP` | 0 – 7 | Frequency of alarm snoozes |
| `next_day_fatigue_score`| Float | `TARGET` | 1.0 – 10.0 | Continuous fatigue index |
| `sleep_debt_category` | String | `TARGET` | 4 Categories | Sleep debt severity class |

---

## Dataset B Variable Specifications
| Name | Type | Semantic Role | Range / Allowed | Description |
|:---|:---|:---|:---|:---|
| `Student_ID` | String | `IDENTIFIER` | Alphanumeric | Unique student ID |
| `Age` | Integer | `DEMOGRAPHIC` | 13 – 25 | Student chronological age |
| `Gender` | String | `DEMOGRAPHIC` | Male, Female, Non-binary | Self-reported gender |
| `Education_Level` | String | `ACADEMIC` | High School, College, University | Current student academic tier |
| `Daily_Social_Media_Hours`| Float | `DIGITAL_INTENSITY`| 0.0 – 14.0 hrs | Daily hours on social media |
| `Daily_AI_Tool_Usage_Hours`| Float | `DIGITAL_INTENSITY`| 0.0 – 9.5 hrs | Daily hours on AI tools |
| `Sleep_Hours` | Float | `SLEEP` | 2.0 – 11.15 hrs | Nocturnal sleep hours |
| `Physical_Activity_Hours` | Float | `BEHAVIORAL` | 0.0 – 5.0 hrs | Daily exercise hours |
| `Mental_Health_Score` | Float | `TARGET` | 32.56 – 91.76 | Psychological wellbeing index |
| `Physical_Health_Score` | Float | `HEALTH` | 48.03 – 99.98 | Somatic health score |

---

## Derived & Engineered Feature Taxonomy

### Dataset A Engineered Features
| Name | Type | Semantic Role | Range / Unit | Mathematical Description |
|:---|:---|:---|:---|:---|
| `bedtime_intensity_index` | Float | `DIGITAL_INTENSITY` | 0.0 – 180.0 | Optical intensity discounted by blue-light filter: $\frac{\text{brightness}}{100} \times \text{minutes} \times (1 - 0.30 \times \text{filter})$ |
| `screen_to_sleep_ratio` | Float | `BEHAVIORAL` | 0.0 – 0.94 | Proportion of nocturnal sleep duration consumed by pre-sleep device interaction |
| `sleep_architecture_efficiency` | Float | `SLEEP` | 0.17 – 0.55 | Restorative sleep fraction: $\frac{\text{deep\_sleep\_pct} + \text{rem\_sleep\_pct}}{100}$ |
| `cognitive_arousal_weight` | Float | `DIGITAL_PURPOSE` | 0.30 – 1.00 | Biophysical arousal weight assigned to primary bedtime application genre |
| `arousal_weighted_bedtime_exposure` | Float | `DIGITAL_PURPOSE` | 0.3 – 180.0 | Cognitive stimulus: $\text{bedtime\_minutes} \times \text{arousal\_weight}$ |
| `sleep_latency_ratio` | Float | `SLEEP` | 0.01 – 0.64 | Fraction of nocturnal sleep window spent attempting to initiate sleep |
| `caffeine_screen_interaction` | Float | `POTENTIAL_CONFOUNDER` | 0.0 – 45,000.0 | Synergistic evening pharmacological and optical stimulus: $\text{caffeine} \times \text{bedtime\_minutes}$ |
| `brightness_screen_interaction` | Float | `DIGITAL_INTENSITY` | 10.0 – 18,000.0 | Gross luminous flux exposure: $\text{screen\_brightness\_pct} \times \text{bedtime\_minutes}$ |
| `screen_sleep_interaction` | Float | `BEHAVIORAL` | 3.2 – 1,764.0 | Exposure displacing duration: $\text{bedtime\_minutes} \times \text{total\_sleep\_hours}$ |
| `digital_lifestyle_load` (DLL) | Float | `DIGITAL_INTENSITY` | $\approx -2.5$ to $+3.0$ SD | First principal component score from standardized pre-sleep digital behavior |

### Dataset B Engineered Features
| Name | Type | Semantic Role | Range / Unit | Mathematical Description |
|:---|:---|:---|:---|:---|
| `total_digital_hours` | Float | `DIGITAL_INTENSITY` | 0.0 – 23.5 hrs | Aggregate daily digital engagement: $\text{Social\_Media} + \text{AI\_Tools}$ |
| `digital_composition_ratio` | Float | `DIGITAL_PURPOSE` | 0.0 – 1.0 | Proportion of digital budget allocated to generative/assistive AI tools |
| `screen_to_sleep_ratio` | Float | `BEHAVIORAL` | 0.0 – 11.75 | Relational ratio: $\frac{\text{total\_digital\_hours}}{\text{Sleep\_Hours} + \epsilon}$ |
| `active_buffer_ratio` | Float | `BEHAVIORAL` | 0.0 – $\infty$ | Relational restorative buffer: $\frac{\text{Physical\_Activity\_Hours}}{\text{total\_digital\_hours} + \epsilon}$ |
| `sleep_deficit_hours` | Float | `SLEEP` | 0.0 – 6.0 hrs | Truncation relative to normative 8.0-hour restorative baseline |
| `social_sleep_interaction` | Float | `BEHAVIORAL` | 0.0 – 156.1 | Cross-modal displacement: $\text{Daily\_Social\_Media\_Hours} \times \text{Sleep\_Hours}$ |
| `ai_sleep_interaction` | Float | `BEHAVIORAL` | 0.0 – 105.9 | Cross-modal displacement: $\text{Daily\_AI\_Tool\_Usage\_Hours} \times \text{Sleep\_Hours}$ |
| `social_physical_interaction` | Float | `BEHAVIORAL` | 0.0 – 70.0 | Sedentary screen vs exercise balance: $\text{Social\_Media} \times \text{Physical\_Activity}$ |
| `digital_lifestyle_load` (DLL) | Float | `DIGITAL_INTENSITY` | $\approx -3.0$ to $+3.5$ SD | First principal component score from standardized daily digital indicators |
