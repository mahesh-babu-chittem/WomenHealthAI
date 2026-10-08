import numpy as np
import pandas as pd
from pathlib import Path

TEMPORAL_DIR = Path("data/processed/temporal_windows")
RESULTS_DIR = Path("results/stage5_forecasting")

TRAIN_RATIO = 0.70
VAL_RATIO = 0.15
TEST_RATIO = 0.15


def load_canonical_split(horizon):
    """Load X/y plus the single canonical chronological split used by every model."""
    X = np.load(TEMPORAL_DIR / f"X_h{horizon}.npy")
    y = np.load(TEMPORAL_DIR / f"y_h{horizon}.npy")
    meta = pd.read_csv(TEMPORAL_DIR / f"window_metadata_h{horizon}.csv")

    if len(X) != len(y) or len(X) != len(meta):
        raise ValueError(
            f"Canonical alignment failure for H{horizon}: "
            f"X={len(X)}, y={len(y)}, metadata={len(meta)}"
        )

    train_end = int(len(X) * TRAIN_RATIO)
    val_end = int(len(X) * (TRAIN_RATIO + VAL_RATIO))

    return {
        "X": X,
        "y": y,
        "meta": meta,
        "train_idx": np.arange(0, train_end),
        "val_idx": np.arange(train_end, val_end),
        "test_idx": np.arange(val_end, len(X)),
        "X_train": X[:train_end],
        "y_train": y[:train_end],
        "X_val": X[train_end:val_end],
        "y_val": y[train_end:val_end],
        "X_test": X[val_end:],
        "y_test": y[val_end:],
        "meta_train": meta.iloc[:train_end].reset_index(drop=True),
        "meta_val": meta.iloc[train_end:val_end].reset_index(drop=True),
        "meta_test": meta.iloc[val_end:].reset_index(drop=True),
    }


def save_predictions(actual, predicted, metadata, output_file, horizon):
    """Preserve the existing first two prediction columns and append matching keys."""
    actual = np.asarray(actual).reshape(-1)
    predicted = np.asarray(predicted).reshape(-1)
    metadata = metadata.reset_index(drop=True).copy()

    if len(actual) != len(predicted) or len(actual) != len(metadata):
        raise ValueError(
            f"Prediction alignment failure for H{horizon}: "
            f"actual={len(actual)}, predicted={len(predicted)}, metadata={len(metadata)}"
        )

    # The first two columns intentionally retain the existing schema used by
    # figures/statistical scripts: Actual/Predicted or Actual_RHRS/Predicted_RHRS.
    out = pd.DataFrame({
        "Actual_RHRS": actual,
        "Predicted_RHRS": predicted,
    })

    # Keep stable matching keys after the original two columns.
    key_cols = [
        c for c in [
            "participant_id",
            "target_date",
            "target_day",
            "input_start_day",
            "input_end_day",
            "forecast_horizon",
            "window_index",
        ] if c in metadata.columns
    ]
    for c in key_cols:
        out[c] = metadata[c].values

    # Preserve exact two-column compatibility for consumers that use the first
    # two columns, while adding the information required for true paired tests.
    out.to_csv(output_file, index=False)
    return out


def prediction_key_frame(df, horizon):
    """Return a standardized key/error frame for paired statistical tests."""
    actual_col = "Actual_RHRS" if "Actual_RHRS" in df.columns else df.columns[0]
    pred_col = "Predicted_RHRS" if "Predicted_RHRS" in df.columns else df.columns[1]

    required = ["participant_id", "target_day", "forecast_horizon"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(
            "Prediction CSV is missing canonical matching columns: " + ", ".join(missing)
        )

    out = df.copy()
    out["forecast_horizon"] = pd.to_numeric(out["forecast_horizon"], errors="raise").astype(int)
    out = out[out["forecast_horizon"] == int(horizon)].copy()
    out["_actual"] = pd.to_numeric(out[actual_col], errors="raise")
    out["_predicted"] = pd.to_numeric(out[pred_col], errors="raise")
    out["_error"] = (out["_actual"] - out["_predicted"]).abs()

    # target_day is the canonical forecast target. Together with participant_id
    # and horizon it uniquely identifies a forecast observation.
    return out[
        ["participant_id", "target_day", "forecast_horizon", "_actual", "_predicted", "_error"]
    ]


def find_prediction_file(results_dir, horizon, model_name):
    """Prefer the existing h7_/h14_ convention; fall back to the current generic filename."""
    prefixed = results_dir / f"h{horizon}_{model_name}_predictions.csv"
    if prefixed.exists():
        return prefixed

    generic = results_dir / f"{model_name}_predictions.csv"
    if generic.exists():
        return generic

    return None
