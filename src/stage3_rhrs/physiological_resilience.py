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
# PHYSIOLOGICAL FEATURES
# ==========================================

features = [
    "mean_rmssd",
    "mean_lf",
    "mean_hf"
]

# ==========================================
# PERCENTILE NORMALIZATION
# ==========================================

for col in features:

    df[col] = pd.to_numeric(
        df[col],
        errors="coerce"
    )

    df[col] = df[col].fillna(
        df[col].median()
    )

    df[col] = (
        rankdata(df[col])
        /
        len(df)
    ) * 100

# ==========================================
# RESTING HR
# Lower RHR = Better Physiology
# ==========================================

df["resting_hr"] = pd.to_numeric(
    df["resting_hr"],
    errors="coerce"
)

df["resting_hr"] = df["resting_hr"].fillna(
    df["resting_hr"].median()
)

df["resting_hr"] = (
    rankdata(df["resting_hr"])
    /
    len(df)
) * 100

# Invert because lower HR is better

df["resting_hr_score"] = (
    100 - df["resting_hr"]
)

# ==========================================
# PHYSIOLOGICAL RESILIENCE SCORE
# ==========================================

df["PRS"] = (
    df["mean_rmssd"]
    +
    df["mean_lf"]
    +
    df["mean_hf"]
    +
    df["resting_hr_score"]
) / 4

df["PRS"] = df["PRS"].clip(0, 100)

# ==========================================
# SAVE TABLE
# ==========================================

df[
    [
        "id",
        "day_in_study",
        "PRS"
    ]
].to_csv(
    RESULTS_DIR / "Table_6_PRS.csv",
    index=False
)

# ==========================================
# SUMMARY
# ==========================================

summary = {
    "mean": float(df["PRS"].mean()),
    "std": float(df["PRS"].std()),
    "min": float(df["PRS"].min()),
    "max": float(df["PRS"].max())
}

with open(
    RESULTS_DIR / "physiological_resilience.json",
    "w"
) as f:

    json.dump(
        summary,
        f,
        indent=4
    )

print("\nPhysiological Resilience Summary")
print(summary)