import pandas as pd
import json
from pathlib import Path

df = pd.read_csv(
    "data/processed/rhrs_dataset.csv"
)

results = {}

scores = [
    "HRS",
    "PRS",
    "MRS",
    "BRS",
    "SRS",
    "RHRS"
]

for col in scores:

    results[col] = {
        "mean": float(df[col].mean()),
        "std": float(df[col].std()),
        "min": float(df[col].min()),
        "max": float(df[col].max())
    }

Path(
    "results/stage3_rhrs"
).mkdir(
    parents=True,
    exist_ok=True
)

with open(
    "results/stage3_rhrs/rhrs_diagnostics.json",
    "w"
) as f:

    json.dump(
        results,
        f,
        indent=4
    )

print(json.dumps(
    results,
    indent=4
))