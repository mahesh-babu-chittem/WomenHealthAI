import pandas as pd
import json
from pathlib import Path

RESULTS_DIR = Path("results/stage4_validation")
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(
    "data/processed/rhrs_dataset.csv"
)

items = df[
    [
        "HRS",
        "PRS",
        "MRS",
        "BRS",
        "SRS"
    ]
]

k = items.shape[1]

item_variances = items.var(axis=0, ddof=1)

total_score = items.sum(axis=1)

total_variance = total_score.var(ddof=1)

cronbach_alpha = (
    k/(k-1)
) * (
    1 - item_variances.sum()/total_variance
)

results = {
    "cronbach_alpha":
        float(cronbach_alpha)
}

with open(
    RESULTS_DIR /
    "reliability_results.json",
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
    "Table_11_Reliability.csv",
    index=False
)

print(results)
