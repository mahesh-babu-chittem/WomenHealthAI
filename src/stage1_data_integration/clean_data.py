import pandas as pd
import json
from pathlib import Path

DATA_DIR = Path("data/processed")
RESULTS_DIR = Path("results/stage1_data_integration")

df = pd.read_csv(DATA_DIR / "master_dataframe.csv")

rows_before = len(df)

# -----------------------------------
# REMOVE DUPLICATES
# -----------------------------------

duplicates = int(df.duplicated().sum())

df = df.drop_duplicates()

# -----------------------------------
# SYMPTOM MAPPING
# -----------------------------------

symptom_map = {
    "Not at all": 0,
    "Very Low": 1,
    "Low": 2,
    "Moderate": 3,
    "High": 4,
    "Very High": 5
}

symptom_cols = [
    "headaches",
    "cramps",
    "sorebreasts",
    "fatigue",
    "sleepissues",
    "moodswings",
    "stress",
    "foodcravings",
    "indigestion",
    "bloating"
]

for col in symptom_cols:

    if col in df.columns:

        df[col] = (
            df[col]
            .astype(str)
            .str.split("/")
            .str[0]
            .map(symptom_map)
        )

# -----------------------------------
# MISSING VALUES
# -----------------------------------

missing_before = int(df.isna().sum().sum())

numeric_cols = df.select_dtypes(include="number").columns

for col in numeric_cols:

    df[col] = df[col].fillna(df[col].median())

missing_after = int(df.isna().sum().sum())

# -----------------------------------
# SAVE CLEAN DATA
# -----------------------------------

df.to_csv(
    DATA_DIR / "clean_master_dataframe.csv",
    index=False
)

# -----------------------------------
# REPORT
# -----------------------------------

report = {
    "rows_before": rows_before,
    "rows_after": len(df),
    "duplicates_removed": duplicates,
    "missing_before": missing_before,
    "missing_after": missing_after
}

with open(
    RESULTS_DIR / "cleaning_report.json",
    "w"
) as f:

    json.dump(report, f, indent=4)

print("Cleaning completed.")