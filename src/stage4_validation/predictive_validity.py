import pandas as pd
from scipy.stats import pearsonr
import json
from pathlib import Path

RESULTS_DIR = Path(
    "results/stage4_validation"
)

df = pd.read_csv(
    "data/processed/rhrs_dataset.csv"
)

symptoms = [
    "headaches",
    "cramps",
    "fatigue",
    "foodcravings",
    "bloating"
]

df["symptom_burden"] = (
    df[symptoms]
    .mean(axis=1)
)

r,p = pearsonr(
    df["RHRS"],
    df["symptom_burden"]
)

results = {
    "correlation":
        float(r),
    "p_value":
        float(p)
}

with open(
    RESULTS_DIR /
    "predictive_validity.json",
    "w"
) as f:

    json.dump(
        results,
        f,
        indent=4
    )

pd.DataFrame(
    [results]
).to_csv(
    RESULTS_DIR /
    "Table_14_Predictive_Validity.csv",
    index=False
)

print(results)