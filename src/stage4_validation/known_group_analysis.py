import pandas as pd
from scipy.stats import ttest_ind
import json
from pathlib import Path

RESULTS_DIR = Path(
    "results/stage4_validation"
)

df = pd.read_csv(
    "data/processed/rhrs_dataset.csv"
)

q25 = df["RHRS"].quantile(0.25)

q75 = df["RHRS"].quantile(0.75)

low_group = df[
    df["RHRS"] <= q25
]

high_group = df[
    df["RHRS"] >= q75
]

features = [
    "sleep_score",
    "mean_rmssd",
    "stress_score",
    "mean_glucose"
]

results = {}

for col in features:

    t,p = ttest_ind(
        high_group[col],
        low_group[col],
        nan_policy="omit"
    )

    results[col] = {
        "t_stat":
            float(t),
        "p_value":
            float(p)
    }

with open(
    RESULTS_DIR /
    "known_group_results.json",
    "w"
) as f:

    json.dump(
        results,
        f,
        indent=4
    )

pd.DataFrame(
    results
).T.to_csv(
    RESULTS_DIR /
    "Table_13_Known_Groups.csv"
)

print(results)
