"""Stage 9 inference ablations using the exact saved Stage 5 TFT checkpoint.

No model is retrained or substituted. Feature-removal rows are inference-time
feature-masking/sensitivity analyses on the same Stage 5 weights. The equal-weight
RHRS target variant is reported as not evaluable with a fixed checkpoint because
changing the target would require training a different model.
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from pytorch_forecasting import TimeSeriesDataSet, TemporalFusionTransformer
from pytorch_forecasting.data import TorchNormalizer

SCRIPT_DIR = Path(__file__).resolve().parent
# Supports both src/stage9_ablation/ layout and a standalone stage9_ablation folder.
PROJECT_ROOT = SCRIPT_DIR.parents[1] if SCRIPT_DIR.parent.name == "src" else SCRIPT_DIR.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.stage9_ablation.ablation_config import (
    ABLATIONS, EQUAL_WEIGHTS, FEATURE_COLUMNS, HORIZONS, RESULT_FILES,
)
from src.stage5_forecasting.evaluation_utils import load_canonical_split

DATA_PATH = PROJECT_ROOT / "data" / "processed" / "rhrs_dataset.csv"
TEMPORAL_DIR = PROJECT_ROOT / "data" / "processed" / "temporal_windows"
RESULTS_DIR = PROJECT_ROOT / "results" / "stage9_ablation"
DEFAULT_CHECKPOINT = PROJECT_ROOT / "results" / "stage5_forecasting" / "checkpoints" / "tft_final.ckpt"
ENCODER_LENGTH = 14
BATCH_SIZE = 64


def calculate_metrics(actual, predicted):
    actual = np.asarray(actual, dtype=float).reshape(-1)
    predicted = np.asarray(predicted, dtype=float).reshape(-1)
    error = predicted - actual
    ss_res = float(np.sum(error ** 2))
    ss_tot = float(np.sum((actual - np.mean(actual)) ** 2))
    corr = float(np.corrcoef(actual, predicted)[0, 1]) if np.std(actual) > 0 and np.std(predicted) > 0 else 0.0
    return {
        "MAE": float(np.mean(np.abs(error))),
        "RMSE": float(np.sqrt(np.mean(error ** 2))),
        "R2": float(1 - ss_res / ss_tot) if ss_tot > 0 else 0.0,
        "r": corr,
    }


def build_stage5_frame(horizon):
    """Reproduce the Stage 5 TFT frame schema; keep target name RHRS unchanged."""
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Dataset not found: {DATA_PATH}")
    meta_path = TEMPORAL_DIR / f"window_metadata_h{horizon}.csv"
    if not meta_path.exists():
        raise FileNotFoundError(f"Canonical Stage 5 metadata not found: {meta_path}")

    source = pd.read_csv(DATA_PATH).sort_values(["id", "day_in_study"]).reset_index(drop=True)
    required = {"id", "day_in_study", "RHRS", *FEATURE_COLUMNS}
    missing = sorted(required - set(source.columns))
    if missing:
        raise ValueError(f"Dataset missing Stage 5 TFT columns: {missing}")
    metadata = pd.read_csv(meta_path)
    rows = []
    for _, m in metadata.iterrows():
        pid = m["participant_id"]
        wid = f"W{int(m['window_index'])}"
        participant = source[source["id"] == pid].sort_values("day_in_study")
        encoder = participant[(participant["day_in_study"] >= m["input_start_day"]) & (participant["day_in_study"] <= m["input_end_day"])]
        decoder = participant[(participant["day_in_study"] > m["input_end_day"]) & (participant["day_in_study"] <= m["target_day"])]
        if len(encoder) != ENCODER_LENGTH or len(decoder) != horizon:
            raise ValueError(f"{wid}: encoder/decoder lengths {len(encoder)}/{len(decoder)}; expected {ENCODER_LENGTH}/{horizon}.")
        for t, (_, r) in enumerate(encoder.iterrows()):
            row = {"window_id": wid, "participant_id": pid, "time_idx": t,
                   "day_in_study": float(r["day_in_study"]), "RHRS": float(r["RHRS"])}
            row.update({c: float(r[c]) for c in FEATURE_COLUMNS})
            rows.append(row)
        for t, (_, r) in enumerate(decoder.iterrows(), start=ENCODER_LENGTH):
            row = {"window_id": wid, "participant_id": pid, "time_idx": t,
                   "day_in_study": float(r["day_in_study"]), "RHRS": float(r["RHRS"])}
            # Match Stage 5: future unknown covariates are not exposed to the model.
            row.update({c: np.nan for c in FEATURE_COLUMNS})
            rows.append(row)
    return pd.DataFrame(rows), metadata


def make_stage5_dataset(frame, horizon):
    """Use the same target, known/unknown reals and dataset options as Stage 5."""
    return TimeSeriesDataSet(
        frame, time_idx="time_idx", target="RHRS", group_ids=["window_id"],
        min_encoder_length=ENCODER_LENGTH, max_encoder_length=ENCODER_LENGTH,
        min_prediction_length=horizon, max_prediction_length=horizon,
        time_varying_known_reals=["day_in_study"],
        time_varying_unknown_reals=list(FEATURE_COLUMNS) + ["RHRS"],
        target_normalizer=TorchNormalizer(method="identity"),
        add_relative_time_idx=True, add_encoder_length=True,
        allow_missing_timesteps=False,
    )


def load_stage5_checkpoint(checkpoint_path, horizon):
    if not checkpoint_path.exists():
        raise FileNotFoundError(
            "The saved Stage 5 TFT checkpoint is required; no new model will be trained. "
            f"Expected checkpoint: {checkpoint_path}. Provide --checkpoint with the actual Stage 5 checkpoint."
        )
    model = TemporalFusionTransformer.load_from_checkpoint(str(checkpoint_path), map_location="cpu")
    # A checkpoint's decoder length is part of its learned model shape. Never silently
    # train a replacement or claim an incompatible checkpoint is the same trained model.
    saved_horizon = getattr(model, "hparams", {}).get("max_prediction_length", None)
    if saved_horizon is None:
        saved_horizon = getattr(model, "max_prediction_length", None)
    if saved_horizon is not None and int(saved_horizon) != int(horizon):
        raise ValueError(
            f"Checkpoint {checkpoint_path} is configured for prediction length {saved_horizon}, "
            f"but H{horizon} data was requested. Use the matching Stage 5 checkpoint; "
            "this script will not retrain or substitute another model."
        )
    model.eval()
    return model


def run_one(horizon, key, checkpoint_path, batch_size):
    spec = ABLATIONS[key]
    if spec["target_mode"] != "original_rhrs":
        return {
            "configuration": spec["label"], "ablation_key": key,
            "ablation_type": spec["type"], "target_mode": spec["target_mode"],
            "removed_input_features": spec["removed_features"], "horizon": horizon,
            "model": "saved Stage 5 pytorch_forecasting.TemporalFusionTransformer",
            "checkpoint": str(checkpoint_path), "status": "not_evaluable_with_fixed_checkpoint",
            "reason": "Equal-weight RHRS changes the supervised target; evaluating it requires a separately trained model, which is intentionally not done because this run must reuse the exact saved Stage 5 checkpoint.",
            "test_samples": 0, "MAE": None, "RMSE": None, "R2": None, "r": None,
        }

    frame, metadata = build_stage5_frame(horizon)
    split = load_canonical_split(horizon)
    if len(metadata) != len(split["meta"]):
        raise RuntimeError(f"H{horizon}: window metadata count does not match Stage 5 canonical split.")
    train_ids = set("W" + split["meta_train"]["window_index"].astype(int).astype(str))
    test_ids = set("W" + split["meta_test"]["window_index"].astype(int).astype(str))
    train_df = frame[frame.window_id.isin(train_ids)].copy()
    test_df = frame[frame.window_id.isin(test_ids)].copy()

    # Use Stage 5's exact feature schema for every run. Ablations mask one encoder
    # feature to its training-encoder median; the model weights/architecture remain fixed.
    removed = spec["removed_features"]
    if removed:
        encoder_rows = train_df[train_df["time_idx"] < ENCODER_LENGTH]
        for feature in removed:
            median = float(encoder_rows[feature].median())
            test_encoder_mask = test_df["time_idx"] < ENCODER_LENGTH
            test_df.loc[test_encoder_mask, feature] = median

    base_dataset = make_stage5_dataset(frame, horizon)
    testing = TimeSeriesDataSet.from_dataset(base_dataset, test_df, stop_randomization=True)
    test_loader = testing.to_dataloader(train=False, batch_size=batch_size, num_workers=0)
    model = load_stage5_checkpoint(checkpoint_path, horizon)

    predictions = model.predict(test_loader)
    if hasattr(predictions, "detach"):
        predictions = predictions.detach().cpu().numpy()
    predictions = np.asarray(predictions)
    actual_batches = []
    for _, y in test_loader:
        target = y[0] if isinstance(y, (tuple, list)) else y
        actual_batches.append(target.detach().cpu().numpy())
    actual = np.concatenate(actual_batches, axis=0)
    if predictions.ndim == 1:
        predictions = predictions[:, None]
    if actual.ndim == 1:
        actual = actual[:, None]
    predictions, actual = predictions[:, -1], actual[:, -1]
    expected = len(split["meta_test"])
    if len(predictions) != expected or len(actual) != expected:
        raise RuntimeError(f"H{horizon} {key} alignment failure: predictions={len(predictions)}, actual={len(actual)}, expected={expected}")

    return {
        "configuration": spec["label"], "ablation_key": key,
        "ablation_type": "fixed_checkpoint_inference_feature_masking" if removed else spec["type"],
        "target_mode": "original_rhrs", "removed_input_features": removed,
        "feature_masking": "training-encoder median replacement" if removed else "none",
        "horizon": horizon,
        "model": "saved Stage 5 pytorch_forecasting.TemporalFusionTransformer",
        "checkpoint": str(checkpoint_path), "status": "evaluated",
        "epochs_requested": 0, "epochs_trained": 0,
        "test_samples": int(len(actual)), **calculate_metrics(actual, predictions),
    }


def run_horizon(horizon, checkpoint_path, batch_size):
    results = []
    for key in ABLATIONS:
        print(f"[H{horizon}] Evaluating saved Stage 5 checkpoint for {key}: {ABLATIONS[key]['label']}", flush=True)
        result = run_one(horizon, key, checkpoint_path, batch_size)
        results.append(result)
        print(json.dumps(result, indent=2), flush=True)
    payload = {
        "experiment": "WomenHealthAI Stage 9 fixed-checkpoint TFT inference ablation",
        "task": f"{horizon}-day RHRS forecasting",
        "model": "saved Stage 5 pytorch_forecasting.TemporalFusionTransformer",
        "checkpoint": str(checkpoint_path),
        "training_performed": False,
        "alignment": "Stage 5 canonical window metadata and 70/15/15 chronological split",
        "ablation_method": "Feature removals are inference-time median masking with identical Stage 5 model weights; they are sensitivity analyses, not retrained feature-removal models.",
        "target_note": "Equal-weight RHRS is retained in the configuration/output schema but marked not evaluable because a fixed original-target checkpoint cannot be used to claim a separately trained equal-weight-target experiment.",
        "metrics": {"MAE": "lower_is_better", "RMSE": "lower_is_better", "R2": "higher_is_better", "r": "higher_is_better"},
        "results": results,
    }
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    out = RESULTS_DIR / RESULT_FILES[horizon]
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--horizon", type=int, nargs="+", choices=HORIZONS, default=[14],
                        help="Must match the prediction length of the supplied Stage 5 checkpoint.")
    parser.add_argument("--checkpoint", type=Path, default=DEFAULT_CHECKPOINT,
                        help="Path to the saved Stage 5 TFT checkpoint; no training fallback is permitted.")
    parser.add_argument("--batch-size", type=int, default=BATCH_SIZE)
    args = parser.parse_args()
    if args.batch_size < 1:
        parser.error("--batch-size must be a positive integer")
    for horizon in args.horizon:
        print(f"Saved: {run_horizon(horizon, args.checkpoint.resolve(), args.batch_size)}")

if __name__ == "__main__":
    main()
