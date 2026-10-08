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
# GLUCOSE FEATURES
# ==========================================

features = [
    "mean_glucose",
    "std_glucose"
]

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

df["mean_glucose_rank"] = (
    rankdata(df["mean_glucose"])
    /
    len(df)
) * 100

df["std_glucose_rank"] = (
    rankdata(df["std_glucose"])
    /
    len(df)
) * 100

# ==========================================
# INVERT SCORES
# Lower glucose variability is healthier
# Lower glucose burden is healthier
# ==========================================

df["glucose_health"] = (
    100 - df["mean_glucose_rank"]
)

df["variability_health"] = (
    100 - df["std_glucose_rank"]
)

# ==========================================
# METABOLIC RESILIENCE SCORE
# ==========================================

df["MRS"] = (
    0.6 * df["glucose_health"]
    +
    0.4 * df["variability_health"]
)

df["MRS"] = df["MRS"].clip(0, 100)

# ==========================================
# SAVE TABLE
# ==========================================

df[
    [
        "id",
        "day_in_study",
        "MRS"
    ]
].to_csv(
    RESULTS_DIR / "Table_7_MRS.csv",
    index=False
)

# ==========================================
# SUMMARY
# ==========================================

summary = {
    "mean": float(df["MRS"].mean()),
    "std": float(df["MRS"].std()),
    "min": float(df["MRS"].min()),
    "max": float(df["MRS"].max())
}

with open(
    RESULTS_DIR / "metabolic_resilience.json",
    "w"
) as f:

    json.dump(
        summary,
        f,
        indent=4
    )

print("\nMetabolic Resilience Summary")
print(summary)