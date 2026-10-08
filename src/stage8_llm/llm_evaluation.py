import pandas as pd
import textstat

from pathlib import Path

REPORT_DIR = Path(
    "results/stage8_llm"
)

interventions = pd.read_csv(
    "results/stage7_intervention/intervention_recommendations.csv"
)

results = []

for _, row in interventions.iterrows():

    patient_id = int(
        row["Participant"]
    )

    report_file = (
        REPORT_DIR /
        f"patient_{patient_id}.txt"
    )

    if not report_file.exists():
        continue

    report = report_file.read_text()

    # ==========================
    # WORD COUNT
    # ==========================

    words = len(
        report.split()
    )

    # ==========================
    # READABILITY
    # ==========================

    readability = (
        textstat.flesch_reading_ease(
            report
        )
    )

    # ==========================
    # GUIDANCE FIDELITY
    # ==========================

    interventions_text = (
        str(row["Interventions"])
        .lower()
    )

    report_text = (
        report.lower()
    )

    expected = []

    if "hormonal" in interventions_text:
        expected.append(
            "hormonal"
        )

    if "psychological" in interventions_text:
        expected.append(
            "psychological"
        )

    if "metabolic" in interventions_text:
        expected.append(
            "metabolic"
        )

    if "behavioral" in interventions_text:
        expected.append(
            "behavioral"
        )

    if "symptom" in interventions_text:
        expected.append(
            "symptom"
        )

    if "overall resilience" in interventions_text:
        expected.append(
            "resilience"
        )

    covered = 0

    for term in expected:

        if term in report_text:

            covered += 1

    gfs = (

        covered / len(expected)

        if len(expected) > 0

        else 1.0

    )

    results.append({

        "Participant":
            patient_id,

        "WordCount":
            words,

        "Readability":
            readability,

        "GFS":
            gfs

    })

eval_df = pd.DataFrame(
    results
)

eval_df.to_csv(

    REPORT_DIR /
    "llm_evaluation.csv",

    index=False
)

print("\n====================")
print("LLM EVALUATION")
print("====================\n")

print(

    eval_df[
        [
            "WordCount",
            "Readability",
            "GFS"
        ]

    ].mean()

)