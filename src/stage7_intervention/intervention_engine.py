import json
import pandas as pd

from pathlib import Path

from src.stage7_intervention.risk_stratification import (
    classify_risk
)

from src.stage7_intervention.resilience_interventions import (
    generate_resilience_interventions
)

RESULTS_DIR = Path(
    "results/stage7_intervention"
)

RESULTS_DIR.mkdir(
    parents=True,
    exist_ok=True
)

# ==========================================
# LOAD DATA
# ==========================================

df = pd.read_csv(
    "data/processed/rhrs_dataset.csv"
)

# Latest record of each participant

patients = (

    df.sort_values(
        ["id","day_in_study"]
    )

    .groupby("id")

    .tail(1)

)

outputs = []

for _, patient in patients.iterrows():

    risk = classify_risk(
        patient["RHRS"]
    )

    interventions = (
        generate_resilience_interventions(
            patient
        )
    )

    outputs.append({

        "Participant":
            patient["id"],

        "RHRS":
            patient["RHRS"],

        "Risk":
            risk,

        "Interventions":
            "; ".join(
                interventions
            )

    })

results = pd.DataFrame(
    outputs
)

results.to_csv(

    RESULTS_DIR /
    "intervention_recommendations.csv",

    index=False
)

print(results.head())