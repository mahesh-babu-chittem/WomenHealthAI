import pandas as pd
from scipy.stats import rankdata
import json
from pathlib import Path

RESULTS_DIR = Path("results/stage3_rhrs")
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(
    "data/processed/clean_master_dataframe.csv"
)

# ==========================================
# FEATURES
# ==========================================

features = [
    "sleep_score",
    "deep_sleep"
]

# ==========================================
# PERCENTILE SCALING
# ==========================================

for col in features:

    df[col] = (
        rankdata(df[col])
        /
        len(df)
    ) * 100

df["stress_score"] = (
    rankdata(df["stress_score"])
    /
    len(df)
) * 100

# ==========================================
# BEHAVIORAL RESILIENCE SCORE
# ==========================================

sleep_component = (
    df["sleep_score"]
    +
    df["deep_sleep"]
) / 2

stress_penalty = (
    0.3 * df["stress_score"]
)

df["BRS"] = (
    sleep_component
    -
    stress_penalty
)

df["BRS"] = df["BRS"].clip(0, 100)

# ==========================================
# SAVE TABLE
# ==========================================

df[
    [
        "id",
        "day_in_study",
        "BRS"
    ]
].to_csv(
    RESULTS_DIR / "Table_8_BRS.csv",
    index=False
)

# ==========================================
# SUMMARY
# ==========================================

summary = {
    "mean": float(df["BRS"].mean()),
    "std": float(df["BRS"].std()),
    "min": float(df["BRS"].min()),
    "max": float(df["BRS"].max())
}

with open(
    RESULTS_DIR / "behavioral_resilience.json",
    "w"
) as f:

    json.dump(
        summary,
        f,
        indent=4
    )

print("\nBehavioral Resilience Summary")
print(summary)