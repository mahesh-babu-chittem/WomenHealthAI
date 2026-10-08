import pandas as pd
import json
from pathlib import Path

DATA_PATH = Path("data/processed/clean_master_dataframe.csv")

RESULTS_DIR = Path("results/stage2_eda")
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(DATA_PATH)

# ==========================================
# DATASET CHARACTERISTICS
# ==========================================

dataset_stats = {
    "participants": int(df["id"].nunique()),
    "total_rows": int(len(df)),
    "total_columns": int(df.shape[1]),
    "total_features": int(df.shape[1] - 4)
}

with open(
    RESULTS_DIR / "descriptive_statistics.json",
    "w"
) as f:

    json.dump(dataset_stats, f, indent=4)

# ==========================================
# TABLE 1
# ==========================================

table1 = pd.DataFrame([dataset_stats])

table1.to_csv(
    RESULTS_DIR / "Table_1_Dataset_Characteristics.csv",
    index=False
)

# ==========================================
# TABLE 2
# ==========================================

numeric_df = df.select_dtypes(include="number")

feature_stats = numeric_df.describe().T

feature_stats["median"] = numeric_df.median()

feature_stats.to_csv(
    RESULTS_DIR / "Table_2_Feature_Statistics.csv"
)

print("Descriptive statistics completed.")