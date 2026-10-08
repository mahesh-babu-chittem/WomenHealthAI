import torch
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

known_reals = [
    "day_in_study"
]

unknown_reals = [

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

training_cutoff = (

    df["time_idx"].max()

    - 14

)

dataset = TimeSeriesDataSet(

    df[
        lambda x:
        x.time_idx <= training_cutoff
    ],

    time_idx="time_idx",

    target="RHRS",

    group_ids=["id"],

    max_encoder_length=14,

    max_prediction_length=14,

    time_varying_known_reals=
        known_reals,

    time_varying_unknown_reals=
        unknown_reals
)

loader = dataset.to_dataloader(

    train=False,

    batch_size=64,

    num_workers=0
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
# RAW PREDICTIONS
# ==========================================

raw_predictions = tft.predict(

    loader,

    mode="raw",

    return_x=True

)

# ==========================================
# INTERPRETATION
# ==========================================

interpretation = (

    tft.interpret_output(

        raw_predictions.output,

        reduction="sum"

    )

)

print("\nINTERPRETATION KEYS\n")

print(
    interpretation.keys()
)

for k,v in interpretation.items():

    print("\n")
    print(k)

    print(type(v))

    if hasattr(v, "shape"):

        print(v.shape)

# ==========================================
# VARIABLE IMPORTANCE
# ==========================================

# ==========================================
# VARIABLE IMPORTANCE
# ==========================================

feature_names = [

    "day_in_study",

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

importance = (
    interpretation[
        "encoder_variables"
    ]
    .cpu()
    .numpy()
)

importance_df = pd.DataFrame({

    "Feature":
        feature_names,

    "Importance":
        importance

})

importance_df = (

    importance_df
    .sort_values(

        by="Importance",

        ascending=False

    )

)

# ==========================================
# SAVE CSV
# ==========================================

importance_df.to_csv(

    RESULTS_DIR /
    "Table_22_Feature_Importance.csv",

    index=False

)

# ==========================================
# PLOT
# ==========================================

plt.figure(
    figsize=(10,8)
)

plt.barh(

    importance_df["Feature"],

    importance_df["Importance"]

)

plt.gca().invert_yaxis()

plt.xlabel(
    "Importance"
)

plt.ylabel(
    "Feature"
)

plt.title(
    "TFT Feature Importance"
)

plt.tight_layout()

plt.savefig(

    RESULTS_DIR /
    "Figure_12_Feature_Importance.png",

    dpi=300

)

plt.close()

# ==========================================
# PRINT
# ==========================================

print("\n====================")
print("FEATURE IMPORTANCE")
print("====================\n")

print(
    importance_df
)

print("\nSaved:\n")

print(
    RESULTS_DIR /
    "Table_22_Feature_Importance.csv"
)

print(
    RESULTS_DIR /
    "Figure_12_Feature_Importance.png"
)