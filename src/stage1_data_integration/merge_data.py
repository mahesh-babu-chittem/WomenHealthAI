import pandas as pd
import json
from pathlib import Path

# ==================================================
# PATHS
# ==================================================

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")
RESULTS_DIR = Path("results/stage1_data_integration")

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

# ==================================================
# LOAD FILES
# ==================================================

hormones = pd.read_csv(RAW_DIR / "hormones_and_selfreport.csv")

hrv = pd.read_csv(RAW_DIR / "heart_rate_variability_details.csv")

rhr = pd.read_csv(RAW_DIR / "resting_heart_rate.csv")

sleep = pd.read_csv(RAW_DIR / "sleep_score.csv")

stress = pd.read_csv(RAW_DIR / "stress_score.csv")

glucose = pd.read_csv(RAW_DIR / "glucose.csv")

# ==================================================
# DAILY AGGREGATION
# ==================================================

hrv_daily = (
    hrv.groupby(["id", "day_in_study"])
    .agg(
        mean_rmssd=("rmssd", "mean"),
        std_rmssd=("rmssd", "std"),
        mean_lf=("low_frequency", "mean"),
        mean_hf=("high_frequency", "mean"),
        hrv_samples=("rmssd", "count"),
    )
    .reset_index()
)

glucose_daily = (
    glucose.groupby(["id", "day_in_study"])
    .agg(
        mean_glucose=("glucose_value", "mean"),
        std_glucose=("glucose_value", "std"),
        min_glucose=("glucose_value", "min"),
        max_glucose=("glucose_value", "max"),
    )
    .reset_index()
)

rhr_daily = (
    rhr.groupby(["id", "day_in_study"])
    .agg(
        resting_hr=("value", "mean"),
    )
    .reset_index()
)

sleep_daily = (
    sleep.groupby(["id", "day_in_study"])
    .agg(
        sleep_score=("overall_score", "mean"),
        composition_score=("composition_score", "mean"),
        revitalization_score=("revitalization_score", "mean"),
        duration_score=("duration_score", "mean"),
        deep_sleep=("deep_sleep_in_minutes", "mean"),
        sleep_restlessness=("restlessness", "mean"),
    )
    .reset_index()
)

stress_daily = (
    stress.groupby(["id", "day_in_study"])
    .agg(
        stress_score=("stress_score", "mean"),
    )
    .reset_index()
)

# ==================================================
# MERGE
# ==================================================

master = hormones.copy()

master = master.merge(
    hrv_daily,
    on=["id", "day_in_study"],
    how="left"
)

master = master.merge(
    glucose_daily,
    on=["id", "day_in_study"],
    how="left"
)

master = master.merge(
    rhr_daily,
    on=["id", "day_in_study"],
    how="left"
)

master = master.merge(
    sleep_daily,
    on=["id", "day_in_study"],
    how="left"
)

master = master.merge(
    stress_daily,
    on=["id", "day_in_study"],
    how="left"
)

# ==================================================
# SAVE MASTER DATAFRAME
# ==================================================

master.to_csv(
    PROCESSED_DIR / "master_dataframe.csv",
    index=False
)

print("Master dataframe saved.")
print(master.shape)

# ==================================================
# REPORTS
# ==================================================

integration_report = {
    "participants": int(master["id"].nunique()),
    "rows": int(master.shape[0]),
    "columns": int(master.shape[1]),
    "features": list(master.columns)
}

with open(
    RESULTS_DIR / "integration_report.json",
    "w"
) as f:
    json.dump(integration_report, f, indent=4)

participant_summary = (
    master.groupby("id")
    .size()
    .to_dict()
)

with open(
    RESULTS_DIR / "participant_summary.json",
    "w"
) as f:
    json.dump(participant_summary, f, indent=4)

feature_summary = {}

for col in master.select_dtypes(include="number").columns:

    feature_summary[col] = {
        "mean": float(master[col].mean())
        if pd.notna(master[col].mean())
        else None,

        "std": float(master[col].std())
        if pd.notna(master[col].std())
        else None,

        "min": float(master[col].min())
        if pd.notna(master[col].min())
        else None,

        "max": float(master[col].max())
        if pd.notna(master[col].max())
        else None,
    }

with open(
    RESULTS_DIR / "feature_summary.json",
    "w"
) as f:
    json.dump(feature_summary, f, indent=4)

print("Reports generated.")