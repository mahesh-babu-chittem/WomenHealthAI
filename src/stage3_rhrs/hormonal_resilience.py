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
# HORMONAL FEATURES
# ==========================================

features = [
    "lh",
    "estrogen",
    "pdg"
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
# HORMONAL RESILIENCE SCORE
# ==========================================

df["HRS"] = (
    df["lh"]
    +
    df["estrogen"]
    +
    df["pdg"]
) / 3

df["HRS"] = df["HRS"].clip(0, 100)

# ==========================================
# SAVE TABLE
# ==========================================

df[
    [
        "id",
        "day_in_study",
        "HRS"
    ]
].to_csv(
    RESULTS_DIR / "Table_5_HRS.csv",
    index=False
)

# ==========================================
# SUMMARY
# ==========================================

summary = {
    "mean": float(df["HRS"].mean()),
    "std": float(df["HRS"].std()),
    "min": float(df["HRS"].min()),
    "max": float(df["HRS"].max())
}

with open(
    RESULTS_DIR / "hormonal_resilience.json",
    "w"
) as f:

    json.dump(
        summary,
        f,
        indent=4
    )

print("\nHormonal Resilience Summary")
print(summary)