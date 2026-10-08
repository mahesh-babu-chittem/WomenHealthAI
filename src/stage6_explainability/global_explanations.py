import pandas as pd
import matplotlib.pyplot as plt

from pathlib import Path

RESULTS_DIR = Path(
    "results/stage6_explainability"
)

# ==========================================
# LOAD RESULTS
# ==========================================

feature_df = pd.read_csv(

    RESULTS_DIR /
    "Table_22_Feature_Importance.csv"

)

attention_df = pd.read_csv(

    RESULTS_DIR /
    "Table_23_Attention_Weights.csv"

)

# ==========================================
# TOP FEATURES
# ==========================================

top_features = feature_df.head(10)

top_features.to_csv(

    RESULTS_DIR /
    "Table_24_Top10_Features.csv",

    index=False

)

# ==========================================
# TOP ATTENTION DAYS
# ==========================================

top_days = (

    attention_df

    .sort_values(

        by="Attention_Weight",

        ascending=False

    )

    .head(10)

)

top_days.to_csv(

    RESULTS_DIR /
    "Table_25_Top10_Attention_Days.csv",

    index=False

)

# ==========================================
# COMBINED GLOBAL EXPLANATION
# ==========================================

fig = plt.figure(
    figsize=(14,6)
)

# ------------------------
# FEATURE IMPORTANCE
# ------------------------

plt.subplot(
    1,
    2,
    1
)

plt.barh(

    top_features["Feature"],

    top_features["Importance"]

)

plt.gca().invert_yaxis()

plt.title(
    "Top Feature Importance"
)

plt.xlabel(
    "Importance"
)

# ------------------------
# ATTENTION
# ------------------------

plt.subplot(
    1,
    2,
    2
)

plt.plot(

    attention_df["Historical_Day"],

    attention_df["Attention_Weight"],

    marker="o"
)

plt.title(
    "Temporal Attention"
)

plt.xlabel(
    "Days Before Forecast"
)

plt.ylabel(
    "Attention Weight"
)

plt.grid(True)

plt.tight_layout()

plt.savefig(

    RESULTS_DIR /
    "Figure_14_Global_Explanations.png",

    dpi=300

)

plt.close()

# ==========================================
# REPORT
# ==========================================

report = []

report.append(
    "GLOBAL EXPLANATION REPORT"
)

report.append(
    "=" * 50
)

report.append("\nTOP 10 FEATURES\n")

for _, row in top_features.iterrows():

    report.append(

        f"{row['Feature']} : "
        f"{row['Importance']:.4f}"

    )

report.append(
    "\nTOP 10 ATTENTION DAYS\n"
)

for _, row in top_days.iterrows():

    report.append(

        f"Day {int(row['Historical_Day'])} : "
        f"{row['Attention_Weight']:.6f}"

    )

with open(

    RESULTS_DIR /
    "Global_Explanation_Report.txt",

    "w"

) as f:

    f.write(
        "\n".join(report)
    )

# ==========================================
# PRINT
# ==========================================

print("\n===================")
print("GLOBAL EXPLANATIONS")
print("===================\n")

print(top_features)

print("\n")

print(top_days)

print("\nSaved:\n")

print(
    RESULTS_DIR /
    "Table_24_Top10_Features.csv"
)

print(
    RESULTS_DIR /
    "Table_25_Top10_Attention_Days.csv"
)

print(
    RESULTS_DIR /
    "Figure_14_Global_Explanations.png"
)

print(
    RESULTS_DIR /
    "Global_Explanation_Report.txt"
)