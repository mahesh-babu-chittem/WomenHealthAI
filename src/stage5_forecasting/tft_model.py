import json
from pathlib import Path
import numpy as np
import pandas as pd

from lightning.pytorch import Trainer
from lightning.pytorch.callbacks import ModelCheckpoint
from pytorch_forecasting import TimeSeriesDataSet, TemporalFusionTransformer
from pytorch_forecasting.metrics import RMSE
from pytorch_forecasting.data import TorchNormalizer

from src.stage5_forecasting.metrics_regression import compute_all_metrics
from src.stage5_forecasting.config import HORIZON
from src.stage5_forecasting.evaluation_utils import load_canonical_split, RESULTS_DIR

RESULTS_DIR.mkdir(parents=True, exist_ok=True)
TEMPORAL_DIR = Path("data/processed/temporal_windows")

FEATURE_COLUMNS = [
    "lh", "estrogen", "pdg",
    "mean_rmssd", "mean_lf", "mean_hf",
    "resting_hr",
    "mean_glucose", "std_glucose",
    "sleep_score", "deep_sleep",
    "stress_score",
    "headaches", "cramps", "fatigue", "foodcravings", "bloating",
    "HRS", "PRS", "MRS", "BRS", "SRS"
]

UNKNOWN_REALS = FEATURE_COLUMNS + ["RHRS"]


def build_canonical_tft_frame(horizon):
    """Create one independent 14-day encoder + H-day decoder sequence per canonical window.

    Each sequence is keyed by window_id, so the TFT sees exactly the same forecast
    instances used by every baseline. Future unknown covariates are intentionally
    unavailable (NaN); only day_in_study is known in the decoder and RHRS is retained
    as the supervised target.
    """
    source = pd.read_csv("data/processed/rhrs_dataset.csv")
    source = source.sort_values(["id", "day_in_study"])
    meta = pd.read_csv(TEMPORAL_DIR / f"window_metadata_h{horizon}.csv")

    rows = []
    for _, m in meta.iterrows():
        pid = m["participant_id"]
        start_day = m["input_start_day"]
        end_day = m["input_end_day"]
        target_day = m["target_day"]
        window_id = f"W{int(m['window_index'])}"

        p = source[source["id"] == pid].copy().sort_values("day_in_study")
        encoder = p[(p["day_in_study"] >= start_day) & (p["day_in_study"] <= end_day)].copy()
        decoder = p[(p["day_in_study"] > end_day) & (p["day_in_study"] <= target_day)].copy()

        if len(encoder) != 14 or len(decoder) != horizon:
            raise ValueError(
                f"Canonical TFT sequence mismatch for window {window_id}: "
                f"encoder={len(encoder)}, decoder={len(decoder)}, expected 14/{horizon}."
            )

        for t, (_, r) in enumerate(encoder.iterrows()):
            row = {
                "window_id": window_id,
                "participant_id": pid,
                "time_idx": t,
                "day_in_study": float(r["day_in_study"]),
                "RHRS": float(r["RHRS"]),
            }
            for c in FEATURE_COLUMNS:
                row[c] = float(r[c])
            rows.append(row)

        for j, (_, r) in enumerate(decoder.iterrows(), start=14):
            row = {
                "window_id": window_id,
                "participant_id": pid,
                "time_idx": j,
                "day_in_study": float(r["day_in_study"]),
                "RHRS": float(r["RHRS"]),
            }
            # Future values of unknown covariates are not supplied to the model.
            for c in FEATURE_COLUMNS:
                row[c] = np.nan
            rows.append(row)

    return pd.DataFrame(rows), meta


all_df, meta = build_canonical_tft_frame(HORIZON)

# Exact same 70/15/15 split as all baseline models.
split = load_canonical_split(HORIZON)
train_ids = set("W" + split["meta_train"]["window_index"].astype(int).astype(str))
val_ids = set("W" + split["meta_val"]["window_index"].astype(int).astype(str))
test_ids = set("W" + split["meta_test"]["window_index"].astype(int).astype(str))

train_df = all_df[all_df["window_id"].isin(train_ids)].copy()
val_df = all_df[all_df["window_id"].isin(val_ids)].copy()
test_df = all_df[all_df["window_id"].isin(test_ids)].copy()

known_reals = ["day_in_study"]

def make_base_dataset(frame):
    return TimeSeriesDataSet(
        frame,
        time_idx="time_idx",
        target="RHRS",
        group_ids=["window_id"],
        min_encoder_length=14,
        max_encoder_length=14,
        min_prediction_length=HORIZON,
        max_prediction_length=HORIZON,
        time_varying_known_reals=known_reals,
        time_varying_unknown_reals=UNKNOWN_REALS,
        target_normalizer=TorchNormalizer(method="identity"),
        add_relative_time_idx=True,
        add_encoder_length=True,
        allow_missing_timesteps=False,
    )

# The base dataset contains every canonical window solely so categorical encoders
# know every window id. It is never used for training directly.
base_dataset = make_base_dataset(all_df)
training = TimeSeriesDataSet.from_dataset(
    base_dataset, train_df, stop_randomization=True
)
validation = TimeSeriesDataSet.from_dataset(
    base_dataset, val_df, stop_randomization=True
)
testing = TimeSeriesDataSet.from_dataset(
    base_dataset, test_df, stop_randomization=True
)

train_loader = training.to_dataloader(train=True, batch_size=64, num_workers=0)
val_loader = validation.to_dataloader(train=False, batch_size=64, num_workers=0)
test_loader = testing.to_dataloader(train=False, batch_size=64, num_workers=0)

# Keep the original TFT hyperparameters.
tft = TemporalFusionTransformer.from_dataset(
    training,
    learning_rate=0.01,
    hidden_size=32,
    attention_head_size=4,
    dropout=0.1,
    hidden_continuous_size=16,
    loss=RMSE(),
    reduce_on_plateau_patience=4,
)

checkpoint_callback = ModelCheckpoint(
    dirpath="results/stage5_forecasting/checkpoints",
    filename="tft_best",
    save_top_k=1,
    monitor="train_loss_epoch",
    mode="min",
)

trainer = Trainer(
    max_epochs=30,
    accelerator="auto",
    logger=False,
    callbacks=[checkpoint_callback],
)

trainer.fit(tft, train_loader, val_loader)
trainer.save_checkpoint("results/stage5_forecasting/checkpoints/tft_final.ckpt")

# Each canonical test sequence produces H predictions. The manuscript's H-day
# forecast target is the final decoder step, i.e. exactly H days after the encoder.
predictions_all = tft.predict(test_loader)
predictions_all = predictions_all.detach().cpu().numpy()

actuals_all = []
for _, y in test_loader:
    target = y[0]
    actuals_all.append(target.detach().cpu().numpy())
actuals_all = np.concatenate(actuals_all, axis=0)

if predictions_all.ndim == 1:
    predictions_all = predictions_all[:, None]
if actuals_all.ndim == 1:
    actuals_all = actuals_all[:, None]

predictions = predictions_all[:, -1]
actuals = actuals_all[:, -1]

if len(predictions) != len(split["meta_test"]):
    raise RuntimeError(
        f"TFT canonical test alignment failed: predictions={len(predictions)}, "
        f"expected={len(split['meta_test'])}"
    )

metrics = compute_all_metrics(actuals, predictions)
metrics["Model"] = "Temporal Fusion Transformer"
metrics["Horizon"] = HORIZON

with open(RESULTS_DIR / "tft_results.json", "w") as f:
    json.dump(metrics, f, indent=4)

# Keep the existing TFT prediction filename and the original first two columns.
pred_df = pd.DataFrame({
    "Actual": actuals,
    "Predicted": predictions,
})
for c in [
    "participant_id", "target_date", "target_day",
    "input_start_day", "input_end_day", "forecast_horizon", "window_index"
]:
    if c in split["meta_test"].columns:
        pred_df[c] = split["meta_test"][c].values
pred_df.to_csv(RESULTS_DIR / "tft_predictions.csv", index=False)

print("\n===================")
print("TFT RESULTS")
print("===================\n")
for k, v in metrics.items():
    print(f"{k}: {v}")
