import ollama
import pandas as pd

from pathlib import Path

RESULTS_DIR = Path(
    "results/stage8_llm"
)

RESULTS_DIR.mkdir(
    parents=True,
    exist_ok=True
)

# =====================================
# LOAD INTERVENTIONS
# =====================================

df = pd.read_csv(
    "results/stage7_intervention/intervention_recommendations.csv"
)

# =====================================
# GENERATE REPORTS
# =====================================

for _, patient in df.iterrows():

    prompt = f"""
You are WomenHealthGPT.

Patient Profile:

RHRS:
{patient['RHRS']:.2f}

Risk Category:
{patient['Risk']}

Interventions:
{patient['Interventions']}

Generate:

1. Health Summary

2. Main Resilience Concerns

3. Personalized Recommendations

4. Monitoring Advice

Requirements:

- Professional clinical tone
- Easy to understand
- Maximum 250 words
- Do not mention AI
- Do not provide medical diagnosis
"""

    response = ollama.chat(

        model="llama3:latest",

        messages=[

            {
                "role": "user",
                "content": prompt
            }

        ]

    )

    report = (
        response["message"]["content"]
    )

    participant_id = int(
        patient["Participant"]
    )

    with open(

        RESULTS_DIR /
        f"patient_{participant_id}.txt",

        "w"

    ) as f:

        f.write(report)

print(
    f"Generated {len(df)} reports."
)