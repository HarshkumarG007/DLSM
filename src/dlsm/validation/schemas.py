try:
    import pandera.pandas as pa
    from pandera.pandas import Column, Check, DataFrameSchema
except ImportError:
    import pandera as pa
    from pandera import Column, Check, DataFrameSchema


schema_dataset_a = DataFrameSchema(
    {
        "user_id": Column(str, nullable=False),
        "age": Column(int, Check.in_range(18, 100), nullable=False),
        "gender": Column(str, Check.isin(["Female", "Male", "Non-Binary"]), nullable=False),
        "occupation_type": Column(str, nullable=False),
        "chronotype": Column(str, Check.isin(["Intermediate", "Night Owl", "Morning Lark"]), nullable=False),
        "bedtime_phone_minutes": Column(int, Check.in_range(0, 360), nullable=False),
        "primary_bedtime_app": Column(str, nullable=False),
        "screen_brightness_pct": Column(int, Check.in_range(0, 100), nullable=False),
        "blue_light_filter_active": Column(int, Check.isin([0, 1]), nullable=False),
        "caffeine_post_5pm_mg": Column(int, Check.greater_than_or_equal_to(0), nullable=False),
        "physical_activity_min": Column(int, Check.greater_than_or_equal_to(0), nullable=False),
        "sleep_latency_min": Column(float, Check.greater_than(0), nullable=False),
        "total_sleep_hours": Column(float, Check.in_range(1.0, 18.0), nullable=False),
        "deep_sleep_pct": Column(float, Check.in_range(0.0, 100.0), nullable=False),
        "rem_sleep_pct": Column(float, Check.in_range(0.0, 100.0), nullable=False),
        "morning_alarm_snoozes": Column(int, Check.greater_than_or_equal_to(0), nullable=False),
        "next_day_fatigue_score": Column(float, Check.in_range(1.0, 10.0), nullable=False),
        "sleep_debt_category": Column(str, nullable=False),
    },
    strict=True,
    coerce=True
)

schema_dataset_b = DataFrameSchema(
    {
        "Student_ID": Column(str, nullable=False),
        "Age": Column(int, Check.in_range(10, 50), nullable=False),
        "Gender": Column(str, Check.isin(["Male", "Female", "Non-binary"]), nullable=False),
        "Education_Level": Column(str, Check.isin(["High School", "College", "University"]), nullable=False),
        "Daily_Social_Media_Hours": Column(float, Check.in_range(0.0, 24.0), nullable=False),
        "Daily_AI_Tool_Usage_Hours": Column(float, Check.in_range(0.0, 24.0), nullable=False),
        "Sleep_Hours": Column(float, Check.in_range(1.0, 24.0), nullable=False),
        "Physical_Activity_Hours": Column(float, Check.in_range(0.0, 24.0), nullable=False),
        "Mental_Health_Score": Column(float, Check.in_range(0.0, 100.0), nullable=False),
        "Physical_Health_Score": Column(float, Check.in_range(0.0, 100.0), nullable=False),
    },
    strict=True,
    coerce=True
)

def validate_dataset_a(df):
    return schema_dataset_a.validate(df)

def validate_dataset_b(df):
    return schema_dataset_b.validate(df)
