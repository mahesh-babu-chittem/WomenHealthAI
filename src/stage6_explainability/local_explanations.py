import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from pathlib import Path

# ==========================================
# PATHS
# ==========================================

RESULTS_DIR = Path(
    "results/stage6_explainability"
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

predictions = pd.read_csv(
    "results/stage5_forecasting/tft_predictions.csv"
)

feature_importance = pd.read_csv(
    RESULTS_DIR /
    "Table_22_Feature_Importance.csv"
)

# ==========================================
# MOST IMPORTANT FEATURES
# ==========================================

top_features = (

    feature_importance

    .sort_values(
        "Importance",
        ascending=False
    )

    .head(10)

)

top_feature_names = list(
    top_features["Feature"]
)

# ==========================================
# SELECT EXAMPLE PATIENT
# ==========================================

sample_idx = len(predictions) // 2

actual_value = (
    predictions.iloc[
        sample_idx
    ]["Actual"]
)

predicted_value = (
    predictions.iloc[
        sample_idx
    ]["Predicted"]
)

# ==========================================
# LATEST RECORD
# ==========================================

patient_row = df.iloc[-1]

# ==========================================
# CONTRIBUTIONS
# ==========================================

contributions = []

for feature in top_feature_names:

    if feature not in patient_row.index:
        continue

    value = patient_row[
        feature
    ]

    importance = float(

        top_features[
            top_features["Feature"] == feature
        ]["Importance"].values[0]

    )

    contribution = (

        value * importance

    )

    contributions.append([

        feature,
        value,
        importance,
        contribution

    ])

# ==========================================
# DATAFRAME
# ==========================================

contrib_df = pd.DataFrame(

    contributions,

    columns=[

        "Feature",
        "Value",
        "Importance",
        "Contribution"

    ]

)

contrib_df = (

    contrib_df

    .sort_values(
        "Contribution",
        ascending=False
    )

)

contrib_df.to_csv(

    RESULTS_DIR /
    "Table_26_Local_Explanation.csv",

    index=False

)

# ==========================================
# VISUALIZATION
# ==========================================

plt.figure(
    figsize=(10,6)
)

plt.barh(

    contrib_df["Feature"],

    contrib_df["Contribution"]

)

plt.gca().invert_yaxis()

plt.xlabel(
    "Contribution Score"
)

plt.ylabel(
    "Feature"
)

plt.title(
    "Local Explanation for TFT Prediction"
)

plt.tight_layout()

plt.savefig(

    RESULTS_DIR /
    "Figure_15_Local_Explanation.png",

    dpi=300

)

plt.close()

# ==========================================
# REPORT
# ==========================================

report = []

report.append(
    "LOCAL EXPLANATION REPORT"
)

report.append(
    "=" * 50
)

report.append("")

report.append(

    f"Actual RHRS: {actual_value:.3f}"

)

report.append(

    f"Predicted RHRS: {predicted_value:.3f}"

)

report.append("")

report.append(
    "TOP CONTRIBUTORS"
)

report.append("")

for _, row in contrib_df.head(10).iterrows():

    report.append(

        f"{row['Feature']} | "
        f"Value={row['Value']:.3f} | "
        f"Contribution={row['Contribution']:.3f}"

    )

with open(

    RESULTS_DIR /
    "Local_Explanation_Report.txt",

    "w"

) as f:

    f.write(
        "\n".join(report)
    )

# ==========================================
# PRINT
# ==========================================

print("\n===================")
print("LOCAL EXPLANATION")
print("===================\n")

print(
    f"Actual RHRS: {actual_value:.3f}"
)

print(
    f"Predicted RHRS: {predicted_value:.3f}"
)

print("\nTop Contributors:\n")

print(
    contrib_df.head(10)
)

print("\nSaved:\n")

print(
    RESULTS_DIR /
    "Table_26_Local_Explanation.csv"
)

print(
    RESULTS_DIR /
    "Figure_15_Local_Explanation.png"
)

print(
    RESULTS_DIR /
    "Local_Explanation_Report.txt"
)