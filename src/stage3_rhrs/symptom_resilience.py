import pandas as pd
from scipy.stats import rankdata
import json
from pathlib import Path

# ==========================================
# PATHS
# ==========================================

RESULTS_DIR = Path("results/stage3_rhrs")
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

# ==========================================
# LOAD DATA
# ==========================================

df = pd.read_csv(
    "data/processed/clean_master_dataframe.csv"
)

# ==========================================
# SYMPTOM FEATURES
# ==========================================

features = [
    "headaches",
    "cramps",
    "fatigue",
    "foodcravings",
    "bloating",
    "stress"
]

# ==========================================
# CLEANING
# ==========================================

for col in features:

    df[col] = pd.to_numeric(
        df[col],
        errors="coerce"
    )

    df[col] = df[col].fillna(
        df[col].median()
    )

# ==========================================
# PERCENTILE NORMALIZATION
# ==========================================

for col in features:

    df[col + "_rank"] = (
        rankdata(df[col])
        /
        len(df)
    ) * 100

# ==========================================
# SYMPTOM BURDEN
# Higher symptom severity = worse health
# ==========================================

symptom_burden = (
    df["headaches_rank"]
    +
    df["cramps_rank"]
    +
    df["fatigue_rank"]
    +
    df["foodcravings_rank"]
    +
    df["bloating_rank"]
    +
    df["stress_rank"]
) / 6

# ==========================================
# SYMPTOM RESILIENCE SCORE
# ==========================================

df["SRS"] = (
    100 - symptom_burden
)

df["SRS"] = df["SRS"].clip(0, 100)

# ==========================================
# SAVE TABLE
# ==========================================

df[
    [
        "id",
        "day_in_study",
        "SRS"
    ]
].to_csv(
    RESULTS_DIR / "Table_9_SRS.csv",
    index=False
)

# ==========================================
# SUMMARY
# ==========================================

summary = {
    "mean": float(df["SRS"].mean()),
    "std": float(df["SRS"].std()),
    "min": float(df["SRS"].min()),
    "max": float(df["SRS"].max())
}

with open(
    RESULTS_DIR / "symptom_resilience.json",
    "w"
) as f:

    json.dump(
        summary,
        f,
        indent=4
    )

print("\nSymptom Resilience Summary")
print(summary)