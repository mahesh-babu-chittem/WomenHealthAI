import shap
import torch
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from pathlib import Path

from pytorch_forecasting import (
    TimeSeriesDataSet,
    TemporalFusionTransformer
)

# ==========================================
# PATHS
# ==========================================

CHECKPOINT = (
    "results/stage5_forecasting/"
    "checkpoints/tft_final.ckpt"
)

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

df = df.sort_values(
    ["id", "day_in_study"]
)

df["time_idx"] = (
    df.groupby("id")
      .cumcount()
)

# ==========================================
# FEATURES
# ==========================================

feature_names = [

    "RHRS",

    "HRS",
    "PRS",
    "MRS",
    "BRS",
    "SRS",

    "lh",
    "estrogen",
    "pdg",

    "mean_rmssd",
    "mean_lf",
    "mean_hf",

    "mean_glucose",
    "std_glucose",

    "resting_hr",

    "sleep_score",
    "deep_sleep",

    "stress_score"

]

# ==========================================
# SIMPLE TABULAR VIEW
# ==========================================

X = df[
    feature_names
].copy()

# use fewer samples
X_background = X.sample(
    100,
    random_state=42
)

X_explain = X.sample(
    50,
    random_state=123
)

# ==========================================
# LOAD TFT
# ==========================================

tft = (

    TemporalFusionTransformer
    .load_from_checkpoint(
        CHECKPOINT
    )

)

tft.eval()

# ==========================================
# SURROGATE PREDICTOR
# ==========================================

global_importance = pd.read_csv(
    RESULTS_DIR /
    "Table_22_Feature_Importance.csv"
)

importance_dict = dict(

    zip(

        global_importance["Feature"],

        global_importance["Importance"]

    )

)

weights = np.array([

    importance_dict[f]

    for f in feature_names

])

weights = weights / weights.sum()

def surrogate_predict(X_input):

    X_input = np.asarray(
        X_input
    )

    return np.dot(
        X_input,
        weights
    )

# ==========================================
# SHAP
# ==========================================

explainer = shap.KernelExplainer(

    surrogate_predict,

    X_background

)

shap_values = explainer.shap_values(

    X_explain,

    nsamples=100

)

# ==========================================
# SAVE SHAP TABLE
# ==========================================

mean_abs_shap = np.abs(
    shap_values
).mean(axis=0)

shap_df = pd.DataFrame({

    "Feature":
        feature_names,

    "MeanAbsSHAP":
        mean_abs_shap

})

shap_df = shap_df.sort_values(

    "MeanAbsSHAP",

    ascending=False

)

shap_df.to_csv(

    RESULTS_DIR /
    "Table_27_SHAP_Importance.csv",

    index=False

)

# ==========================================
# BAR PLOT
# ==========================================

plt.figure(
    figsize=(10,6)
)

plt.barh(

    shap_df["Feature"],

    shap_df["MeanAbsSHAP"]

)

plt.gca().invert_yaxis()

plt.title(
    "SHAP Feature Importance"
)

plt.tight_layout()

plt.savefig(

    RESULTS_DIR /
    "Figure_16_SHAP_Barplot.png",

    dpi=300

)

plt.close()

# ==========================================
# SUMMARY PLOT
# ==========================================

shap.summary_plot(

    shap_values,

    X_explain,

    feature_names=feature_names,

    show=False

)

plt.tight_layout()

plt.savefig(

    RESULTS_DIR /
    "Figure_17_SHAP_Summary.png",

    dpi=300

)

plt.close()

# ==========================================
# PRINT
# ==========================================

print("\n===================")
print("SHAP ANALYSIS")
print("===================\n")

print(
    shap_df.head(10)
)

print("\nSaved:\n")

print(
    RESULTS_DIR /
    "Table_27_SHAP_Importance.csv"
)

print(
    RESULTS_DIR /
    "Figure_16_SHAP_Barplot.png"
)

print(
    RESULTS_DIR /
    "Figure_17_SHAP_Summary.png"
)