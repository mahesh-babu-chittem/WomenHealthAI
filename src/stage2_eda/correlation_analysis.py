import pandas as pd
import json
import matplotlib.pyplot as plt
import seaborn as sns

from pathlib import Path

DATA_PATH = Path(
    "data/processed/clean_master_dataframe.csv"
)

RESULTS_DIR = Path("results/stage2_eda")
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(DATA_PATH)

# ==========================================
# NUMERIC FEATURES
# ==========================================

numeric_df = df.select_dtypes(include="number")

corr_matrix = numeric_df.corr()

# ==========================================
# SAVE MATRIX
# ==========================================

corr_matrix.to_csv(
    RESULTS_DIR / "Table_3_Correlation_Matrix.csv"
)

corr_matrix.to_json(
    RESULTS_DIR / "correlation_matrix.json",
    indent=4
)

# ==========================================
# HEATMAP
# ==========================================

plt.figure(figsize=(16,12))

sns.heatmap(
    corr_matrix,
    cmap="coolwarm",
    center=0
)

plt.tight_layout()

plt.savefig(
    RESULTS_DIR /
    "Figure_1_Correlation_Heatmap.png",
    dpi=300
)

plt.close()

print("Correlation analysis completed.")