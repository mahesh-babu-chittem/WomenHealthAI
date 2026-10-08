import pandas as pd
import json
from pathlib import Path

DATA_PATH = Path(
    "data/processed/clean_master_dataframe.csv"
)

RESULTS_DIR = Path("results/stage2_eda")
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(DATA_PATH)

# ==========================================
# MISSING VALUES
# ==========================================

missing = (
    df.isnull()
    .sum()
    .sort_values(ascending=False)
)

missing_df = pd.DataFrame({
    "feature": missing.index,
    "missing_count": missing.values,
    "missing_percent":
        (missing.values / len(df))*100
})

missing_df.to_csv(
    RESULTS_DIR / "missing_value_report.csv",
    index=False
)

missing_report = {
    "total_missing":
        int(df.isnull().sum().sum()),

    "features_with_missing":
        int((missing > 0).sum())
}

with open(
    RESULTS_DIR / "missing_value_report.json",
    "w"
) as f:

    json.dump(missing_report, f, indent=4)

print("Missing value analysis completed.")