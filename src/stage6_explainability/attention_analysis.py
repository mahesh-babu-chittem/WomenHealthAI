import torch
import pandas as pd
import numpy as np
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
    df["time_idx"].max() - 14
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
# LOAD MODEL
# ==========================================

tft = (
    TemporalFusionTransformer
    .load_from_checkpoint(
        CHECKPOINT
    )
)

tft.eval()

# ==========================================
# RAW OUTPUTS
# ==========================================

raw_predictions = tft.predict(

    loader,

    mode="raw",

    return_x=True
)

# ==========================================
# INTERPRET
# ==========================================

interpretation = tft.interpret_output(

    raw_predictions.output,

    reduction="mean"
)

attention = (
    interpretation["attention"]
    .cpu()
    .numpy()
)

# ==========================================
# SAVE CSV
# ==========================================

attention_df = pd.DataFrame({

    "Historical_Day": np.arange(
        -13,
        1
    ),

    "Attention_Weight":
        attention

})

attention_df.to_csv(

    RESULTS_DIR /
    "Table_23_Attention_Weights.csv",

    index=False
)

# ==========================================
# PLOT
# ==========================================

plt.figure(
    figsize=(10,6)
)

plt.plot(

    attention_df[
        "Historical_Day"
    ],

    attention_df[
        "Attention_Weight"
    ],

    marker="o"
)

plt.xlabel(
    "Days Before Forecast"
)

plt.ylabel(
    "Attention Weight"
)

plt.title(
    "Temporal Attention Analysis"
)

plt.grid(True)

plt.tight_layout()

plt.savefig(

    RESULTS_DIR /
    "Figure_13_Attention_Weights.png",

    dpi=300

)

plt.close()

# ==========================================
# PRINT
# ==========================================

print("\n====================")
print("ATTENTION WEIGHTS")
print("====================\n")

print(
    attention_df
)

print("\nSaved:\n")

print(
    RESULTS_DIR /
    "Table_23_Attention_Weights.csv"
)

print(
    RESULTS_DIR /
    "Figure_13_Attention_Weights.png"
)