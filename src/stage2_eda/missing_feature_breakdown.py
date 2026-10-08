import pandas as pd
import json
from pathlib import Path

# ==========================================
# PATHS
# ==========================================

DATA_PATH = Path(
    "data/processed/clean_master_dataframe.csv"
)

RESULTS_DIR = Path("results/stage2_eda")
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

# ==========================================
# LOAD DATA
# ==========================================

df = pd.read_csv(DATA_PATH)

# ==========================================
# MISSING VALUE BREAKDOWN
# ==========================================

missing_counts = df.isnull().sum()

missing_counts = missing_counts[
    missing_counts > 0
].sort_values(ascending=False)

missing_df = pd.DataFrame({
    "feature": missing_counts.index,
    "missing_count": missing_counts.values,
    "missing_percentage":
        (
            missing_counts.values / len(df)
        ) * 100
})

# ==========================================
# SAVE CSV
# ==========================================

missing_df.to_csv(
    RESULTS_DIR /
    "Table_4_Missing_Feature_Breakdown.csv",
    index=False
)

# ==========================================
# SAVE JSON
# ==========================================

missing_json = {}

for _, row in missing_df.iterrows():

    missing_json[row["feature"]] = {
        "missing_count":
            int(row["missing_count"]),

        "missing_percentage":
            round(
                float(
                    row["missing_percentage"]
                ),
                4
            )
    }

with open(
    RESULTS_DIR /
    "missing_feature_breakdown.json",
    "w"
) as f:

    json.dump(
        missing_json,
        f,
        indent=4
    )

# ==========================================
# CONSOLE OUTPUT
# ==========================================

print("\n===== MISSING FEATURE BREAKDOWN =====\n")

if len(missing_df) == 0:

    print("No missing values found.")

else:

    print(missing_df)

print(
    f"\nFeatures with missing values: "
    f"{len(missing_df)}"
)

print(
    f"Total missing cells: "
    f"{int(df.isnull().sum().sum())}"
)

print("\nFiles saved:")
print(
    "Table_4_Missing_Feature_Breakdown.csv"
)
print(
    "missing_feature_breakdown.json"
)