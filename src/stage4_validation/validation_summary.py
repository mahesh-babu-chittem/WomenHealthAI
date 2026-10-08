import json
from pathlib import Path

RESULTS_DIR = Path(
    "results/stage4_validation"
)

files = [
    "reliability_results.json",
    "convergent_validity.json",
    "known_group_results.json",
    "predictive_validity.json"
]

summary = {}

for file in files:

    with open(
        RESULTS_DIR / file
    ) as f:

        summary[file] = json.load(f)

with open(
    RESULTS_DIR /
    "validation_summary.json",
    "w"
) as f:

    json.dump(
        summary,
        f,
        indent=4
    )

print("Validation summary saved.")