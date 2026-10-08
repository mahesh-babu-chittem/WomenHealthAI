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

features = [
    "sleep_score",
    "mean_rmssd",
    "stress_score",
    "lh",
    "estrogen",
    "pdg"
]

results = {}

for col in features:

    try:

        r,p = pearsonr(
            df["RHRS"],
            df[col]
        )

        results[col] = {
            "pearson_r":
                float(r),
            "p_value":
                float(p)
        }

    except:

        pass

with open(
    RESULTS_DIR /
    "convergent_validity.json",
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
    "Table_12_Convergent_Validity.csv"
)

print(results)