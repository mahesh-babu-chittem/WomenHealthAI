import pandas as pd

results = pd.read_csv(
    "results/stage7_intervention/intervention_recommendations.csv"
)

print("\n====================")
print("RISK DISTRIBUTION")
print("====================\n")

print(
    results["Risk"]
    .value_counts()
)